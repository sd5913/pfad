"""Verify cited extracts against the downloaded PDF, then embed chunks and queries."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HANDBOOK_URL = ('https://www.polyu.edu.hk/ar/docdrive/polyu-students/student-handbook/'
                'Student_Handbook_2026-27_English.pdf')
QUERIES = ['What should I do if I lose my student identity card?',
           'How do I request leave from class?',
           'How much does replacing a lost student identity card cost?']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', default='out/Student_Handbook_2026-27_English.pdf')
    parser.add_argument('--out', default='fixtures/handbook.json')
    args = parser.parse_args()
    source = json.loads(Path('fixtures/chunks.json').read_text(encoding='utf-8'))
    pdf = Path(args.pdf)
    if hashlib.sha256(pdf.read_bytes()).hexdigest() != source['source']['sha256']:
        parser.error('PDF hash differs; review edition/pages/extracts before rebuilding.')
    if Path(args.out).exists():
        parser.error('Output exists; use --out out/rebuilt-handbook.json and review the diff.')
    for chunk in source['chunks']:
        page = str(chunk['page'])
        try:
            text = subprocess.run(['pdftotext', '-layout', '-f', page, '-l', page,
                                   str(pdf), '-'], capture_output=True, text=True, check=True).stdout
        except FileNotFoundError:
            parser.error('pdftotext is missing; install Poppler (poppler-utils on Debian/Ubuntu '
                         'or Fedora; poppler on Arch), then check pdftotext -v. '
                         'The supplied fixtures/handbook.json can be used without rebuilding.')
        if chunk['text'] not in ' '.join(text.split()):
            parser.error(f"Extract does not match PDF page: {chunk['id']}")
    from encoder import Encoder
    encoder = Encoder()
    for chunk, vector in zip(source['chunks'], encoder.encode([c['text'] for c in source['chunks']])):
        chunk['vector'] = vector
    source['encoder'] = encoder.identity
    source['queries'] = [{'text': text, 'vector': vector}
                         for text, vector in zip(QUERIES, encoder.encode(QUERIES))]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(source, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f"Verified {len(source['chunks'])} cited extracts; wrote real 384D vectors and three queries.")


if __name__ == '__main__':
    main()
