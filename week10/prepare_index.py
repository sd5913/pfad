"""Instructor preparation: real cached CLIP vectors with source and weight hashes.

CLIP is a short-text encoder, not a policy-specialized retriever. Check retrieved
passages empirically. This command never downloads weights or the handbook.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HANDBOOK_URL = ('https://www.polyu.edu.hk/ar/docdrive/polyu-students/student-handbook/'
                'Student_Handbook_2026-27_English.pdf')


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


class ClipEncoder:
    def __init__(self, snapshot):
        import torch
        from transformers import CLIPTextModel, CLIPTokenizer
        self.torch = torch
        snapshot = Path(snapshot)
        self.tokenizer = CLIPTokenizer.from_pretrained(str(snapshot / 'tokenizer'), local_files_only=True)
        self.model = CLIPTextModel.from_pretrained(str(snapshot / 'text_encoder'),
                                                  local_files_only=True).eval().to('cpu')
        self.identity = {
            'kind': 'clip-pooler', 'name': 'stable-diffusion-v1-5/CLIPTextModel',
            'digest': digest(snapshot / 'text_encoder' / 'model.safetensors'),
            'tokenizer_sha256': digest(snapshot / 'tokenizer' / 'vocab.json'),
            'merges_sha256': digest(snapshot / 'tokenizer' / 'merges.txt'),
            'dimension': self.model.config.hidden_size,
            'pooling': 'EOS pooler_output; L2 normalized', 'max_tokens': 77,
        }

    def encode(self, texts):
        inputs = self.tokenizer(texts, padding=True, truncation=False, return_tensors='pt')
        if inputs['input_ids'].shape[1] > 77:
            raise ValueError('CLIP accepts at most 77 tokens. Shorten the query or chunk; no truncation.')
        with self.torch.no_grad():
            output = self.model(**inputs).pooler_output
            return self.torch.nn.functional.normalize(output, dim=-1).tolist()

    def chunks(self, text):
        current = []
        for word in text.split():
            candidate = ' '.join(current + [word])
            if len(self.tokenizer.encode(candidate)) > 70:
                if not current:
                    raise ValueError('One source word exceeds the encoder limit.')
                yield ' '.join(current)
                current = [word]
            else:
                current.append(word)
        if current:
            yield ' '.join(current)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', required=True)
    parser.add_argument('--encoder-path', required=True)
    parser.add_argument('--pages', required=True, help='Comma-separated one-based PDF pages, e.g. 8,9')
    parser.add_argument('--retrieved-on', required=True, help='Actual retrieval date, YYYY-MM-DD')
    parser.add_argument('--query', action='append', required=True, help='Repeat for at least two short questions')
    parser.add_argument('--out', default='fixtures/handbook.json')
    args = parser.parse_args()
    if len(args.query) < 2:
        parser.error('Prepare at least two query vectors.')
    if Path(args.out).exists():
        parser.error('Output exists; choose a new versioned path, then review the diff.')
    encoder = ClipEncoder(args.encoder_path)
    chunks = []
    for page in sorted(set(int(p) for p in args.pages.split(','))):
        if page < 1:
            parser.error('PDF pages are one-based.')
        extracted = subprocess.run(['pdftotext', '-f', str(page), '-l', str(page),
                                    args.pdf, '-'], capture_output=True, text=True, check=True).stdout
        for number, text in enumerate(encoder.chunks(extracted), 1):
            chunks.append({'id': f'hb2026-p{page:03d}-c{number:02d}', 'page': page, 'text': text})
    if not chunks:
        parser.error('No source text extracted; inspect the PDF/OCR before proceeding.')
    for offset in range(0, len(chunks), 16):
        batch = chunks[offset:offset + 16]
        for chunk, vector in zip(batch, encoder.encode([c['text'] for c in batch])):
            chunk['vector'] = vector
    queries = [{'text': text, 'vector': vector}
               for text, vector in zip(args.query, encoder.encode(args.query))]
    bundle = {'source': {'title': 'PolyU Student Handbook 2026-27 (English)', 'year': '2026-27',
                         'url': HANDBOOK_URL, 'sha256': digest(args.pdf),
                         'retrieved_on': args.retrieved_on, 'page_numbering': 'PDF position, one-based',
                         'scope': 'Selected-page teaching extract; not the complete handbook'},
              'encoder': encoder.identity, 'chunks': chunks, 'queries': queries}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Wrote {len(chunks)} real vectors; inspect source/title/pages and both query rankings before use.')


if __name__ == '__main__':
    main()
