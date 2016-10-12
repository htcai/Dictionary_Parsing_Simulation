# Simulates the pattern of English homophony via a bigram model built from syllables.

from __future__ import division
import nltk, re, random
from syllabification import *

path_clustered = '/data/cmudict_clustered.txt'


def pick_syll(cfd, prec_syll):
    fd = cfd[prec_syll]
    options = fd.keys()
    current = 0
    space = {}
    for syll in options:
        move_to = current + fd[syll]
        for ind in range(current, move_to):
            space[ind] = syll
        current = move_to
    result = int(random.random() * current)
    pick = space[result]
    return pick


def simulate(cfd, probs, word_count, poss_syll):
    clustered = {}
    generated = []
    for syll_num in range(1,9):
        clustered[syll_num] = {}
    for word in range(word_count):
        init_syll = random.choice(poss_syll)
        syllables = [init_syll]
        prec_syll = init_syll
        for ind in range(2, 9):
            if random.random() < probs[ind-1]:
                break
            else:
                if prec_syll in cfd.keys():
                    syll = pick_syll(cfd, prec_syll)
                else:
                    syll = random.choice(poss_syll)
                syllables.append(syll)
                prec_syll = syll
        phon = ' . '.join(syllables)
        generated.append(phon)
        length = len(syllables)
        cluster = clustered[length]
        if phon in cluster.keys():
            cluster[phon].append(word)
        else:
            cluster[phon] = [word]

    counts = {}
    for syll_num in range(1, 9):
        counts[syll_num] = {}
        cluster = clustered[syll_num]
        phon_form = cluster.keys()
        counts[syll_num]['phon_form'] = len(phon_form)
        words = sum([len(cluster[phon]) for phon in phon_form])
        counts[syll_num]['words'] = words
    return generated


def read_clustered(path_clustered):
    f = open(path_clustered, 'r')
    lines = f.read().split('\n')
    if lines[-1] == '':
        del lines[-1]
    clusters = [tuple(line.split(': ')) for line in lines]
    clusters = [(pron, eval(words)) for pron, words in clusters]
    clustered = dict(clusters)
    return clustered


clustered = read_clustered(path_clustered)
word_dist = {}
homophones = count_homophones(clustered)

for syll_num in range(1, 9):
    counts = homophones[syll_num]
    word_num = counts['pron_num'] + counts['homo_num']
    word_dist[syll_num] = word_num


word_count = sum(word_dist.values())
probs = {}

for syll_num in range(1, 9):
    remain = sum([word_dist[n] for n in range(syll_num, 9)])
    probs[syll_num] = word_dist[syll_num] / remain


path_bigrams = '/data/cmudict_bigrams.txt'


def get_cfd(path_bigrams):
    f = open(path_bigrams, 'r')
    lines = f.read().split('\n')
    if lines[-1] == '':
        del lines[-1]
    bgms = [eval(line) for line in lines if 'WF' not in eval(line)]
    cfd = nltk.ConditionalFreqDist(bgms)
    return cfd

cfd = get_cfd(path_bigrams)
pronunciations = clustered.keys()
poss_syll = possible_syllables(pronunciations)
