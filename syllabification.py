# Collect possible syllables of a language

import nltk, re
from collections import defaultdict

entries = nltk.corpus.cmudict.entries()
entries = [(w, p) for w, p in entries if re.search(r'[AEIOU]', ' '.join(p))]
path_onsets = '/data/cmudict_onsets.txt'
f_onsets = open(path_onsets, 'r')
onsets = f_onsets.read().split('\n')
if onsets[-1] == '':
    del onsets[-1]
possible_onsets = [onset.split(' ') for onset in onsets]
porter = nltk.PorterStemmer()


def get_onsets(entries):
    onsets = []
    for word, pron in entries:
        onset = []
        for i in range(len(pron)):
            cur = pron[i]
            if not re.search(r'[0-9]', cur):
                onset.append(cur)
            else:
                break
        if onset not in onsets:
            onsets.append(onset)
    return onsets


def deduct_list(lst, to_remove):
    result = [item for item in lst if item not in to_remove]
    return result


def remove_digit(string):
    result = ''
    for symbol in string:
        if not symbol.isdigit():
            result += symbol
    return result
    

def get_syllables(pron):
    remain_indices = range(len(pron))
    nuclei = [i for i in remain_indices if re.search(r'[AEIOU]', pron[i])]
    syllables = [(nucleus, [pron[nucleus]]) for nucleus in nuclei]
    syllables = dict(syllables)
    remain_indices = deduct_list(remain_indices, nuclei)
    for nucleus in nuclei:
        syll = syllables[nucleus]
        current = nucleus
        onset = []
        while current - 1 in remain_indices:
            current -= 1
            consonant = pron[current]
            cluster = [consonant] + onset
            if cluster in possible_onsets:
                onset = cluster
                remain_indices.remove(current)
            else:
                break
        syllables[nucleus] = onset + syll
    coda = []
    for nucleus in nuclei:
        syll = syllables[nucleus]
        current = nucleus
        while current + 1 in remain_indices:
            current += 1
            syll.append(pron[current])
            remain_indices.remove(current)
        syllables[nucleus] = syll
    if remain_indices:
        rem = [pron[i] for i in remain_indices]
        syllables[nuclei[0]] = rem + syllables[nuclei[0]]
    result = [syllables[nucleus] for nucleus in nuclei]
    return result


def syllabify(entries):
    res = []
    for w, p in entries:
        if re.search(r'[AEIOU]', ' '.join(p)):
            sylls = get_syllables(p)
            sylls = [' '.join(comps) for comps in sylls]
            pron = ' . '.join(sylls)
            res.append((w, pron))
    return res


def cluster_words(entries):
    clustered = defaultdict(list)
    for word, pron in entries:
        syllables = get_syllables(pron)
        pron = [' '.join(syll) for syll in syllables]
        pron = ' . '.join(pron)
        clustered[pron].append(word)
    return clustered


def retrieve_syllables(string):
    pron = string.split(' . ')
    syllables = [remove_digit(syll) for syll in pron]
    return syllables


def remove_stress(clustered):
    result = {}
    pronunciations = [pron for pron in clustered.keys() if len(pron) > 0]
    for pron in pronunciations:
        basic_pron = remove_digit(pron)
        if basic_pron not in result.keys():
            result[basic_pron] = clustered[pron]
        else:
            result[basic_pron] += clustered[pron]
    return result


def count_homophones(clustered):
    counts = {}
    for syll_num in range(20):
        counts[syll_num] = {'pron_num': 0, 'homo_num': 0}
    for pron in clustered.keys():
        syllables = pron.split(' . ')
        syll_num = len(syllables)
        counts[syll_num]['pron_num'] += 1
        words = clustered[pron]
        additionals = len(words) - 1
        if additionals > 0:
            counts[syll_num]['homo_num'] += additionals
    return counts


def inflected(word):
    return word != porter.stem(word) or "'" in word or "-" in word or ' ' in word


def remove_infl(clustered):
    result = {}
    pronunciations = clustered.keys()
    pronunciations.sort()
    for pron in pronunciations:
        words = clustered[pron]
        non_inflected = []
        for word in words:
            if not inflected(word):
                non_inflected.append(word)
        if non_inflected != []:
            result[pron] = non_inflected
    return result


def read_dict(path_dict):
    f = open(path_dict, 'r')
    lines = f.read().split('\n')
    del lines[-1]
    clusters = [line.split(': ') for line in lines]
    clusters = [[line[0], eval(line[1])] for line in clusters]
    dict_stem = dict(clusters)

    return dict_stem


def unusualOnsets(entries):
    res = []
    for w, p in entries:
        if re.search(r'[AEIOU]', ' '.join(p)):
            for i in xrange(len(p)):
                if re.search(r'[AEIOU]', p[i]):
                    break
            if p[:i] != [] and p[:i] not in possible_onsets:
                res.append((w, p))
    return res
        

def noStress(entries):
    res = []
    for w, p in entries:
        pron = get_syllables(p)
        pron = [' '.join(syll) for syll in pron]
        pron = ' . '.join(pron)
        noS = ''
        for s in pron:
            if not s.isdigit():
                noS += s
        res.append((w, noS))
    return res

def possible_syllables(pronunciations):
    poss_sylls = []
    for pron in pronunciations:
        pron = pron.split(' . ')
        for syll in pron:
            #syll = remove_digit(syll)
            if syll not in poss_sylls:
                poss_sylls.append(syll)
    return poss_sylls
