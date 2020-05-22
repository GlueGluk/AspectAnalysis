# -*- coding: utf-8 -*-
import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
regex = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".decode('utf-8')

file = "markers_found_no_extra.txt";

fh = open(file)
en = []
ru = []
for line in fh:
    if re.search("["+regex+"]", line.decode('utf-8')):
        ru.append(line)
    else:
        en.append(line)
fh.close()

out = open('markers_filtered_en.txt', 'w')
for line in en:
    out.write(line)
out.close()
out = open('markers_filtered_ru.txt', 'w')
for line in ru:
    out.write(line)
out.close()
