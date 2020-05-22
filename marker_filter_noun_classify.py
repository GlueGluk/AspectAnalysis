import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

file = "markers_filtered_ru_1stage.txt";

fh = open(file)
withNoun = {}
nouns = []
noNoun = []
for line in fh:
    words = re.split(r'\s+', line)
    words = list(filter(lambda x: re.search(r'\S', x), words))
    hasNoun = False
    for w in words:
        p = morph.parse(w.decode('utf-8'))[0]
        if 'NOUN' in p.tag:
            print(w)
            hasNoun = True
            if withNoun.get(w):
                withNoun[w].append(line)
            else:
                nouns.append(w)
                withNoun[w] = [line]
            break
    if not hasNoun:
        noNoun.append(line)

fh.close()

nouns.sort()
out = open('markers_filtered_ru_with_noun_classif.txt', 'w')
out2 = open('filter_found_nouns.txt', 'w')
for noun in nouns:
    out2.write(noun+"\n")
    out.write("\n---\n"+noun+":\n")
    for line in withNoun[noun]:
        out.write(line)
out.close()
out2.close()
out = open('markers_filtered_ru_no_noun_classif.txt', 'w')
for line in noNoun:
    out.write(line)
out.close()
