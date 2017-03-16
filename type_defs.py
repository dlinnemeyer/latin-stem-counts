from typing import NamedTuple, List

# NewType these?
Word = str
Count = int
Inflection = str

# just a latin stem line plus a potential multi-line english definition.
# We may broaden the latin portion to be a tuple of its own with grammatical
# info, but this is enough for now
Stem = NamedTuple('Stem', [
    ('latin', str),
    ('english', str)
])

RawCount = NamedTuple('RawCount', [
    ('word', Word),
    ('count', Count)
])

PossibleStem = NamedTuple('PossibleStem', [
    ('inflections', List[Inflection]),
    ('stem', Stem)
])

Definition = List[PossibleStem]

DefinedWord = NamedTuple('DefinedWord', [
    ('raw_count', RawCount),
    ('definition', Definition)
])

StemCount = NamedTuple('StemCount', [
    ('stem', Stem),
    ('defined_words', List[DefinedWord]),
    ('count', Count)
])
