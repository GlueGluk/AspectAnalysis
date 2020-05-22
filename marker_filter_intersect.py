import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

hand_markers = []
fh = open("hand_collected_markers")
for line in fh:
    line = line.rstrip('\n')
    hand_markers.append(line)

file = "markers_found_no_extra.txt";

fh = open(file)
inters = []
nointers = []
for line in fh:
    line = line.rstrip('\n')
    match = False
    for mar in hand_markers:
        if mar == line:
            match = True
            break
    if match:
        inters.append(line)
    else:
        nointers.append(line)
fh.close()

out = open('markers_filtered_intersect.txt', 'w')
for line in inters:
    out.write(line+"\n")
out.close()
out = open('markers_filtered_no_intersect.txt', 'w')
for line in nointers:
    out.write(line+"\n")
out.close()
