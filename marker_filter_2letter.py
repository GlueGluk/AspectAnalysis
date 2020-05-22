import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

file = "markers_filtered_ru_no_lat2.txt";

fh = open(file)
withN2l = []
noN2l = []
for line in fh:
    print(line)
    words = re.split(r'\s+', line)
    words = list(filter(lambda x: re.search(r'\S', x), words))
    hasN2l = False
    for w in words:
        if len(w.decode('utf8')) > 2:
            hasN2l = True
            break
    if hasN2l:
        withN2l.append(line)
    else:
        noN2l.append(line)
fh.close()

out = open('markers_filtered_ru_less_2_letter.txt', 'w')
for line in noN2l:
    out.write(line)
out.close()
out = open('markers_filtered_ru_more_2_letter.txt', 'w')
for line in withN2l:
    out.write(line)
out.close()
