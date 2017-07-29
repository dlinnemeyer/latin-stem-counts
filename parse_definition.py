import re
from typing import List
from type_defs import Definition, PossibleStem, Stem, ParsedStem


def _is_match(regex, s):
    return re.fullmatch(regex, s) is not None


def is_inflected_form(s):
    return _is_match('^[a-zA-Z\.]+\s{2,20}[A-Z]{1,8}[a-zA-Z0-9 ]*$', s)


def is_latin_stem(s):
    return _is_match('^[a-zA-Z0-9\.,\-\(\) ]+\s+\[[A-Z]{5}\].*$', s)


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
# multiple possible stems under a single english def, hence the list of
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

        # definition of scriptum has an inflected form after an initial latin
        # stem. I've only seen this right before an english def, so we should
        # be able to break out of the loop in this case
        if len(latin_stem) == 0 and len(pairs):
            key = len(pairs) - 1
            pairs[key] = (pairs[key][0] + inflections, pairs[key][1])
            break

        if len(latin_stem) > 1:
            raise ValueError(
                "Multi-line latin definition found {} in {}".format(
                    latin_stem, chunk))

        # cleanse all the junk now. lots of whitespace from words
        pairs.append((inflections, latin_stem[0] if len(latin_stem) else ""))

    # return all the inflection/latin_stem pairs
    return list(map(lambda pair: PossibleStem(
        stem=Stem(
            latin=pair[1],
            parsed=parse_stem(pair[1]),
            english="\n".join(_chunk)
        ),
        inflections=pair[0]
    ), pairs))


def parse_stem(latin: str) -> ParsedStem:
    # TODO: add conditional parseing based on part of speech to get more info
    # about verbs, nouns, etc.
    m = re.match(r"^(.*)  (\w+) .*$", latin)
    if m is None:
        return ParsedStem(
            part_of_speech=None,
            core_stem=None
        )

    core_stem, part_of_speech = m.groups()
    return ParsedStem(
        part_of_speech=part_of_speech,
        core_stem=core_stem
    )


# exclude 'problem' lines that might be parseable at some point, but we're
# ignoring for now
def is_problem_line(line):
    return any(x in line for x in ['TACKON', 'PACKON']) or line.startswith('-que')


def cleanse_raw_definition(raw_definition: str) -> List[str]:
    return [
        line.strip()
        for line in raw_definition.split("\n")
        if len(line) > 1 and not is_problem_line(line)
    ]


def get_definition(raw_definition: str) -> Definition:
    _def = cleanse_raw_definition(raw_definition)
    possible_stems = []  # type: List[PossibleStem]

    while len(_def) > 0:
        chunk_stems, _def = split_by(
            lambda line: is_inflected_form(line) or is_latin_stem(line),
            _def)
        english_lines, _def = split_by(is_english_line, _def)

        possible_stems += process_definition_chunk(chunk_stems + english_lines)

    return possible_stems
