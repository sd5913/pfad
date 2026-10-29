"""Local model HTTP adapters; never download a model or contact a paid endpoint."""
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
            raise RuntimeError('Local model unavailable. Check the prepared local server/model; '
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


class LlamaServer(Ollama):
    def __init__(self, model='handbook-local', port=11440):
        super().__init__(model, port)

    def identity(self):
        return self.request('/v1/models')['data'][0]['id']

    def chat(self, messages, tools):
        wire = json.loads(json.dumps(messages))
        for message in wire:
            if message['role'] == 'tool':
                message['name'] = message.pop('tool_name')
            for call in message.get('tool_calls', []):
                call['function']['arguments'] = json.dumps(call['function']['arguments'])
        payload = {
            'model': self.model, 'messages': wire, 'tools': tools,
            'tool_choice': 'required' if tools else 'auto', 'temperature': 0, 'max_tokens': 400,
            'reasoning_effort': 'none', 'stream': False}
        if not tools:
            source_ids = sorted({chunk['id'] for message in wire if message['role'] == 'tool'
                                 for chunk in json.loads(message['content'])})
            schema = {'type': 'object', 'properties': {
                'answer': {'type': 'string'},
                'source_ids': {'type': 'array', 'items': {'type': 'string', 'enum': source_ids}}},
                'required': ['answer', 'source_ids'], 'additionalProperties': False}
            payload['response_format'] = {'type': 'json_schema', 'json_schema': {
                'name': 'handbook_answer', 'schema': schema}}
            wire[0]['content'] += (' For the answer phase return JSON. Use source_ids=[] when '
                'the passages cannot answer the current question. '
                'Put a short answer without bracketed citations in answer; put the exact IDs '
                'of supporting passages in source_ids. A nearby topic alone is not support.')
        result = self.request('/v1/chat/completions', payload)
        reply = result['choices'][0]['message']
        for call in reply.get('tool_calls', []):
            arguments = call['function']['arguments']
            if isinstance(arguments, str):
                call['function']['arguments'] = json.loads(arguments)
        if not tools and not reply.get('tool_calls'):
            answer = json.loads(reply['content'])
            if any(source not in source_ids for source in answer['source_ids']):
                raise ValueError('The model returned an unknown source ID.')
            reply['structured_answer'] = answer
            reply['content'] = (answer['answer'].strip() + ' ' + ' '.join(
                '[' + source + ']' for source in answer['source_ids'])) if answer['source_ids'] else (
                    'I cannot answer from these sources.')
        return reply
