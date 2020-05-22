import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

file = "markers_filtered_ru_no_lat2.txt";

fh = open(file)
withPOS = []
noPOS = []
for line in fh:
    words = re.split(r'\s+', line)
    words = list(filter(lambda x: re.search(r'\S', x), words))
    hasPOS = False
    for w in words:
        p = morph.parse(w.decode('utf-8'))[0]
        print(w)
        print(p.tag)
        if 'VERB' in p.tag or 'INFN' in p.tag or 'NOUN' in p.tag or 'ADJF' in p.tag or 'ADJS' in p.tag or 'PRTF' in p.tag or 'PRTS' in p.tag:
            hasPOS = True
            break
    if hasPOS:
        withPOS.append(line)
    else:
        noPOS.append(line)

fh.close()

out = open('markers_filtered_ru_with_pos.txt', 'w')
for line in withPOS:
    out.write(line)
out.close()
out = open('markers_filtered_ru_no_pos.txt', 'w')
for line in noPOS:
    out.write(line)
out.close()
