import unittest
from operator import attrgetter
from type_defs import StemCount, RawCount, Stem, PossibleStem, DefinedWord
from run import get_raw_counts, get_stem_counts, lookup


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

    # This is the nitty gritty. lots of parsing tests here
    # Note: we could move this to definition(), but I'd prefer just to toss in
    # a word and re-check words. guards against changes in words itself?
    def test_lookup(self):
        self.assertEqual(lookup("propheta"), [
            PossibleStem(
                stem=Stem(
                    latin='propheta, prophetae  N (1st) M   [XEXBO]',
                    english=(
                        'prophet; spokesman/interpreter of a god; '
                        'foreteller, soothsayer (L+S);'
                    )
                ),
                inflections=[
                    'prophet.a            N      1 1 NOM S M',
                    'prophet.a            N      1 1 VOC S M',
                    'prophet.a            N      1 1 ABL S M'
                ]
            ),
            PossibleStem(
                stem=Stem(
                    latin='prophetes, prophetae  N M   [DEXCS]    Late',
                    english=(
                        'prophet; spokesman/interpreter of a god; '
                        'foreteller, soothsayer (L+S);'
                    )
                ),
                inflections=[
                    'prophet.a            N      1 7 VOC S M',
                    'prophet.a            N      1 7 ABL S M'
                ]
            ),
            PossibleStem(
                stem=Stem(
                    latin=(
                        'propheto, prophetare, prophetavi, prophetatus  V '
                        '(1st)   [EEXCS]    Later'
                    ),
                    english='prophesy, foretell, predict;'
                ),
                inflections=[
                    'prophet.a            V      1 1 PRES ACTIVE  IMP 2 S'
                ]
            )
        ])

    def test_get_stem_counts(self):
        stem = Stem(latin="STEM", english="STEMENGLISH")
        stem2 = Stem(latin="STEM2", english="STEM2ENGLISH")
        defined_words = [
            DefinedWord(RawCount("WORD", 3), [
                PossibleStem(stem, ["inflection1", "inflection2"])
            ]),
            DefinedWord(RawCount("WORD2", 4), [
                PossibleStem(stem, ["inflection3", "inflection4"]),
                PossibleStem(stem2, ["inflection5", "inflection6"])
            ]),
            DefinedWord(RawCount("WORD3", 5), [
                PossibleStem(stem2, ["inflection5", "inflection6"])
            ])
        ]
        sort_counts = lambda stem_counts: sorted(
            stem_counts,
            key=attrgetter('stem.latin'))
        self.assertEqual(
            sort_counts(get_stem_counts(defined_words)),
            sort_counts([
                StemCount(stem, defined_words[0:2], 7),
                StemCount(stem2, defined_words[1:3], 9)
            ])
        )
