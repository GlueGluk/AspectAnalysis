import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

file = "markers_filtered_ru_1stage.txt";

filter_parts = [
    "Abbr",
    "Name",
    "Surn",
    "Fixd",
]

fh = open(file)
withBad = []
noBad = []
for line in fh:
    words = re.split(r'\s+', line)
    words = list(filter(lambda x: re.search(r'\S', x), words))
    hasBad = False
    for w in words:
        p = morph.parse(w.decode('utf-8'))[0]
        for part in filter_parts:
            if part in p.tag:
                print(w)
                print(p.tag)
                hasBad = True
                break
        if hasBad:
            break
    if hasBad:
        withBad.append(line)
    else:
        noBad.append(line)

fh.close()

out = open('markers_filtered_ru_bad_tag.txt', 'w')
for line in withBad:
    out.write(line)
out.close()
out = open('markers_filtered_ru_no_bad_tag.txt', 'w')
for line in noBad:
    out.write(line)
out.close()
