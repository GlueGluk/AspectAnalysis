import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

file = "markers_filtered_ru.txt";

fh = open(file)
withLat = []
noLat = []
for line in fh:
    words = re.split(r'\s+', line)
    words = list(filter(lambda x: re.search(r'\S', x), words))
    hasLat = False
    for w in words:
        p = morph.parse(w.decode('utf-8'))[0]
        print(w)
        print(p.tag)
        if 'LATN' in p.tag:
            hasLat = True
            break
    if hasLat:
        withLat.append(line)
    else:
        noLat.append(line)

fh.close()

out = open('markers_filtered_ru_with_lat.txt', 'w')
for line in withLat:
    out.write(line)
out.close()
out = open('markers_filtered_ru_no_lat.txt', 'w')
for line in noLat:
    out.write(line)
out.close()
