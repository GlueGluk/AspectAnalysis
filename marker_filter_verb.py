import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

file = "markers_filtered_ru_known.txt";

fh = open(file)
withV = []
noV = []
for line in fh:
    words = re.split(r'\s+', line)
    hasVerb = False
    for w in words:
        p = morph.parse(w.decode('utf-8'))[0]
        if 'VERB' in p.tag or 'INFN' in p.tag:
            hasVerb = True
            break
    if hasVerb:
        withV.append(line)
    else:
        noV.append(line)

fh.close()

out = open('1.1_markers_filtered_with_verb.txt', 'w')
for line in withV:
    out.write(line)
out.close()
out = open('1.2_markers_filtered_no_verb.txt', 'w')
for line in noV:
    out.write(line)
out.close()
