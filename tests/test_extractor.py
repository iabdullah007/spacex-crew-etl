from __future__ import annotations

import unittest

from src.etl.extractor import Extractor


class TestExtractData(unittest.TestCase):
    def test_api_response(self):
        extractor = Extractor()
        response_data = extractor.extract_data()
        self.assertTrue(len(response_data))
