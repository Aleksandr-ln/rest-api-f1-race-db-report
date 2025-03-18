import unittest
from datetime import datetime

from racing_report_api.database.setup_db import (
    parse_abbreviations, parse_log_file
)


class TestSetupDB(unittest.TestCase):
    def setUp(self):
        self.abbreviations_file = 'test_abbreviations.txt'
        self.log_file = 'test_log.txt'
        self.invalid_log_file = 'test_invalid_log.txt'

    def tearDown(self):
        import os
        for file in [
            self.abbreviations_file, self.log_file, self.invalid_log_file
        ]:
            if os.path.exists(file):
                os.remove(file)

    def test_parse_abbreviations(self):
        data = "SVF_Sebastian Vettel_FERRARI\nDRR_Daniel Ricciardo_REDBULL"
        with open('test_abbreviations.txt', 'w') as f:
            f.write(data)
        result = parse_abbreviations('test_abbreviations.txt')
        expected = {
            'SVF': {'name': 'Sebastian Vettel', 'team': 'FERRARI'},
            'DRR': {'name': 'Daniel Ricciardo', 'team': 'REDBULL'}
        }
        self.assertEqual(result, expected)

    def test_parse_log_file(self):
        data = "SVF2018-05-24_12:02:58.917\nDRR2018-05-24_12:05:58.778"
        with open('test_log.txt', 'w') as f:
            f.write(data)
        result = parse_log_file('test_log.txt')
        expected = {
            'SVF': datetime(2018, 5, 24, 12, 2, 58, 917000),
            'DRR': datetime(2018, 5, 24, 12, 5, 58, 778000)
        }
        self.assertEqual(result, expected)

    def test_invalid_log_format(self):
        data = "INVALID_LINE_WITHOUT_UNDERSCORE"
        with open(self.invalid_log_file, 'w') as f:
            f.write(data)

        result = parse_log_file(self.invalid_log_file)

        self.assertEqual(len(result), 0)
