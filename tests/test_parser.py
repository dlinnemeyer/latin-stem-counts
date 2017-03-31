import unittest
from parse_definition import is_inflected_form, is_latin_stem, get_definition
from type_defs import Stem, PossibleStem

inflecteds = [
    "femin.a              ADJ    1 1 NOM S F POS",
    "femin.a              ADJ    1 1 VOC S F POS",
    "femin.a              ADJ    1 1 ABL S F POS",
    "femin.a              ADJ    1 1 NOM P N POS",
    "femin.a              ADJ    1 1 VOC P N POS",
    "femin.a              ADJ    1 1 ACC P N POS",
    "prophet.a            N      1 1 NOM S M",
    "prophet.a            N      1 1 VOC S M",
    "prophet.a            N      1 1 ABL S M",
    "prophet.a            N      1 7 VOC S M",
    "prophet.a            N      1 7 ABL S M",
    "prophet.a            V      1 1 PRES ACTIVE  IMP 2 S",
    "sicut                ADV    POS  ",
    "sicut                CONJ",
    "script.um            SUPINE 3 1 ACC S N"
]

stems = [
    "femur, feminis  N (3rd) N   [XBXBO]",
    "femina, feminae  N (1st) F   [XXXAX]",
    "propheta, prophetae  N (1st) M   [XEXBO]",
    "prophetes, prophetae  N M   [DEXCS]    Late",
    "propheto, prophetare, prophetavi, prophetatus  V (1st)   [EEXCS]    Late",
    "edo, esse, -, -  V TRANS   [XXXCO]",
    "sicut  ADV   [XXXAX]",
    "scribo, scribere, scripsi, scriptus  V (3rd)   [XXXAX]",
]

neither = [
    "thigh (human/animal); flat vertical band on triglyph; [~ bubulu => plat]",
    "prophet; spokesman/interpreter of a god; foreteller, soothsayer (L+S);",
    "prophesy, foretell, predict;",
]

propheta_definition = """
prophet.a            N      1 1 NOM S M
prophet.a            N      1 1 VOC S M
prophet.a            N      1 1 ABL S M
propheta, prophetae  N (1st) M   [XEXBO]
prophet.a            N      1 7 VOC S M
prophet.a            N      1 7 ABL S M
prophetes, prophetae  N M   [DEXCS]    Late
prophet; spokesman/interpreter of a god; foreteller, soothsayer (L+S);
prophet.a            V      1 1 PRES ACTIVE  IMP 2 S
propheto, prophetare, prophetavi, prophetatus  V (1st)   [EEXCS]    Later
prophesy, foretell, predict;

"""

est_definition = """
es.t                 V      7 3 PRES ACTIVE  IND 3 S      Early
edo, esse, -, -  V TRANS   [XXXCO]
eat/consume/devour; eat away (fire/water/disease); destroy; spend money on food
.est                 V      5 1 PRES ACTIVE  IND 3 S
sum, esse, fui, futurus  V   [XXXAX]
be; exist; (also used to form verb perfect passive tenses) with NOM PERF PPL

"""

scriptum_definition = """
script.um            VPAR   3 1 NOM S N PERF PASSIVE PPL
script.um            VPAR   3 1 VOC S N PERF PASSIVE PPL
script.um            VPAR   3 1 ACC S M PERF PASSIVE PPL
script.um            VPAR   3 1 ACC S N PERF PASSIVE PPL
scribo, scribere, scripsi, scriptus  V (3rd)   [XXXAX]
script.um            SUPINE 3 1 ACC S N
write; compose;
script.um            N      2 2 NOM S N
script.um            N      2 2 VOC S N
script.um            N      2 2 ACC S N
scriptum, scripti  N (2nd) N   [XXXDX]    lesser
something written; written communication; literary work;
script.um            N      4 1 ACC S M
scriptus, scriptus  N (4th) M   [XXXDS]    lesser
scribe's office; being a clerk;
*
"""

class TestParser(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_is_inflected_form(self):
        for inflected in inflecteds:
            self.assertTrue(
                is_inflected_form(inflected),
                "{} should be an inflected form".format(inflected))

        for should_not in stems + neither:
            self.assertFalse(
                is_inflected_form(should_not),
                "{} should not be an inflected form".format(should_not))

    def test_is_latin_stem(self):
        for stem in stems:
            self.assertTrue(
                is_latin_stem(stem),
                "{} should be a stem".format(stem))

        for should_not in inflecteds + neither:
            self.assertFalse(
                is_latin_stem(should_not),
                "{} should not be a stem".format(should_not))

    def test_propheta(self):
        by_line = list(filter(
            lambda line: line != "",
            propheta_definition.split("\n")))

        self.assertEqual(get_definition(propheta_definition), [
            PossibleStem(
                inflections=by_line[:3],
                stem=Stem(latin=by_line[3], english=by_line[7])
            ),
            PossibleStem(
                inflections=by_line[4:6],
                stem=Stem(latin=by_line[6], english=by_line[7])
            ),
            PossibleStem(
                inflections=[by_line[8]],
                stem=Stem(latin=by_line[9], english=by_line[10])
            )
        ])

    def test_est(self):
        by_line = list(filter(
            lambda line: line != "",
            est_definition.split("\n")))

        self.assertEqual(get_definition(est_definition), [
            PossibleStem(
                inflections=by_line[:1],
                stem=Stem(latin=by_line[1], english=by_line[2])
            ),
            PossibleStem(
                inflections=by_line[3:4],
                stem=Stem(latin=by_line[4], english=by_line[5])
            )
        ])

    def test_scriptum(self):
        by_line = list(filter(
            lambda line: line != "",
            scriptum_definition.split("\n")))

        self.assertEqual(get_definition(scriptum_definition), [
            PossibleStem(
                inflections=by_line[:4] + [by_line[5]],
                stem=Stem(latin=by_line[4], english=by_line[6])
            ),
            PossibleStem(
                inflections=by_line[7:10],
                stem=Stem(latin=by_line[10], english=by_line[11])
            ),
            PossibleStem(
                inflections=[by_line[12]],
                stem=Stem(latin=by_line[13], english=by_line[14])
            )
        ])
