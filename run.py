#!/usr/bin/python3
import csv
from operator import attrgetter
import sys
from collections import Counter
from typing import Iterable, List, Dict  # NOQA
import string
import subprocess
from parse_definition import get_definition
from type_defs import StemCount, RawCount, DefinedWord, Definition, Stem  # NOQA

TOP_X_WORDS = 30
PATH_TO_WORDS = "/home/dlinnemeyer/whitakers-words"
OUTPUT_FILE = "stuff.csv"


def get_raw_counts(lines: Iterable[str]) -> List[RawCount]:
    words = Counter()  # type: ignore
    for line in map(cleanse, lines):
        words.update(filter(is_valid, line.split(" ")))

    return [
        RawCount(word=word, count=count)
        for word, count in words.items()
    ]


def define_word(raw_count: RawCount) -> DefinedWord:
    return DefinedWord(
        raw_count=raw_count,
        definition=lookup(raw_count.word))


def get_stem_counts(defined_words: List[DefinedWord]) -> List[StemCount]:
    # map latin stems to all the defined words that reference it. A single
    # defined words has multiple possible stems, so it'll go in multiple
    # places potentially. Also, Stems are unhashable, so need a dict mapping
    # stem.latin to defined words, then latin to Stem
    stem_words = {}  # type: Dict[str, List[DefinedWord]]
    stems = {}  # type: Dict[str, Stem]
    for defined_word in defined_words:
        for possible_stem in defined_word.definition:
            latin = possible_stem.stem.latin
            if latin not in stems:
                stem_words[latin] = []
                stems[latin] = possible_stem.stem

            stem_words[latin] += [defined_word]

    return [
        StemCount(
            stem=stems[stem_latin],
            defined_words=defined_words,
            count=sum(map(
                lambda defined_word: defined_word.raw_count.count,
                defined_words
            ))
        )
        for stem_latin, defined_words in stem_words.items()
    ]

def filter_bad_stem_counts(stem_counts: List[StemCount]) -> List[StemCount]:
    return list(filter(
        lambda stem_count: stem_count.stem.latin != "",
        stem_counts))


def print_stem_count(stem_count):
    print("{} {} [forms: {}]".format(
        stem_count.count,
        stem_count.stem.latin,
        ", ".join(map(
            lambda defined_word: defined_word.raw_count.word,
            stem_count.defined_words
        ))
    ))


# this is a flat dict for csv output
def stem_count_to_dict(stem_count):
    return {
        'count': stem_count.count,
        'stem': stem_count.stem.latin,
        'part_of_speech': stem_count.stem.parsed.part_of_speech,
        'definition': stem_count.stem.english,
        'raw_words': ", ".join(map(
            lambda defined_word: defined_word.raw_count.word,
            stem_count.defined_words
        ))
    }

def write_csv(outfile, stem_counts):
    dicts = list(map(stem_count_to_dict, stem_counts))
    writer = csv.DictWriter(outfile, fieldnames=[
        'count', 'stem', 'part_of_speech', 'definition', 'raw_words'
    ])

    writer.writeheader()
    for d in dicts:
        writer.writerow(d)

# this is probably bad, but it's a start
def is_namedtuple(x):
    return hasattr(x, '_asdict')


def cleanse(s):
    return s.translate(
        s.maketrans("", "", string.punctuation + "\n")
    ).strip().lower()


def is_valid(s):
    return s != ''


def lookup(word: str) -> Definition:
    return get_definition(subprocess.getoutput(
        "cd {} && bin/words {}".format(PATH_TO_WORDS, word)
    ))


def run(text: Iterable[str]) -> List[StemCount]:
    raw_counts = get_raw_counts(text)
    defined_words = list(map(define_word, raw_counts))

    raw_stem_counts = get_stem_counts(defined_words)
    stem_counts = filter_bad_stem_counts(raw_stem_counts)

    if len(stem_counts) < len(raw_stem_counts):
        print("Filtered out {} bad stem counts".format(
            len(raw_stem_counts) - len(stem_counts)))

    truncated_stem_counts = sorted(
        stem_counts,
        key=attrgetter('count'),
        reverse=True
    )[:TOP_X_WORDS]

    print("Printing to {}".format(OUTPUT_FILE))
    with open(OUTPUT_FILE, 'w') as f:
        write_csv(f, truncated_stem_counts)

if __name__ == '__main__':
    run(sys.stdin)
