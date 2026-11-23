"""Full-document coverage and Qdrant upload boundaries; no inference doubles."""
import importlib.util
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import tempfile
from threading import Thread
import unittest

from handbook import VectorIndex
from qdrant_index import QdrantIndex


HAS_INGEST = (importlib.util.find_spec('pymupdf4llm') is not None
              and importlib.util.find_spec('langchain_text_splitters') is not None)


@unittest.skipUnless(HAS_INGEST, 'Install the ingest extra to check PDF extraction.')
class PDFIngestionTests(unittest.TestCase):
    def test_failed_bundle_write_does_not_publish_partial_json(self):
        from qdrant_add_pdf import save_bundle
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'handbook-full.json'
            with self.assertRaises(TypeError):
                save_bundle(path, {'valid_prefix': 'content', 'invalid_tail': object()})
            self.assertFalse(path.exists())
            save_bundle(path, {'complete': True})
            self.assertEqual(json.loads(path.read_text()), {'complete': True})
            with self.assertRaises(FileExistsError):
                save_bundle(path, {'replacement': True})
            self.assertEqual(json.loads(path.read_text()), {'complete': True})

    def test_all_pages_and_short_passages_survive_chunking(self):
        from qdrant_add_pdf import chunks_from_pages
        pages = [
            {'text': '**A. Registration**\n\nRegister before term starts.',
             'metadata': {'page_number': 1}},
            {'text': 'A short but important footnote.', 'metadata': {'page_number': 2}},
            {'text': '# Final appendix\n\nThe last page is included.',
             'metadata': {'page_number': 137}},
        ]
        chunks = chunks_from_pages(pages, 'a' * 64)
        self.assertEqual({c['page'] for c in chunks}, {1, 2, 137})
        self.assertTrue(any('short but important footnote' in c['text'] for c in chunks))
        self.assertTrue(any('last page is included' in c['text'] for c in chunks))
        self.assertEqual([c['id'] for c in chunks],
                         [c['id'] for c in chunks_from_pages(pages, 'a' * 64)])
        self.assertEqual(len({c['id'] for c in chunks}), len(chunks))

    def test_long_sections_keep_their_tail_and_page_metadata(self):
        from qdrant_add_pdf import chunks_from_pages
        words = [f'word{i:04d}' for i in range(1000)]
        chunks = chunks_from_pages([
            {'text': '# Long section\n\n' + ' '.join(words),
             'metadata': {'page': 19}},
        ], 'b' * 64)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(c['text']) <= 1500 for c in chunks))
        self.assertTrue(all(c['page'] == 19 for c in chunks))
        recovered = set(' '.join(c['text'] for c in chunks).split())
        self.assertTrue(set(words) <= recovered)

    def test_real_pdf_extraction_includes_first_middle_and_last_page(self):
        import pymupdf
        from qdrant_add_pdf import extract_pages, chunks_from_pages
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'three-pages.pdf'
            with pymupdf.open() as document:
                for text in ['First page registration.', 'Middle page fees.',
                             'Last page graduation.']:
                    page = document.new_page()
                    page.insert_text((72, 72), text)
                document.save(path)
            pages = extract_pages(path)
            self.assertEqual(len(pages), 3)
            chunks = chunks_from_pages(pages, 'c' * 64)
            self.assertEqual({c['page'] for c in chunks}, {1, 2, 3})
            self.assertTrue(any('graduation' in c['text'] for c in chunks))


class QdrantUploadTests(unittest.TestCase):
    def test_batched_http_upload_preserves_every_point_and_is_repeatable(self):
        points = {}
        batch_sizes = []

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def send(self, result):
                data = json.dumps({'result': result}).encode()
                self.send_response(200)
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                self.send({'collections': []})

            def do_PUT(self):
                body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                if self.path.endswith('/points?wait=true'):
                    batch_sizes.append(len(body['points']))
                    points.update({p['id']: p for p in body['points']})
                self.send({'status': 'completed'})

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        index = VectorIndex({'source': {'title': 'Protocol fixture'},
                             'encoder': {'dimension': 2},
                             'chunks': [{'id': f'page-{i}', 'page': i,
                                         'text': f'Page {i}', 'vector': [1., .5]}
                                        for i in range(1, 6)]})
        remote = QdrantIndex(index, server.server_port)
        remote.seed(batch_size=2)
        self.assertEqual(batch_sizes, [2, 2, 1])
        self.assertEqual({p['payload']['page'] for p in points.values()}, {1, 2, 3, 4, 5})
        self.assertTrue(all(len(p['vector']) == 2 for p in points.values()))
        remote.seed(batch_size=2)
        self.assertEqual(len(points), 5)


if __name__ == '__main__':
    unittest.main()
