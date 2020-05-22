import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

file = "markers_filtered_ru_1stage.txt";

fh = open(file)
withAdj = {}
adjs = []
noAdj = []
for line in fh:
    words = re.split(r'\s+', line)
    words = list(filter(lambda x: re.search(r'\S', x), words))
    hasAdj = False
    for w in words:
        p = morph.parse(w.decode('utf-8'))[0]
        if 'ADJF' in p.tag or 'ADJS' in p.tag:
            print(w)
            hasAdj = True
            if withAdj.get(w):
                withAdj[w].append(line)
            else:
                adjs.append(w)
                withAdj[w] = [line]
            break
    if not hasAdj:
        noAdj.append(line)

fh.close()

adjs.sort()
out = open('markers_filtered_ru_with_adj_classif.txt', 'w')
out2 = open('filter_found_adjs.txt', 'w')
for adj in adjs:
    out2.write(adj+"\n")
    out.write("\n---\n"+adj+":\n")
    for line in withAdj[adj]:
        out.write(line)
out.close()
out2.close()
out = open('markers_filtered_ru_no_adj_classif.txt', 'w')
for line in noAdj:
    out.write(line)
out.close()
