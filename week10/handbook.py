"""Small cosine index: source text and encoder identity travel with each vector."""
import argparse
import json
import math
from pathlib import Path


def normalized(values, dimension):
    if len(values) != dimension or not all(isinstance(x, (int, float)) and math.isfinite(x) for x in values):
        raise ValueError('Vector dimension or finite-number check failed.')
    length = math.sqrt(sum(x * x for x in values))
    if not length:
        raise ValueError('A zero vector has no cosine direction.')
    return [x / length for x in values]


class VectorIndex:
    def __init__(self, bundle):
        self.source = bundle['source']
        self.encoder = bundle['encoder']
        self.chunks = bundle['chunks']
        self.queries = bundle.get('queries', [])
        if not self.chunks or len({c['id'] for c in self.chunks}) != len(self.chunks):
            raise ValueError('The index needs nonempty chunks with unique IDs.')
        self.vectors = [normalized(c['vector'], self.encoder['dimension']) for c in self.chunks]
        for chunk in self.chunks:
            if not chunk['text'].strip() or not isinstance(chunk['page'], int) or chunk['page'] < 1:
                raise ValueError('Each chunk needs source text and a one-based PDF page.')

    @classmethod
    def load(cls, path):
        if not Path(path).is_file():
            raise FileNotFoundError('Prepared handbook index is missing. See fixtures/README.md; '
                                    'do not substitute invented vectors or policy text.')
        return cls(json.loads(Path(path).read_text(encoding='utf-8')))

    def search_vector(self, vector, encoder, limit=2):
        if encoder != self.encoder:
            raise ValueError('Encoder identity differs: rebuild documents and queries together.')
        if not 1 <= limit <= 5:
            raise ValueError('Retrieve between one and five passages.')
        query = normalized(vector, self.encoder['dimension'])
        scored = [(sum(a * b for a, b in zip(query, v)), chunk)
                  for v, chunk in zip(self.vectors, self.chunks)]
        ranked = sorted(scored, key=lambda pair: pair[0], reverse=True)[:limit]
        return [{**{k: v for k, v in chunk.items() if k != 'vector'}, 'score': round(score, 6),
                 'source': self.source} for score, chunk in ranked]

    def prepared_query(self, question):
        for query in self.queries:
            if query['text'] == question:
                return self.search_vector(query['vector'], self.encoder)
        raise ValueError('No prepared vector for this exact question. Use the matching live encoder '
                         'for a new question; this fixture does not keyword-match.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', default='fixtures/handbook.json')
    parser.add_argument('--query')
    args = parser.parse_args()
    index = VectorIndex.load(args.bundle)
    print('SOURCE', json.dumps(index.source))
    print('ENCODER', json.dumps(index.encoder))
    print('FIRST VECTOR (first 8 values)', index.chunks[0]['vector'][:8])
    queries = [args.query] if args.query else [q['text'] for q in index.queries]
    for query in queries:
        print('QUERY', query)
        print(json.dumps(index.prepared_query(query), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
