"""Regression checks on the supplied learned vectors, not keyword substitutes."""
from pathlib import Path
import unittest

from handbook import VectorIndex


class HandbookTests(unittest.TestCase):
    def setUp(self):
        self.index = VectorIndex.load(Path(__file__).parent / 'fixtures' / 'handbook.json')

    def test_prepared_real_questions_retrieve_the_relevant_cited_sections(self):
        expected = ['hb2026-p020-replacement', 'hb2026-p025-leave', 'hb2026-p076-fees']
        for query, chunk_id in zip(self.index.queries, expected, strict=True):
            with self.subTest(question=query['text']):
                results = self.index.prepared_query(query['text'])
                self.assertEqual(results[0]['id'], chunk_id)
                self.assertIn('text', results[0])
                self.assertGreater(results[0]['page'], 0)

    def test_fixture_cannot_answer_a_new_query_without_the_matching_encoder(self):
        with self.assertRaisesRegex(ValueError, 'matching live encoder'):
            self.index.prepared_query('An unprepared question')


if __name__ == '__main__':
    unittest.main()
