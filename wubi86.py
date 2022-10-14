#!/usr/bin/env python3
# *-* encoding:utf8 *-*
#  vim: colorcolumn=80

import sys
import pickle

datafile = "./wubi86.dat"



def data2code(data):
    s, *arr = pickle.unpack("4s4B", data)
    while s[-1] == 0:
        s = s[:-1]
    s = s.decode('utf8')
    res = [s] + [s[:l] for l in arr if l>0]
    return res


def word2code(word):
    wv = ord(word)
    if wv >= 0x4000 and wv<= 0x9FFF:
        offset = (wv - 0x4000) * 8
        with open(datafile, 'rb') as f:
            f.seek(offset)
            data = f.read(8)
            return data2code(data)

    if wv >= 0xE000 and wv <= 0xFAFF:
        wh = wv >> 8
        wl = wv & 0xff
        mapped_offset = (0x100 + wh) * 8
        with open(datafile, 'rb') as f:
            f.seek(mapped_offset)
            data = f.read(8)
            data_index = pickle.unpack('L', data)

            data_offset = (data_index[0] + wl) * 8
            f.seek(data_offset)
            data = f.read(8)
            return data2code(data)

def words2code(words):
    if len(words) == 1:
        return word2code(words[0])
    elif len(words) == 2:
        return word2code(words[0])[0][:2] + word2code(words[1])[0][:2]
    elif len(words) == 3:
        return word2code(words[0])[0][:1] + word2code(words[1])[0][:1] + \
                word2code(words[2])[0][:2]
    else:
        return word2code(words[0])[0][:1] + word2code(words[1])[0][:1] + \
                word2code(words[2])[0][:1] + word2code(words[-1])[0][:1]


if len(sys.argv) > 1:
    w = sys.argv[1]
    print(words2code(w))
else:
    w = '之'
    w = '謢'
    w = '﨎'
    print(word2code(w))

