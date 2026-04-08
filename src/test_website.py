from website import extract_title
import unittest

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# This is a title"
        extracted = extract_title(md)
        self.assertEqual(extracted, "This is a title")

    def test_missing_whitespace(self):
        md = "#This is a title"
        with self.assertRaises(ValueError):
            extracted = extract_title(md)

    def test_missing_hashtags(self):
        md = "This has no hashtags"
        with self.assertRaises(ValueError):
            extracted = extract_title(md)

    def test_too_many_hashtags(self):
        md = "## This is a title"
        with self.assertRaises(ValueError):
            extracted = extract_title(md)

    def test_hashtag_later(self):
        md = "A ## hashtags needs to be here"
        with self.assertRaises(ValueError):
            extracted = extract_title(md)

    def test_heading_in_second_line(self):
        md = "No heading \n# but a heading here"
        extracted = extract_title(md)
        self.assertEqual(extracted, "but a heading here")