"""Embed every PDF page with Qwen3 and upload its Markdown chunks to Qdrant.

Adapted from week10/handbook_app/qdrant_add_pdf.py on the 2025 branch,
revision 512edb07927c5d77cacc7279ba6be601b33dc601. Reuses its Markdown
section preprocessing and 1500/200 splitting, retaining page provenance.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

from encoder import Encoder, QWEN_IDENTITY
from handbook import VectorIndex
from prepare_index import HANDBOOK_URL, QUERIES
from qdrant_index import QdrantIndex

ROOT = Path(__file__).resolve().parent


def save_bundle(path, bundle):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                     prefix=path.name + '.', delete=False) as output:
        temporary = Path(output.name)
        try:
            json.dump(bundle, output, ensure_ascii=False)
            output.write('\n')
            output.flush()
            os.fsync(output.fileno())
            # Publish a complete file atomically without replacing an existing bundle.
            path.hardlink_to(temporary)
        finally:
            temporary.unlink()


def extract_pages(path):
    import pymupdf4llm
    return pymupdf4llm.to_markdown(str(path), page_chunks=True, use_ocr=False,
                                 write_images=False, show_progress=False)


def chunks_from_pages(pages, source_hash, chunk_size=1500, chunk_overlap=200):
    from langchain_text_splitters import MarkdownHeaderTextSplitter, MarkdownTextSplitter
    headers = MarkdownHeaderTextSplitter(
        headers_to_split_on=[('#', 'Chapter'), ('##', 'Section'),
                             ('###', 'Subsection'), ('######', 'Heading')],
        strip_headers=False)
    splitter = MarkdownTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = []
    for page in pages:
        metadata = page['metadata']
        number = metadata.get('page_number', metadata.get('page'))
        if not isinstance(number, int) or number < 1:
            raise ValueError('PDF extraction must retain one-based page numbers.')
        markdown = re.sub(r'\*\*([A-Z]\. [^*\n]+)\*\*', r'### \1', page['text'])
        sections = headers.split_text(markdown)
        for document in splitter.split_documents(sections):
            text = document.page_content.strip()
            if not text:
                continue
            digest = hashlib.sha256(text.encode()).hexdigest()[:16]
            chunks.append({'id': f'pdf-{source_hash[:12]}-p{number:03d}-{len(chunks):04d}-{digest}',
                           'page': number, 'text': text,
                           'section': ' > '.join(document.metadata.values()) or f'PDF page {number}'})
    if not chunks:
        raise ValueError('No extractable PDF text. A scanned document needs OCR before indexing.')
    return chunks


def build_bundle(pdf, encoder, chunk_size=1500, chunk_overlap=200, batch_size=8,
                 source_url=None):
    import pymupdf
    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
    pages = extract_pages(pdf)
    with pymupdf.open(pdf) as document:
        page_count = len(document)
        title = document.metadata.get('title') or pdf.name
    if len(pages) != page_count:
        raise ValueError('PDF extraction omitted pages; no partial index was published.')
    chunks = chunks_from_pages(pages, digest, chunk_size, chunk_overlap)
    covered = sorted({chunk['page'] for chunk in chunks})
    expected = {p['metadata'].get('page_number', p['metadata'].get('page'))
                for p in pages if p['text'].strip()}
    if set(covered) != expected:
        raise ValueError('Chunking omitted a page with text; no partial index was published.')
    print(f'Extracted {page_count} pages; {len(covered)} contain text; '
          f'embedding {len(chunks)} chunks with {encoder.identity["name"]}.', flush=True)
    vectors = encoder.encode([c['text'] for c in chunks], batch_size=batch_size,
                             show_progress=True)
    for chunk, vector in zip(chunks, vectors, strict=True):
        chunk['vector'] = vector
    questions = QUERIES + ['What is academic probation?',
                           'How do I apply for credit transfer?']
    query_vectors = encoder.encode(questions, query=True, batch_size=batch_size)
    return {
        'source': {'title': title, 'url': source_url, 'file': pdf.name,
                   'sha256': digest, 'pages': page_count},
        'encoder': encoder.identity,
        'ingestion': {'scope': 'full-pdf', 'pages_indexed': covered,
                      'empty_pages': sorted(set(range(1, page_count + 1)) - set(covered)),
                      'chunk_size': chunk_size, 'chunk_overlap': chunk_overlap,
                      'extraction': 'pymupdf4llm Markdown, page_chunks=True'},
        'chunks': chunks,
        'queries': [{'text': text, 'vector': vector}
                    for text, vector in zip(questions, query_vectors, strict=True)],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path,
                        default=ROOT / 'out/Student_Handbook_2026-27_English.pdf')
    parser.add_argument('--out', type=Path, default=ROOT / 'out/handbook-full.json')
    parser.add_argument('--source-url', help='Public provenance URL for a different input PDF')
    parser.add_argument('--download', action='store_true', help='Allow the pinned Qwen model download')
    parser.add_argument('--chunk-size', type=int, default=1500)
    parser.add_argument('--chunk-overlap', type=int, default=200)
    parser.add_argument('--batch-size', type=int, default=8, help='Embedding batch size')
    parser.add_argument('--device', choices=['cpu', 'cuda'], default='cpu')
    parser.add_argument('--port', type=int, default=6333)
    args = parser.parse_args()
    if not 0 <= args.chunk_overlap < args.chunk_size or args.batch_size < 1:
        parser.error('Use 0 <= chunk-overlap < chunk-size and a positive batch-size.')
    try:
        if args.out.exists():
            bundle = json.loads(args.out.read_text(encoding='utf-8'))
            matches = (bundle['source']['sha256'] == hashlib.sha256(args.pdf.read_bytes()).hexdigest()
                       and bundle['encoder'] == QWEN_IDENTITY
                       and bundle['ingestion']['chunk_size'] == args.chunk_size
                       and bundle['ingestion']['chunk_overlap'] == args.chunk_overlap)
            if not matches:
                raise ValueError('Existing bundle differs; choose a new --out path.')
            print('Reusing complete embedded bundle:', args.out, flush=True)
        else:
            encoder = Encoder(download=args.download, identity=QWEN_IDENTITY, device=args.device)
            source_url = args.source_url
            if source_url is None and args.pdf.name == 'Student_Handbook_2026-27_English.pdf':
                source_url = HANDBOOK_URL
            bundle = build_bundle(args.pdf, encoder, args.chunk_size, args.chunk_overlap,
                                  args.batch_size, source_url)
            save_bundle(args.out, bundle)
            print('Saved complete embedded bundle:', args.out, flush=True)
        index = VectorIndex(bundle)
        remote = QdrantIndex(index, args.port)
        remote.seed()
        count = remote.call('GET', remote.route)['points_count']
        if count != len(index.chunks):
            raise ValueError(f'Expected {len(index.chunks)} stored points, found {count}. Retry this command.')
        print(f'Indexed {len(index.chunks)} chunks from {len(bundle["ingestion"]["pages_indexed"])} '
              f'of {bundle["source"]["pages"]} PDF pages. Empty pages: '
              f'{bundle["ingestion"]["empty_pages"]}', flush=True)
        print('COLLECTION', remote.collection)
        print('Inspect', remote.base + '/dashboard')
    except (OSError, RuntimeError, ValueError, KeyError) as error:
        parser.exit(1, f'PDF ingestion failed: {error}\n')


if __name__ == '__main__':
    main()
