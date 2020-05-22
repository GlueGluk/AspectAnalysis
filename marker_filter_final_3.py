# -*- coding: utf-8 -*-
import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

meaningless = ['я', 'он', 'она', 'ты', 'вы', 'они']
file = "markers_filtered_ru_meaningful.txt";

fh = open(file)
withOther = []
noOther = []
for line in fh:
#   глаголы с незначащими или существительное + и
    words = re.split(r'\s+', line)
    words = list(filter(lambda x: re.search(r'\S', x), words))
    isNoun = False
    hasOther = False
    for w in words:
        p = morph.parse(w.decode('utf-8'))[0]
        if w in meaningless or 'PREP' in p.tag or 'CONJ' in p.tag or 'PRCL' in p.tag or 'INTJ' in p.tag:
            continue
        if 'NOUN' in p.tag:
            if isNoun:
                hasOther = True
                break
            else:
                isNoun = True
                continue
        else:
            hasOther = True
            break

    if hasOther:
        withOther.append(line)
    else:
        noOther.append(line)

fh.close()

out = open('markers_filtered_ru_cleared2.txt', 'w')
for line in withOther:
    out.write(line)
out.close()
out = open('markers_filtered_ru_removed2.txt', 'w')
for line in noOther:
    out.write(line)
out.close()
