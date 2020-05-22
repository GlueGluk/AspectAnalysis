import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

hand_marker_words = {}
fh = open("hand_collected_markers")
for line in fh:
    line = line.rstrip('\n')
    words = re.split(r'\s+', line)
    words = list(filter(lambda x: re.search(r'\S', x), words))
    for w in words:
        p = morph.parse(w.decode('utf-8'))[0]
        if 'VERB' in p.tag or 'INFN' in p.tag or 'NOUN' in p.tag or 'ADJF' in p.tag or 'ADJS' in p.tag:
            hand_marker_words[w] = True

file = "1.2_markers_filtered_no_verb.txt";
fh = open(file)
withHand = []
noHand = []
for line in fh:
    line = line.rstrip('\n')
    match = False
    for w in hand_marker_words:
        if re.search(r'\b'+w.decode('utf-8')+r'\b', line.decode('utf-8'), re.U):
            match = True
            print(w)
            break
    if match:
        withHand.append(line)
    else:
        noHand.append(line)
fh.close()

out = open('2.3_markers_filtered_ru_with_hand.txt', 'w')
for line in withHand:
    out.write(line+"\n")
out.close()
out = open('2.4_markers_filtered_ru_no_hand.txt', 'w')
for line in noHand:
    out.write(line+"\n")
out.close()
