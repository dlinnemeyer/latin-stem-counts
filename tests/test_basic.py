import unittest
from run import (
    get_raw_counts, get_stem_counts, lookup, Definition, RawCount, StemCount,
    DefinedWord)


class BasicTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_get_raw_counts(self):
        self.assertCountEqual(get_raw_counts([
            "id est infinitum est id",
            "   ",
            "   id est blah something"
        ]), [
            RawCount("id", 3),
            RawCount("infinitum", 1),
            RawCount("blah", 1),
            RawCount("something", 1),
            RawCount("est", 3)
        ])

    # This is the nitty fritty. lots of parsing tests here
    # Note: we could move this to definition(), but I'd prefer just to toss in
    # a word and re-check words. guards against changes in words itself?
    def test_lookup(self):
        self.assertEqual(lookup("propheta"), Definition(
            "propheta",
            ["inflection1", "inflection2"]
        ))

    def test_get_stem_counts(self):
        defined_words = [
            DefinedWord(
                RawCount("WORD", 3),
                Definition("STEM", ["inflection1", "inflection2"])
            ),
            DefinedWord(
                RawCount("WORD2", 4),
                Definition("STEM", ["inflection3", "inflection4"])
            ),
            DefinedWord(
                RawCount("WORD3", 5),
                Definition("STEM2", ["inflection1", "inflection2"])
            )
        ]
        self.assertCountEqual(get_stem_counts(defined_words), [
            StemCount("STEM", defined_words[0:2], 7),
            StemCount("STEM2", [defined_words[2]], 5)
        ])
