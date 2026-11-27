"""Tests for the linear-time sentence splitter.

Run from this directory with ``python -m unittest test_sentence_split -v``.
"""

import time
import unittest

from sentence_split import split_sentences


class SplitSentencesTest(unittest.TestCase):
    def test_splits_on_terminators_and_drops_the_delimiter(self):
        self.assertEqual(
            split_sentences("Hello world. This is a test! Is it?"),
            ["Hello world", "This is a test", "Is it", ""],
        )

    def test_keeps_closing_quotes_and_brackets_out_of_the_sentence(self):
        self.assertEqual(
            split_sentences('He said "hi." Then left.'),
            ['He said "hi', "Then left", ""],
        )
        self.assertEqual(split_sentences("(Done.) Next."), ["(Done", "Next", ""])

    def test_consumes_surrounding_whitespace(self):
        self.assertEqual(
            split_sentences("Sentence one.  Sentence two.\nNew line."),
            ["Sentence one", "Sentence two", "New line", ""],
        )

    def test_handles_empty_and_unpunctuated_text(self):
        self.assertEqual(split_sentences(""), [""])
        self.assertEqual(split_sentences("no punctuation here"), ["no punctuation here"])

    def test_consecutive_punctuation_yields_empty_parts(self):
        self.assertEqual(split_sentences("What?!"), ["What", "", ""])

    def test_runs_in_linear_time_on_hostile_input(self):
        # A few hundred thousand characters of punctuation and whitespace used
        # to be worth a DoS attempt; the splitter must stay fast on all of them.
        hostile = [
            " " * 200_000,
            "." + '"' * 200_000,
            "." * 100_000,
            ("a " * 50_000) + ("." * 50_000),
        ]
        for text in hostile:
            started = time.perf_counter()
            split_sentences(text)
            elapsed = time.perf_counter() - started
            self.assertLess(elapsed, 1.0, f"took {elapsed:.3f}s on {len(text)} chars")


if __name__ == "__main__":
    unittest.main()
