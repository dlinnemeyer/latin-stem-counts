import unittest
from parse_definition import is_inflected_form, is_stem, get_definition

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
]

stems = [
    "femur, feminis  N (3rd) N   [XBXBO]",
    "femina, feminae  N (1st) F   [XXXAX]",
    "propheta, prophetae  N (1st) M   [XEXBO]",
    "prophetes, prophetae  N M   [DEXCS]    Late",
    "propheto, prophetare, prophetavi, prophetatus  V (1st)   [EEXCS]    Late",
]

neither = [
    "thigh (human/animal); flat vertical band on triglyph; [~ bubulu => plat]",
    "prophet; spokesman/interpreter of a god; foreteller, soothsayer (L+S);",
    "prophesy, foretell, predict;",
]


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

    def test_is_stem(self):
        for stem in stems:
            self.assertTrue(
                is_stem(stem),
                "{} should be a stem".format(stem))

        for should_not in inflecteds + neither:
            self.assertFalse(
                is_stem(should_not),
                "{} should not be a stem".format(should_not))

    def test_get_definition(self):
        pass
