from __future__ import annotations

import unittest

from src.etl.transformer import Transformer


class TestTransformer(unittest.TestCase):
    def test_transformer_valid_unit_mm(self):
        transformer = Transformer(
            raw_data=[
                {
                    'name': 'Robert Behnken',
                    'agency': 'NASA',
                    'wikipedia': 'https://en.wikipedia.org/wiki/Robert_L._Behnken',
                    'launches': ['5eb87d46ffd86e000604b388'],
                    'status': 'active',
                    'id': '5ebf1a6e23a9a60006e03a7a',
                },
            ],
        )
        res = transformer.transform_data()[0]
        self.assertEqual(res.id, '5ebf1a6e23a9a60006e03a7a')
        self.assertEqual(res.name, 'Robert Behnken')
        self.assertEqual(res.status.value, 'active')
        self.assertEqual(res.launches, ['5eb87d46ffd86e000604b388'])
