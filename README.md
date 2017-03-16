Quick command line wrapper around whittackers words (http://archives.nd.edu/words.html).
We could also try to download the linux version of words, but the link I found
was broken.

Immediate TODO:

 * fix get_definition to handle multiple stems, and multiple inflections per stem. (e.g. propheta, both a noun and a verb, with two possible nouns, and multiple inflections for each noun)
   * fix Definition type to handle multiple inflections and multiple stems
   * fix get_definition to return new type
   * fix get_definition to handle cases where multiple stems share an english definition (propheta and prophetes both have an english definition after prophetes)
   * add test for get_definition.
   * fix other types, as needed.
   * fix run.py. update test and make sure the short text in texts/ provides a useful test case for this
 * test with long output from CLI WW to make sure our definitions aren't getting cut off by the CONTINUE prompt?
 * Switch TOP_X_WORDS to be a parameter, and to apply to stems, not raw words


General Improvements needed:

 * Need to filter out common words as a parameter.
 * build a cache from WW's online list of all inflected forms. That would make things very fast, and if we build the cache in something like YAML, it would allow people like Ryan to edit it or add to it. or at least view it to check on problems.
