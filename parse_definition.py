import re
from typing import List
from type_defs import Definition, PossibleStem, Stem


def _is_match(regex, s):
    return re.fullmatch(regex, s) is not None


def is_inflected_form(s):
    return _is_match("^[a-zA-Z\.]+\s{2,20}[A-Z]+\s{2,8}.*$", s)


def is_latin_stem(s):
    return _is_match("^[a-zA-Z\., ]+\s+[A-Za-z0-9\(\) ]+\s+\[[A-Z]{5}\].*$", s)


def is_english_line(s):
    return (is_inflected_form(s) or is_latin_stem(s)) is False

# imitating funcy's split_by. we'll pull the whole library in if we need it,
# but I didn't want to for just one function, especially since it leaves me
# with some iterator-rangling to do list len checks.
def split_by(pred, seq):
    matches = []
    for x in seq:
        if pred(x):
            matches.append(x)
        else:
            break

    return (matches, seq[len(matches):])


# definition chunks are basically WW output, split by english defs. This groups
# multiple possible stems under a single english def, hend the list of
# possible stems as the return value (e.g. propheta's first two noun entries
# as an example of multiple stems with the same english definition)
def process_definition_chunk(chunk: List[str]) -> List[PossibleStem]:
    _chunk = chunk
    pairs = []
    while not is_english_line(_chunk[0]):
        inflections, _chunk = split_by(is_inflected_form, _chunk)
        latin_stem, _chunk = split_by(is_latin_stem, _chunk)

        if len(inflections) == 0:
            raise ValueError("found no inflections for {}".format(_chunk))

        if len(latin_stem) == 0:
            raise ValueError("latin_stem definition missing after {}".format(
                inflections))

        if len(latin_stem) > 1:
            raise ValueError(
                "Multi-line latin definition found {} in {}".format(
                    latin_stem, chunk))

        pairs.append((inflections, latin_stem[0]))

    # return all the inflection/latin_stem pairs
    return map(lambda pair: PossibleStem(
        stem=Stem(latin=pair[1], english="\n".join(_chunk)),
        inflections=pair[0]
    ), pairs)


def get_definition(raw_definition: str) -> Definition:
    _def = list(filter(lambda line: line != "", raw_definition.split("\n")))
    possible_stems = []

    while len(_def) > 0:
        chunk_stems, _def = split_by(
            lambda line: is_inflected_form(line) or is_latin_stem(line),
            _def)
        english_lines, _def = split_by(is_english_line, _def)

        possible_stems += process_definition_chunk(chunk_stems + english_lines)

    return possible_stems
