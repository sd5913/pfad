"""Fetch only the instructor-supplied public PDF; never guesses another year."""
import argparse
import hashlib
from pathlib import Path
import urllib.request

from prepare_index import HANDBOOK_URL


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', default='out/Student_Handbook_2026-27_English.pdf')
    args = parser.parse_args()
    destination = Path(args.out)
    if destination.exists():
        parser.error('Destination already exists; inspect it or choose a new path.')
    try:
        with urllib.request.urlopen(HANDBOOK_URL, timeout=30) as response:
            data = response.read(25 * 1024 * 1024 + 1)
        if len(data) > 25 * 1024 * 1024 or not data.startswith(b'%PDF-'):
            raise ValueError('Expected a PDF of at most 25 MiB; inspect the source response.')
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('xb') as output:
            output.write(data)
        print('URL', HANDBOOK_URL)
        print('SHA256', hashlib.sha256(data).hexdigest())
        print('BYTES', len(data))
        print('Now inspect title/year, section boundaries and PDF-page numbering before indexing.')
    except (OSError, ValueError) as error:
        parser.exit(1, f'Handbook download failed: {error}\n')


if __name__ == '__main__':
    main()
