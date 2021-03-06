# Dictionary Parsing and Simulation for the Project of Language Optimality and Evolution#

This project aims to provide evidence against the claim of [Piantadosi et al. 2012](http://www.sciencedirect.com/science/article/pii/S0010027711002496), by showing that the pattern of homophony (i.e., repeated usage of a phonological form for different words) can be replicated via a random process. This random simulation only takes into account the co-occurrence information of adjacent syllables in words.

This repository contains Python scripts that are produced to perform the following tasks. Detailed code comments will be added soon.

* `syllabification.py`: Parses the pronunciations (i.e., phonological forms) of words into syllables, following the principle of maximzing the cluster of onset consonants of each syllable.
* `simulate_homophony_by_syllables`: Simulates the pattern of homophony of English via a randomized bigram model constructed from syllables.


The `data` folder contains the results of parsing the CMU Pronunciation Dictionary and of the random word generation.

* `cmudict_onset`: The (short) list of possible onsets that are legitimate, which was manually checked by Aletheia Cui and Ava Irani.
* `cmudict_syllabified`: The phonological forms that are syllabified.
* `cmudict_nostress.txt`: Same as `cmudict_syllabified` except that stress markers were removed.
* `cmudict_clustered.txt`: Words are clustered by their phonological forms.
* `cmudict_stems.txt`: Same as `cmudict_nostress.txt` except that all inflected forms of words were removed.
* `generated_words.txt`: The list of synthetic phonological forms that are randomly generated in the simulation.
* `homophony_count.txt`: The countings of pronunciation types and tokens, which are close to the actual pattern of English.
