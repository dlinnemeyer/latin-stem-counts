import re
from type_defs import Definition


def _is_match(regex, s):
    return re.fullmatch(regex, s) is not None


def is_inflected_form(s):
    return _is_match("^[a-zA-Z\.]+\s{2,20}[A-Z]+\s{2,8}.*$", s)


def is_stem(s):
    return _is_match("^[a-zA-Z\., ]+\s+[A-Za-z0-9\(\) ]+\s+\[[A-Z]{5}\].*$", s)


def get_definition(definition: str) -> Definition:
    _def = definition.split("\n")
    inflections = [_def[0]]
    stem = "\n".join(_def[1:])
    return Definition(stem, inflections)
