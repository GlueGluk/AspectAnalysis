# -*- coding: utf-8 -*-
import re
import os
wordbreak = r'(^|$|[\s\.,\?!"«»\-])'

files_dir = './learn_dir/'
files = os.listdir(files_dir)
marker_file = "markers_filtered_ru_1stage.txt"
REMOVE_PERCENT = 10

adj_file = "filter_found_adjs.txt";
adjs = {}
fh = open(adj_file)
for line in fh:
    parts = re.split(r'\s+', line)
    adjs[parts[0]] = {
        'count': 0,
        'files': [],
    }
fh.close()
noun_file = "filter_found_nouns.txt";
nouns = {}
fh = open(noun_file)
for line in fh:
    parts = re.split(r'\s+', line)
    nouns[parts[0]] = {
        'count': 0,
        'files': [],
    }
fh.close()

count = 0
for file in files:
    count += 1
    print(str(count)+"/"+str(len(files))+" "+file)
    cont = ""
    if os.path.isfile(files_dir+file):
        fh = open(files_dir+file)
        cont = fh.read()
        fh.close()
    if not len(cont):
        continue

    cont = cont.decode('utf-8')
    words = re.split(wordbreak+'+', cont, 0, re.U)
    words = list(map(lambda x: x.encode('utf-8'), words))
    for w in words:
        if adjs.get(w):
            adjs[w]['count'] = adjs[w]['count'] + 1
            if not file in adjs[w]['files']:
                adjs[w]['files'].append(file)
        if nouns.get(w):
            nouns[w]['count'] = nouns[w]['count'] + 1
            if not file in nouns[w]['files']:
                nouns[w]['files'].append(file)

out = open('remove_nouns.txt', 'w')
remove_words = []
for k in adjs:
    if (len(adjs[k]['files'])*100/len(files)) < REMOVE_PERCENT:
        remove_words.append(k)
for k in nouns:
    if (len(nouns[k]['files'])*100/len(files)) < REMOVE_PERCENT:
        remove_words.append(k)
        out.write(k+"\n")
out.close()

out1 = open('markers_filtered_ru_frequent.txt', 'w')
out2 = open('markers_filtered_ru_unfrequent.txt', 'w')
fh = open(marker_file)
for line in fh:
    good = True
    for w in remove_words:
        if re.search(r'\b'+w.decode('utf-8')+r'\b', line.decode('utf-8'), re.U):
            good = False
            break
    if good:
        out1.write(line)
    else:
        out2.write(line)
fh.close()
out1.close()
out2.close()
