#!/usr/bin/env python3
# *-* encoding:utf8 *-*
#  vim: colorcolumn=80

import sys
import pickle
from importlib import resources

datafile = "wubi86.dat"


def data2code(data):
    code, *alts = pickle.unpack("4s4B", data)
    while code[-1] == 0:
        code = code[:-1]
    code = code.decode('utf8')
    res = [code] + [code[:alt] for alt in alts if alt > 0]
    return res


def word2code(word, fstream):
    wv = ord(word)
    if wv >= 0x4000 and wv <= 0x9FFF:
        offset = (wv - 0x4000) * 8
        fstream.seek(offset)
        data = fstream.read(8)
        return data2code(data)

    elif wv >= 0xE000 and wv <= 0xFAFF:
        wh = wv >> 8
        wl = wv & 0xff
        mapped_offset = (0x100 + wh) * 8
        fstream.seek(mapped_offset)
        data = fstream.read(8)
        data_index = pickle.unpack('L', data)

        data_offset = (data_index[0] + wl) * 8
        fstream.seek(data_offset)
        data = fstream.read(8)
        return data2code(data)

    return ['']


def words2code(words, fstream):
    def w2c(w):
        return word2code(w, fstream)[0]

    if len(words) == 1:
        return word2code(words[0], fstream)
    elif len(words) == 2:
        return w2c(words[0])[:2] + w2c(words[1])[:2]
    elif len(words) == 3:
        return w2c(words[0])[:1] + w2c(words[1])[:1] + \
                w2c(words[2])[:2]
    else:
        return w2c(words[0])[:1] + w2c(words[1])[:1] + \
                w2c(words[2])[:1] + w2c(words[-1])[:1]


def main():
    if len(sys.argv) > 1:
        w = sys.argv[1]
    else:
        w = '之'
        w = '謢'
        w = '﨎'
    with resources.open_binary('wubi86', datafile) as f:
        print(words2code(w, f))
