"""One pinned CPU sentence encoder for both handbook chunks and questions."""
from pathlib import Path

MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
REVISION = '1110a243fdf4706b3f48f1d95db1a4f5529b4d41'
IDENTITY = {'kind': 'sentence-transformer', 'name': MODEL, 'revision': REVISION,
            'dimension': 384, 'pooling': 'attention-masked mean; L2 normalized',
            'max_tokens': 256}


class Encoder:
    def __init__(self, download=False):
        import torch
        from sentence_transformers import SentenceTransformer
        torch.set_num_threads(4)
        self.model = SentenceTransformer(MODEL, revision=REVISION, device='cpu',
                                        cache_folder=str(Path(__file__).parent / 'out' / 'models'),
                                        local_files_only=not download)
        self.identity = dict(IDENTITY)

    def encode(self, texts):
        for text in texts:
            if len(self.model.tokenizer.encode(text)) > 256:
                raise ValueError('Input exceeds 256 tokens; split the passage or shorten the query.')
        return self.model.encode(texts, normalize_embeddings=True,
                                 show_progress_bar=False).tolist()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download', action='store_true', help='Explicit one-time public model preparation')
    args = parser.parse_args()
    encoder = Encoder(download=args.download)
    print(encoder.identity)
    print('Ready:', len(encoder.encode(['A test question'])[0]), 'dimensions')
