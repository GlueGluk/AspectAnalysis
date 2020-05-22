import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

file = "markers_filtered_ru_known.txt";

fh = open(file)
withN = []
noN = []
for line in fh:
    words = re.split(r'\s+', line)
    hasNum = False
    for w in words:
        p = morph.parse(w.decode('utf-8'))[0]
        if 'NUMR' in p.tag:
            hasNum = True
            break
    if hasNum:
        withN.append(line)
    else:
        noN.append(line)

fh.close()

out = open('markers_filtered_with_number.txt', 'w')
for line in withN:
    out.write(line)
out.close()
out = open('markers_filtered_no_number.txt', 'w')
for line in noN:
    out.write(line)
out.close()
