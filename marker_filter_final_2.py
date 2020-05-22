# -*- coding: utf-8 -*-
import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

most_frequent = ['быть', 'являться', 'иметь', 'который', 'этот', 'такой', 'один', 'весь', 'тот', 'данный', 'другой', 'следующий', 'первый', 'все', 'некоторый', 'каждый']
file = "markers_filtered_ru_cleared.txt";

fh = open(file)
withOther = []
noOther = []
for line in fh:
    words = re.split(r'\s+', line)
    words = list(filter(lambda x: re.search(r'\S', x), words))
    hasOther = False
    for w in words:
        p = morph.parse(w.decode('utf-8'))[0]
        if w in most_frequent or 'NPRO' in p.tag or 'PREP' in p.tag or 'CONJ' in p.tag or 'PRCL' in p.tag or 'INTJ' in p.tag:
            continue
        else:
            hasOther = True
            break
    if hasOther:
        withOther.append(line)
    else:
        noOther.append(line)

fh.close()

out = open('markers_filtered_ru_meaningful.txt', 'w')
for line in withOther:
    out.write(line)
out.close()
out = open('markers_filtered_ru_meaningless.txt', 'w')
for line in noOther:
    out.write(line)
out.close()
