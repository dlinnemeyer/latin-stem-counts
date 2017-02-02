Quick command line wrapper around whittackers words (http://archives.nd.edu/words.html).
We could also try to download the linux version of words, but the link I found
was broken.

Immediate TODO:

 * fix lookup. we take the first line as the inflected form, but that doesn't work for cases where a given inflected form has multiple possibilties for a single stem (e.g. dei could be nominative plural or genitive singular deus). probably read lines until the first word (with "." removed) no longer equals the raw inflected form? those are the possibilities?
 * switch to stem-based counts. The current code works to get stem for each inflected form. Just create a new counter based on stem. Can store stuff in some global dictionary as we go that sort of acts like our future file-based database.


General Improvements needed:

 * Switch to command line version of WW. try this: https://github.com/mk270/whitakers-words.
   * I got this running locally with dnf install gprbuild gcc-gnat
   * run each line through WW, translating each inflected word into stem + definition and adding to counter. we'll need to clean up output from WW; it's pretty messy.
   * If one line at a time is sluggish, just grab the whole text into memory and remove line endings, since they seem to give WW trouble.
   * WW was giving me some weird line-related errors? Maybe I have some windows line endings mixed into the text? need to check on that and have python translate those. or add a second script for cleanse a file before processing.
 * If slow, cache the inflected word -> stem/definition function. We could just do a file-based database that we keep in version control to accumulate a database of lookups. Should run nice and fast over time.
 * Need to filter out common words as a parameter.
 * The words are counted by their inflected form, not their stem. Need to instead lookup every inflected word, switch to stem, then get word counts by stem.
 * Need to deal with words with multiple possible stems. Not sure how that should be handled for word count. Most likely since we're just dealing with basic top X stems, we can count every match as a full count. This is only meant as an approximation anyway.
