Quick command line wrapper around whittackers words (http://archives.nd.edu/words.html).
We could also try to download the linux version of words, but the link I found
was broken.

Immediate TODO:

 * DONE: fix get_definition to handle multiple stems, and multiple inflections per stem. (e.g. propheta, both a noun and a verb, with two possible nouns, and multiple inflections for each noun)
   * DONE: fix Definition type to handle multiple inflections and multiple stems
   * DONE: fix get_definition to return new type
   * DONE: fix get_definition to handle cases where multiple stems share an english definition (propheta and prophetes both have an english definition after prophetes)
   * DONE: add test for get_definition.
   * DONE: fix other types, as needed.
   * DONE: fix run.py. update test and make sure the short text in texts/ provides a useful test case for this
 * DONE: get test passing with idem aliquem quod quidem quisque
   * DONE: make run_short working
   * DONE: add test for -dem or -que words
 * DONE: add csv output
 * DONE: add part of speech to stem and to output
 * cleanup tests and get passing
   * part of speech broke them. just make test_parser ignore parsed part of Stem somehow. it's not relevant to that.
   * add unit tests in test_basics (or maybe parser?) to test parse_stem. We'll want a separate set of tests to know we can convert latin stem text to ParsedStem, which a good handful of examples.
 * remove is_problem_line
   * we should be able to parse whatever WW gives us. at least return some Stem data structure
   * later on, we can remove Stems/Definitions that are missing certain core pieces and emit
     warnings (e.g. if no latin stem, remove; if no inflections and only a stem, remove?)


General Improvements needed:

 * Need to filter out common words as a parameter.
 * build a cache from WW's online list of all inflected forms. That would make things very fast, and if we build the cache in something like YAML, it would allow people like Ryan to edit it or add to it. or at least view it to check on problems.
