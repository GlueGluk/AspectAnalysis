import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

file = "markers_filtered_ru_no_lat.txt";

fh = open(file)
withLat = []
noLat = []
for line in fh:
    if re.search(r'[a-zA-Z]', line.decode('utf-8'), re.U):
        withLat.append(line)
    else:
        noLat.append(line)

fh.close()

out = open('markers_filtered_ru_with_lat2.txt', 'w')
for line in withLat:
    out.write(line)
out.close()
out = open('markers_filtered_ru_no_lat2.txt', 'w')
for line in noLat:
    out.write(line)
out.close()
