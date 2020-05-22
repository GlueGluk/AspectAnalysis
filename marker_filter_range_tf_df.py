# -*- coding: utf-8 -*-
import re
import os
import csv
wordbreak = r'(^|$|[\s\.,\?!"«»\-])'

files_dir = './learn_dir/'
files = os.listdir(files_dir)

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
verb_file = "filter_found_verbs.txt";
verbs = {}
fh = open(verb_file)
for line in fh:
    parts = re.split(r'\s+', line)
    verbs[parts[0]] = {
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
        if verbs.get(w):
            verbs[w]['count'] = verbs[w]['count'] + 1
            if not file in verbs[w]['files']:
                verbs[w]['files'].append(file)

out = open('filter_adjs_ranged_tf_df.csv', 'w')
data = [['tf', 'df', 'tf*df', 'слово']]
for k in adjs:
    data.append([adjs[k]['count'], len(adjs[k]['files']), adjs[k]['count']*len(adjs[k]['files']), k])
writer = csv.writer(out)
writer.writerows(data)
out.close()
out = open('filter_nouns_ranged_tf_df.csv', 'w')
data = [['tf', 'df', 'tf*df', 'слово']]
for k in nouns:
    data.append([nouns[k]['count'], len(nouns[k]['files']), nouns[k]['count']*len(nouns[k]['files']), k])
writer = csv.writer(out)
writer.writerows(data)
out.close()
out = open('filter_verbs_ranged_tf_df.csv', 'w')
data = [['tf', 'df', 'tf*df', 'слово']]
for k in verbs:
    data.append([verbs[k]['count'], len(verbs[k]['files']), verbs[k]['count']*len(verbs[k]['files']), k])
writer = csv.writer(out)
writer.writerows(data)
out.close()
