# -*- coding: utf-8 -*-
import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

meaningless = ['я', 'он', 'она', 'ты', 'вы', 'они']
file = "markers_filtered_ru_frequent.txt";

fh = open(file)
withOther = []
noOther = []
for line in fh:
#   глаголы с незначащими или существительное + и
    words = re.split(r'\s+', line)
    words = list(filter(lambda x: re.search(r'\S', x), words))
    isVerb = False
    isUseless = False
    isNoun = False
    isAdj = False
    isAnd = False
    hasOther = False
    for w in words:
        p = morph.parse(w.decode('utf-8'))[0]
        if w == 'и':
            isAnd = True
            continue
        if w in meaningless or 'PREP' in p.tag or 'CONJ' in p.tag or 'PRCL' in p.tag or 'INTJ' in p.tag:
            isUseless = True
            continue
        if 'NOUN' in p.tag:
            if isNoun:
                hasOther = True
                break
            else:
                isNoun = True
                continue
        if 'VERB' in p.tag or 'INFN' in p.tag:
            if isVerb:
                hasOther = True
                break
            else:
                isVerb = True
                continue
        if 'ADJF' in p.tag or 'ADJS' in p.tag or 'COMP' in p.tag:
            isAdj = True
            continue
        else:
            hasOther = True
            break

    if isNoun and (isUseless or isVerb or isAdj or len(words) > 2):
        hasOther = True
    if isVerb and isAdj:
        hasOther = True
    if hasOther:
        withOther.append(line)
    else:
        noOther.append(line)

fh.close()

out = open('markers_filtered_ru_cleared.txt', 'w')
for line in withOther:
    out.write(line)
out.close()
out = open('markers_filtered_ru_removed.txt', 'w')
for line in noOther:
    out.write(line)
out.close()
