"""Pinned local encoders; documents and questions always share an identity."""
from pathlib import Path

MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
REVISION = '1110a243fdf4706b3f48f1d95db1a4f5529b4d41'
IDENTITY = {'kind': 'sentence-transformer', 'name': MODEL, 'revision': REVISION,
            'dimension': 384, 'pooling': 'attention-masked mean; L2 normalized',
            'max_tokens': 256}
QWEN_IDENTITY = {
    'kind': 'sentence-transformer', 'name': 'Qwen/Qwen3-Embedding-0.6B',
    'revision': '97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3',
    'dimension': 1024, 'pooling': 'last-token; L2 normalized', 'max_tokens': 32768,
    'dtype': 'float32',
    'query_prompt': ('Instruct: Given a web search query, retrieve relevant passages '
                     'that answer the query\nQuery:'),
}


class Encoder:
    def __init__(self, download=False, identity=None, device='cpu'):
        import torch
        from sentence_transformers import SentenceTransformer
        torch.set_num_threads(4)
        if device not in ('cpu', 'cuda'):
            raise ValueError('Choose cpu or cuda for the encoder device.')
        if device == 'cuda' and not torch.cuda.is_available():
            raise RuntimeError('CUDA is unavailable in this environment; use cpu or prepare a CUDA runtime.')
        identity = IDENTITY if identity is None else identity
        if identity not in (IDENTITY, QWEN_IDENTITY):
            raise ValueError('Unknown encoder identity; use a supported pinned model.')
        self.identity = dict(identity)
        # Avoid slow BF16 emulation on laptop CPUs without native BF16 support.
        options = {'model_kwargs': {'dtype': torch.float32}} if identity == QWEN_IDENTITY else {}
        self.model = SentenceTransformer(identity['name'], revision=identity['revision'], device=device,
                                        cache_folder=str(Path(__file__).parent / 'out' / 'models'),
                                        local_files_only=not download, **options)
        self.model.max_seq_length = identity['max_tokens']

    def encode(self, texts, query=False, batch_size=8, show_progress=False):
        prompt = self.identity.get('query_prompt', '') if query else ''
        for text in texts:
            if len(self.model.tokenizer.encode(prompt + text)) > self.identity['max_tokens']:
                raise ValueError(f"Input exceeds {self.identity['max_tokens']} tokens; "
                                 'split the passage or shorten the query.')
        return self.model.encode(texts, prompt=prompt, batch_size=batch_size,
                                 normalize_embeddings=True,
                                 show_progress_bar=show_progress).tolist()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download', action='store_true', help='Explicit one-time public model preparation')
    parser.add_argument('--qwen', action='store_true', help='Prepare the full-PDF Qwen3 embedding model')
    args = parser.parse_args()
    encoder = Encoder(download=args.download, identity=QWEN_IDENTITY if args.qwen else IDENTITY)
    print(encoder.identity)
    print('Ready:', len(encoder.encode(['A test question'])[0]), 'dimensions')
