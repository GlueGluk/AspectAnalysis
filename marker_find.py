# -*- coding: utf-8 -*-
from __future__ import division
import os
import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

files_dir = './learn_dir/'
files = os.listdir(files_dir)
regex = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".decode('utf-8')

MAX_LEN = 5
MIN_FILES = 1
MIN_COUNT = 3
ngramm_dict = {}
count = 0

wordbreak = r'(^|$|[\s\.,\?!"«»\-])'
not_wb = r'[^\s\.,\?!"«»\-]'

# Собираем список ngramm
# Считаем, что тексты уже лемматизированы
# Шаг 1-2
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
    words = list(filter(lambda x: bool(re.search("[A-Za-z]", x)) or bool(re.search("["+regex+"]", x.decode('utf-8'))), words))

    for i in range (len(words)):
        for l in range(2, (MAX_LEN+1)):
            if i+l < len(words):
                ngram = " ".join(words[i:i+l])
                if not (ngramm_dict.get(ngram)):
                    ngramm_dict[ngram] = {
                        'total': 1,
                        'files': [count],
                    }
                else:
                    ngramm_dict[ngram]['total'] += 1
                    if not count in ngramm_dict[ngram]['files']:
                        ngramm_dict[ngram]['files'].append(count)

# Фильтруем полученное
iter_dict = ngramm_dict.copy()
for ngramm in iter_dict:
    # Шаг 3
    if len(ngramm_dict[ngramm]['files']) <= MIN_FILES:
        del ngramm_dict[ngramm]
        continue
    if ngramm_dict[ngramm]['total'] <= MIN_COUNT:
        del ngramm_dict[ngramm]
        continue
    # Шаг 5 
    # Служебные части речи в конце 
    words = ngramm.split(" ")
    # Какой-то мусор сплошной, нужно отфильтровать последовательности из одной или двух букв
    if not filter(lambda x: len(x) > 2, words):
        del ngramm_dict[ngramm]
        continue
    p = morph.parse(words[len(words)-1].decode('utf-8'))[0]
    if 'PREP' in p.tag or 'CONJ' in p.tag or 'PRCL' in p.tag or 'INTJ' in p.tag:
        del ngramm_dict[ngramm]
        continue

iter_dict = ngramm_dict.copy()
for ngramm in iter_dict:
    # Шаг 4
    # Статью с алгоритмом не нашла, поэтому ищу просто по логике
    # Выгляди супер неэффективно вычислительно
    if len(ngramm.split(" ")) < MAX_LEN:
        for ngramm2 in iter_dict:
            if ngramm != ngramm2 and ngramm in ngramm2:
                if ngramm_dict[ngramm]['total'] <= iter_dict[ngramm2]['total']:
                    del ngramm_dict[ngramm]
                    break

# Выводим в файлик по уменьшению значения q
out = open('markers_found_no_extra.txt', 'w')
for k, v in sorted(ngramm_dict.items(), key=lambda item: 1/item[1]['total']):
    out.write(k + '\n')
out.close()
