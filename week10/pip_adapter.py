"""Reuse Week 6 Pip's local-only HTTP client with Week 10's bounded agent loop."""
from pathlib import Path
import sys

SPEECH = Path(__file__).resolve().parents[1] / 'week06' / 'speech'
if str(SPEECH) not in sys.path:
    sys.path.append(str(SPEECH))
import local_reply
from local_model import LlamaServer


class PipModel(LlamaServer):
    def __init__(self, model, base=local_reply.DEFAULT_URL):
        self.model = model
        self.base = local_reply.server_url(base)

    def request(self, route, data=None):
        # The inherited structured tool adapter uses /v1 paths; Pip's base includes /v1.
        return local_reply.call(self.base, route.removeprefix('/v1'), data)

    def identity(self):
        if self.model not in local_reply.list_models(self.base):
            raise ValueError('Load and select this chat model in LM Studio first.')
        return self.model
