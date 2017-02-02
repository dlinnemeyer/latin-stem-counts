#!/usr/bin/python3

import sys
from collections import Counter
import string
import urllib.request
import time
from bs4 import BeautifulSoup as Html
import subprocess

TOP_X_WORDS = 20
PATH_TO_WORDS = "/home/dlinnemeyer/whitakers-words"

def cleanse(s):
    return s.translate(
        s.maketrans("", "", string.punctuation + "\n")
    ).strip().lower()

def is_valid(s):
    return s != ''

def get_word_counts(lines):
    words = Counter()
    for line in map(cleanse, lines):
        words.update(filter(is_valid, line.split(" ")))

    return words.most_common(TOP_X_WORDS)

def lookup(word):
    definition = subprocess.getoutput(
        "cd {} && bin/words {}".format(PATH_TO_WORDS, word)
    ).split("\n")
    inflected = definition[0]
    stem = "\n".join(definition[1:])
    return (inflected, stem)

def run():
    # TODO: need to get definitions for all words, THEN limit down to most
    # common based on stem.
    for word, count in get_word_counts(sys.stdin):
        print("{} [{} occurrences]".format(word, count))
        inflected, stem = lookup(word)
        print("Inflected Info: {}".format(inflected))
        print("Stem: {}".format(stem))

if __name__ == '__main__':
    run()
