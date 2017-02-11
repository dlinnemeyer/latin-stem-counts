from typing import NamedTuple, List

# NewType these?
Word = str
Count = int
Stem = str
Inflection = str

RawCount = NamedTuple('RawCount', [
    ('word', Word),
    ('count', Count)
])

Definition = NamedTuple('Definition', [
    ('stem', Stem),
    ('inflections', List[Inflection])
])

DefinedWord = NamedTuple('DefinedWord', [
    ('raw_count', RawCount),
    ('definition', Definition)
])

StemCount = NamedTuple('StemCount', [
    ('stem', Stem),
    ('defined_words', List[DefinedWord]),
    ('count', Count)
])
