#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script provide you with the Chinese fonts found by fc-list,
# let you choose which to use with thuthesis.

# The script prefers the font name in ASCII to the one containing Unicode
# character, thus trying to avoid the problem with 'Adobe 宋体 Std L'.

# The script should work with Python 2.6, 2.7 and Python 3.2, providing
# that your locale is utf-8. Please report issues if you find.

try:
    from subprocess import check_output
except ImportError: # python 2.6 has no check_output
    from subprocess import Popen, PIPE
    def check_output(cmdline):
        return Popen(cmdline, stdout=PIPE).communicate()[0]

# Py3K renames raw_input to input.
try:
    input = raw_input
except:
    pass

import re

# The return value is of type byte string (in py3k).
fontliststr = check_output(["fc-list", ":lang=zh"])
allfontliststr = check_output(["fc-list", ""])
if not fontliststr:
    print("No Chinese font exists! Leaving...")
    exit(1)

# strip out ':style=BLABLA' stuff
fontnamelist = sorted([x.split(b":")[0] for x in fontliststr.splitlines()])
allfontnamelist = sorted([x.split(b":")[0] for x in allfontliststr.splitlines()])

# Convert to unicode string, assuming utf-8 encoding of byte string.
# Thus following variables are all unicode string.
fontnamelist = [x.decode("utf-8") for x in fontnamelist]
allfontnamelist = [x.decode("utf-8") for x in allfontnamelist]

songtilist = []
kaitilist = []
heitilist = []
fangsonglist = []
lishulist = []
youyuanlist = []

for x in fontnamelist:
    if re.search("仿宋|Fang", x, re.IGNORECASE):
        fangsonglist.append(x)
    elif re.search("宋|Ming", x, re.IGNORECASE):
        songtilist.append(x)
    elif re.search("黑|Hei|Sans|Gothic", x, re.IGNORECASE):
        heitilist.append(x)
    elif re.search("楷|Kai", x, re.IGNORECASE):
        kaitilist.append(x)
    elif re.search("隶|Li", x, re.IGNORECASE):
        lishulist.append(x)
    elif re.search("圆|Yuan", x, re.IGNORECASE):
        youyuanlist.append(x)
    else:
        pass

def selectfont(fontlist):
    if not fontlist:
        if not fontnamelist:
            if not allfontnamelist:
                return ''
            else:
                return selectfont(allfontnamelist)
        else:
            return selectfont(fontnamelist)
    
    for i, v in enumerate(fontlist):
        # Ugly, since python 2 has no real print function.
        print(str(i) + ' ' + v)
    while True:
        n_str = input("选择一个：(输入数字[0-" + str(len(fontlist)-1) + "]，默认0。按z在所有中文字体中选择，按a在所有字体中选择)")
        if not n_str:
            n = 0
        else:
            if n_str == "z" or n_str =="Z":
                return selectfont(fontnamelist)
            elif n_str == "a" or n_str == "A":
                return selectfont(allfontnamelist)
            else:
                try:
                    n = int(n_str)
                except ValueError:
                    continue
        if 0 <= n < len(fontlist):
            break
    asciifontname = ''
    for x in fontlist[n].split(","):
        try:
            x.encode('ascii')
        except UnicodeEncodeError:
            pass
        else:
            asciifontname = x
            break
    if asciifontname:
        return asciifontname
    else:
        print("ASCII font name not found!")
        print("You might encounter error using this font with XeLaTeX...")
        return fontlist[n].split(",")[-1]

print("宋体：")
songti = selectfont(songtilist)
print("黑体：")
heiti = selectfont(heitilist)
print("楷体：")
kaiti = selectfont(kaitilist)
print("仿宋：")
fangsong = selectfont(fangsonglist)
print("隶书：")
lishu = selectfont(lishulist)
print("幼圆：")
youyuan = selectfont(youyuanlist)

if not songti or not heiti or not kaiti:
    print("错误：缺少宋体、黑体或楷体字体")
    exit(2)

print("生成字体文件fontname.def")
with open('fontname.def', 'w') as f:
    f.write("\\ProvidesFile{fontname.def}\n")
    f.write("\\newcommand{\\fontsong}{" + songti + "}\n")
    f.write("\\newcommand{\\fonthei}{" + heiti + "}\n")
    f.write("\\newcommand{\\fontkai}{" + kaiti + "}\n")
    if fangsong:
        f.write("\\newcommand{\\fontfs}{" + fangsong + "}\n")
    else:
        print("缺少仿宋，宋体代替")
        f.write("\\newcommand{\\fontfs}{" + songti + "}\n")
    if lishu:
        f.write("\\newcommand{\\fontli}{" + lishu + "}\n")
    else:
        print("缺少隶书，宋体代替")
        f.write("\\newcommand{\\fontli}{" + songti + "}\n")
    if youyuan:
        f.write("\\newcommand{\\fontyou}{" + youyuan + "}\n")
    else:
        print("缺少幼圆，宋体代替")
        f.write("\\newcommand{\\fontyou}{" + songti + "}\n")

