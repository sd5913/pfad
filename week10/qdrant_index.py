"""The same handbook vectors, served through Qdrant's HTTP API."""
import argparse
import hashlib
import json
import uuid
from urllib import request

from handbook import VectorIndex, normalized


class QdrantIndex:
    def __init__(self, index, port=6333):
        self.index = index
        self.encoder = index.encoder
        self.base = f'http://127.0.0.1:{int(port)}'
        # Content-addressed collection: changed corpus/encoder gets a new collection.
        data = {'encoder': index.encoder, 'source': index.source, 'chunks': index.chunks}
        self.collection = 'sd5913_' + hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()).hexdigest()[:16]

    def call(self, method, route, payload=None):
        from urllib.error import URLError
        data = None if payload is None else json.dumps(payload).encode()
        req = request.Request(self.base + route, data=data, method=method,
                              headers={'Content-Type': 'application/json'})
        class NoRedirect(request.HTTPRedirectHandler):
            def redirect_request(self, *args):
                raise ValueError('Qdrant redirected; check the local service.')
        try:
            opener = request.build_opener(request.ProxyHandler({}), NoRedirect())
            with opener.open(req, timeout=15) as response:
                result = response.read(2_000_001)
            if len(result) > 2_000_000:
                raise ValueError('Qdrant response exceeds classroom limit.')
            return json.loads(result)['result']
        except URLError as error:
            raise RuntimeError('Qdrant unavailable or collection missing. Start the local service, '
                               'then run python qdrant_index.py seed. No fallback was substituted.') from error

    @property
    def route(self):
        return '/collections/' + self.collection

    def seed(self):
        collections = self.call('GET', '/collections')['collections']
        if self.collection not in [item['name'] for item in collections]:
            self.call('PUT', self.route, {'vectors': {'size': self.encoder['dimension'],
                                                    'distance': 'Cosine'}})
        points = [{'id': str(uuid.uuid5(uuid.NAMESPACE_URL, chunk['id'])),
                   'vector': vector,
                   'payload': {**{k: v for k, v in chunk.items() if k != 'vector'},
                               'encoder': self.encoder, 'source': self.index.source}}
                  for chunk, vector in zip(self.index.chunks, self.index.vectors)]
        self.call('PUT', self.route + '/points?wait=true', {'points': points})

    def search_vector(self, vector, encoder, limit=2):
        if encoder != self.encoder:
            raise ValueError('Encoder identity differs: rebuild documents and queries together.')
        if not 1 <= limit <= 5:
            raise ValueError('Retrieve between one and five passages.')
        result = self.call('POST', self.route + '/points/query', {
            'query': normalized(vector, self.encoder['dimension']), 'limit': limit,
            'with_payload': True})
        chunks = []
        for point in result['points']:
            payload = dict(point['payload'])
            if payload.pop('encoder') != self.encoder:
                raise ValueError('Stored encoder differs; use the matching seeded collection.')
            chunks.append({**payload, 'score': round(point['score'], 6)})
        return chunks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['seed', 'query'])
    parser.add_argument('--bundle', default='fixtures/handbook.json')
    parser.add_argument('--port', type=int, default=6333)
    args = parser.parse_args()
    index = VectorIndex.load(args.bundle)
    remote = QdrantIndex(index, args.port)
    print('COLLECTION', remote.collection)
    if args.action == 'seed':
        remote.seed()
        print('Seeded', len(index.chunks), 'points. Inspect', remote.base + '/dashboard')
    else:
        for query in index.queries:
            actual = remote.search_vector(query['vector'], index.encoder)
            expected = index.search_vector(query['vector'], index.encoder)
            if [c['id'] for c in actual] != [c['id'] for c in expected]:
                raise ValueError('Qdrant ranking differs from the reference cosine search.')
            print(query['text'], json.dumps(actual, ensure_ascii=False))


if __name__ == '__main__':
    main()
