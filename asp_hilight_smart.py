# -*- coding: utf-8 -*-
import os
import re
from pymystem3 import Mystem

files_dir = "./t2"
res_dir = "./res_smart3/"
files = os.listdir(files_dir)
mstm = Mystem()
regex = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ".decode('utf-8')
count = 0

asps = {
    "probl_state":  "#ff8080",
    "research_aim": "#ffb84d",
    "actual":       "#ffff66",
    "idea_method":  "#85e085",
    "result":       "#66a3ff",
}

asp_data = {
    "probl_state":   [],
    "research_aim":  [],
    "actual":        [],
    "idea_method":   [],
    "result":        [],
}

rel_data = {
    "attribution":   [],
    "clarification": [],
    "restatement":   [],
    "emphasis":      [],
    "opinion":       [],
    "assumption":    [],
    "conclusion":    [],
    "cause-effect":  [],
    "addition":      [],
    "antithesis":    [],
    "analogy":       [],
    "sequence":      [],
}

wordbreak = r'(^|$|[\s\.,\?!\"«»\-])'
not_wb = r'[^\s\.,\?!\"«»\-]'
wb = r'[\s\.,\?!\"«»\-]'
word_regex = r'\B'+r'(?i)[A-ZА-ЯЁ]'+r'\B'

# prepare aspect data
for asp in asps.keys():
    fh = open("./asp/"+asp)
    for line in fh:
        line = re.sub(r'\n', '', line)
        asp_data[asp].append(line)
    fh.close()

# prepare relation data
for rel in rel_data.keys():
    fh = open("./rel/"+rel)
    for line in fh:
        line = re.sub(r'\n', '', line)
        rel_data[rel].append(line)
    fh.close()

for file in files:
    count+=1
    print(str(count)+"/"+str(len(files))+" "+file)
    cont = ""
    if os.path.isfile(files_dir+"/"+file):
        fh = open(files_dir+"/"+file)
        cont = fh.read()
        fh.close()
    print(len(cont))
    if not len(cont):
        continue

    changed = 0
    res = ""
    cont = cont.decode('utf-8')
    cont = re.sub(r'^'+wb+r'+', "", cont, re.U)
    # по очереди по словам проходим
    while re.match(r'^'+not_wb+'+?'+wordbreak, cont, re.U):
        # начиная с 1ого слова берём кусок в 5 слов (или меньше, если 5 нет)
        frag = ""
        m = re.match('(('+not_wb+'+?'+wordbreak+'+){5})', cont)
        if m:
            frag = m.group(1)
        else:
            frag = cont
        lemmas = mstm.lemmatize(frag)
        lemmas = list(filter(lambda x: re.match(not_wb, x, re.U), lemmas))
        data = " ".join(lemmas)

        # ищем маркер в фрагменте с его начала
        found_len = 0
        for asp in asps.keys():
            if not found_len:
                for pat in asp_data[asp]:
                    line = pat
                    line = re.sub(r'\\\s+', '\s+', line)
                    line = re.sub(r'\s+', '\s+', line)
                    if re.match(line, data.encode('utf-8')):
                        changed = 1
                        words = re.split(r'[\s\.,\?!]+', pat)
                        found_len = len(words)
                        m = re.match('(('+not_wb+'+?'+wordbreak+'+){'+str(found_len)+'})', cont, re.U)
                        if m:
                            add_frag = m.group(0)
                            m = re.match(r'^(.*?'+not_wb+'+?)('+wordbreak+'+)$', add_frag, re.U|re.DOTALL)
                            if m:
                                # Подготовим к html формату
                                ins = m.group(1).encode("utf-8").replace(" ", "&nbsp;")
                                rest = m.group(2).encode("utf-8").replace(" ", "&nbsp;")
                                res += '<span style="background-color:'+asps[asp]+'">'+ins+'</span>'+rest
                                cont = re.sub(r'^'+re.escape(add_frag), '', cont, 0, re.U)
        for rel in rel_data.keys():
            if not found_len:
                for pat in rel_data[rel]:
                    line = pat
                    line = re.sub(r'\\\s+', '\s+', line)
                    line = re.sub(r'\s+', '\s+', line);
                    if re.match(line+wordbreak, data.encode('utf-8')):
                        changed = 1
                        words = re.split(r'[\s\.,\?!]+', pat)
                        found_len = len(words)
                        m = re.match('(('+not_wb+'+?'+wordbreak+'+){'+str(found_len)+'})', cont, re.U)
                        if m:
                            add_frag = m.group(0)
                            m = re.match(r'^(.*?'+not_wb+'+?)('+wordbreak+'+)$', add_frag, re.U|re.DOTALL)
                            if m:
                                # Подготовим к html формату
                                ins = m.group(1).encode("utf-8").replace(" ", "&nbsp;")
                                rest = m.group(2).encode("utf-8").replace(" ", "&nbsp;")
                                res += '<span style="font-weight:bold"> ('+rel+') '+ins+'</span>'+rest
                                cont = re.sub(r'^'+re.escape(add_frag), '', cont, 0, re.U)
        if not found_len:
            m = re.match('('+not_wb+'+?'+wordbreak+'+)', cont, re.U)
            if m:
                res += m.group(1).encode("utf-8")
                cont = re.sub(r'^'+not_wb+'+?'+wordbreak+'+', '', cont, 0, re.U)
    if changed:
        fh = open(res_dir+file+".html", 'w')
        # Подготовим к html формату
        res = res.replace("\n", "<br />")
        fh.write(res)
        fh.close()
