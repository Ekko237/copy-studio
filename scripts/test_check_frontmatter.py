"""Exercise the scalar unquoting used by the frontmatter checker."""

import unittest

from scripts.check_frontmatter import unquote


class UnquoteTests(unittest.TestCase):
    def test_unquoted_input_is_stripped(self):
        self.assertEqual(unquote("  copy bridge\t"), "copy bridge")

    def test_empty_input(self):
        self.assertEqual(unquote(""), "")

    def test_matching_single_quotes_are_removed(self):
        self.assertEqual(unquote(" 'dev notes' "), "dev notes")

    def test_doubled_apostrophe_is_decoded(self):
        self.assertEqual(unquote("'it''s ready'"), "it's ready")

    def test_escaped_double_quotes_are_decoded(self):
        self.assertEqual(unquote(r'"a \"working\" draft"'), 'a "working" draft')

    def test_escaped_newline_is_decoded(self):
        self.assertEqual(unquote(r'"first\nsecond"'), "first\nsecond")
