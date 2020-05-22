import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

file = "markers_filtered_ru_with_pos.txt";

fh = open(file)
known = []
unknown = []
for line in fh:
    words = re.split(r'\s+', line)
    words = list(filter(lambda x: re.search(r'\S', x), words))
    unkn = False
    for w in words:
        p = morph.parse(w.decode('utf-8'))[0]
        for elem in p.methods_stack:
            if type(elem[0]) != pymorphy2.units.by_lookup.DictionaryAnalyzer:
                print(w)
                print(type(elem[0]))
                unkn = True
                break
        if unkn:
            break
    if unkn:
        unknown.append(line)
    else:
        known.append(line)

fh.close()

out = open('markers_filtered_ru_known.txt', 'w')
for line in known:
    out.write(line)
out.close()
out = open('markers_filtered_ru_unknown.txt', 'w')
for line in unknown:
    out.write(line)
out.close()
