import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

file = "markers_filtered_ru_1stage.txt";

fh = open(file)
withVerb = {}
verbs = []
noVerb = []
for line in fh:
    words = re.split(r'\s+', line)
    words = list(filter(lambda x: re.search(r'\S', x), words))
    hasVerb = False
    for w in words:
        p = morph.parse(w.decode('utf-8'))[0]
        if 'VERB' in p.tag or 'INFN' in p.tag:
            print(w)
            hasVerb = True
            if withVerb.get(w):
                withVerb[w].append(line)
            else:
                verbs.append(w)
                withVerb[w] = [line]
            break
    if not hasVerb:
        noVerb.append(line)

fh.close()

verbs.sort()
out = open('markers_filtered_ru_with_verb_classif.txt', 'w')
out2 = open('filter_found_verbs.txt', 'w')
for verb in verbs:
    out2.write(verb+"\n")
    out.write("\n---\n"+verb+":\n")
    for line in withVerb[verb]:
        out.write(line)
out.close()
out2.close()
out = open('markers_filtered_ru_no_verb_classif.txt', 'w')
for line in noVerb:
    out.write(line)
out.close()
