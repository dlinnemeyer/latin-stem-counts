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

idem_definition = """
dem                  TACKON
TACKON w/i-ea-id   idem => same;
i                    PRON   4 2 NOM S M
i                    PRON   4 2 NOM S N
i                    PRON   4 2 ACC S N
idem, eadem, idem  PRON   [XXXAX]
(w/-dem ONLY, idem, eadem, idem) same, the same, the very same, also;

"""

quisque_definition = """
que                  TACKON
PACKON w/qui => whoever it be; whatever; each, each one; everyone, everything;
qu.is                PRON   1 0 DAT P X
qu.is                PRON   1 0 ABL P X
qu  PACK   [XXXAX]
(w/-que) each, each one; every, everybody, everything (more than 2); whatever;
(w/-que) any; each;
qu.is                PRON   1 0 NOM S C
(w/-que) each, each one; every, everybody, everything (more than 2); whatever;
que                  TACKON
-que = and (enclitic, translated before attached word); completes plerus/uter;
qu.is                PRON   1 0 DAT P X
qu.is                PRON   1 0 ABL P X
who; that; which, what; of which kind/degree; person/thing/time/point that;
who/what/which?, what/which one/man/person/thing? what kind/type of?;
who/whatever, everyone who, all that, anything that;
any; anyone/anything, any such; unspecified some; (after si/sin/sive/ne);
who?, which?, what?; what kind of?;
qu.is                PRON   1 0 NOM S C
who/what/which?, what/which one/man/person/thing? what kind/type of?;
anyone/anybody/anything; whoever you pick; something (or other); any (NOM S);
qui.s                V      6 1 PRES ACTIVE  IND 2 S
queo, quire, quivi(ii), quitus  V   [XXXBX]
be able;
que                  TACKON
PACKON w/qui => whoever it be; whatever; each, each one; everyone, everything;
qu.is                PRON   1 0 DAT P X
qu.is                PRON   1 0 ABL P X
qu  PACK   [XXXAX]
(w/-que) each, each one; every, everybody, everything (more than 2); whatever;
(w/-que) any; each;
qu.is                PRON   1 0 NOM S C
(w/-que) each, each one; every, everybody, everything (more than 2); whatever;

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

    def test_idem(self):
        by_line = list(filter(
            lambda line: line != "",
            idem_definition.split("\n")))

        self.assertEqual(get_definition(idem_definition), [
            PossibleStem(
                inflections=by_line[2:5],
                stem=Stem(latin=by_line[5], english=by_line[6])
            )
        ])


    def test_quisque(self):
        by_line = list(filter(
            lambda line: line != "",
            quisque_definition.split("\n")))

        join_eng = lambda lines: "\n".join(lines)

        self.assertEqual(get_definition(quisque_definition), [
            PossibleStem(
                inflections=by_line[2:4],
                stem=Stem(latin=by_line[4], english=join_eng(by_line[5:7]))
            ),
            PossibleStem(
                inflections=[by_line[7]],
                stem=Stem(latin="", english=by_line[8])
            ),
            PossibleStem(
                inflections=by_line[11:13],
                stem=Stem(latin="", english=join_eng(by_line[13:18]))
            ),
            PossibleStem(
                inflections=[by_line[18]],
                stem=Stem(latin="", english=join_eng(by_line[19:21]))
            ),
            PossibleStem(
                inflections=[by_line[21]],
                stem=Stem(latin=by_line[22], english=by_line[23])
            ),
            PossibleStem(
                inflections=by_line[26:28],
                stem=Stem(latin=by_line[28], english=join_eng(by_line[29:31]))
            ),
            PossibleStem(
                inflections=[by_line[31]],
                stem=Stem(latin="", english=by_line[32])
            )
        ])
