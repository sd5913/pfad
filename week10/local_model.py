"""Documented Ollama HTTP contract; local-only, never auto-downloads models."""
import json
import urllib.error
import urllib.request


class Ollama:
    def __init__(self, model, port=11434):
        self.model = model
        self.base = f'http://127.0.0.1:{int(port)}'

    def request(self, route, data=None):
        request = urllib.request.Request(self.base + route,
                                         data=json.dumps(data).encode() if data else None,
                                         headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                result = json.load(response)
        except (urllib.error.URLError, TimeoutError) as error:
            raise RuntimeError('Local model unavailable. Check the prepared Ollama server/model; '
                               'no turn was saved and no model is downloaded automatically.') from error
        if 'error' in result:
            raise RuntimeError(result['error'])
        return result

    def chat(self, messages, tools):
        result = self.request('/api/chat', {'model': self.model, 'messages': messages,
                                          'tools': tools, 'stream': False,
                                          'options': {'temperature': 0, 'num_predict': 600}})
        return result['message']

    def identity(self):
        for model in self.request('/api/tags')['models']:
            if self.model in (model['name'], model.get('model')):
                return model['digest']
        raise RuntimeError('The named model is not installed locally.')

    def embed(self, text, encoder):
        if encoder['name'] != self.model or encoder['digest'] != self.identity():
            raise ValueError('Local embedding model does not match this index.')
        return self.request('/api/embed', {'model': self.model, 'input': text,
                                           'truncate': False})['embeddings'][0]
