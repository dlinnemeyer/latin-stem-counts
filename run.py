import sys
from collections import Counter
import string
import urllib.request
import time
from bs4 import BeautifulSoup as Html

TOP_X_WORDS = 20

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

def get_stem(word):
    html = Html(urllib.request.urlopen(
        "http://archives.nd.edu/cgi-bin/wordz.pl?keyword={}".format(word)
    ).read(), 'lxml')
    stem = html.body.h2.a.contents[0]
    info = html.body.pre.contents[0]
    return (stem, info)

def run():
    # TODO: need to get definitions for all words, THEN limit down to most
    # common based on stem.
    for word, count in get_word_counts(sys.stdin):
        print("{} [{} occurrences]".format(word, count))
        stem, info = get_stem(word)
        print("Stem: {}".format(stem))
        print(info)
        time.sleep(1)

if __name__ == '__main__':
    run()
