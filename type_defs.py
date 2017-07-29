from typing import NamedTuple, List

# NewType these?
Word = str
Count = int
Inflection = str

ParsedStem = NamedTuple('ParsedStem', [
    ('part_of_speech', str),
    ('core_stem', str) # the scribo, scribere part; must be a name for this?
])

Stem = NamedTuple('Stem', [
    ('latin', str),
    ('parsed', ParsedStem),
    ('english', str)
])

RawCount = NamedTuple('RawCount', [
    ('word', Word),
    ('count', Count)
])

PossibleStem = NamedTuple('PossibleStem', [
    ('stem', Stem),
    ('inflections', List[Inflection])
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
