Quick command line wrapper around whittackers words (http://archives.nd.edu/words.html).
We could also try to download the linux version of words, but the link I found
was broken.

Immediate TODO:

 * fix lookup. we take the first line as the inflected form, but that doesn't work for cases where a given inflected form has multiple possibilties for a single stem (e.g. dei could be nominative plural or genitive singular deus). probably read lines until the first word (with "." removed) no longer equals the raw inflected form? those are the possibilities?
 * Switch TOP_X_WORDS to be a parameter, and to apply to stems, not raw words


General Improvements needed:

 * Need to filter out common words as a parameter.
 * build a cache from WW's online list of all inflected forms. That would make things very fast, and if we build the cache in something like YAML, it would allow people like Ryan to edit it or add to it. or at least view it to check on problems.
