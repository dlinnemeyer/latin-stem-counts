Quick command line wrapper around whittackers words (http://archives.nd.edu/words.html).
We could also try to download the linux version of words, but the link I found
was broken.


Improvements needed:

 * Switch to command line version of WW. try this: https://github.com/mk270/whitakers-words
 * Cache the inflected word -> stem/definition function. We could just do a file-based database that we keep in version control to accumulate a database of lookups. Should run nice and fast over time.
 * Need to filter out common words as a parameter.
 * The words are counted by their inflected form, not their stem. Need to instead lookup every inflected word, switch to stem, then get word counts by stem.
 * Need to deal with words with multiple possible stems. Not sure how that should be handled for word count. Most likely since we're just dealing with basic top X stems, we can count every match as a full count. This is only meant as an approximation anyway.
