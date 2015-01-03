#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: main.py

import re
import pandas as pd
import search
from romanize import he

data = he.data

"""
Data mapping between roman and greek letters and isopsephy values
"""

# letters from α to θ (1 to 9)
data[1] = data['alef']
data[2] = data['beth']
data[3] = data['gimel']
data[4] = data['daleth']
data[5] = data['he']
data[6] = data['vau']
data[7] = data['zayin']
data[8] = data['heth']
data[9] = data['teth']

# letters from ι to ϙ (10 to 90)
data[10] = data['yod']
data[20] = data['kaph']
data[30] = data['lamed']
data[40] = data['mem']
data[50] = data['num']
data[60] = data['samekh']
data[70] = data['ayin']
data[80] = data['pe']
data[90] = data['tsade']

# letters from ρ to ϡ (100 to 900)
data[100] = data['qoph']
data[200] = data['resh']
data[300] = data['shin']
data[400] = data['tau']
data[500] = data['final_kaph']
data[600] = data['final_mem']
data[700] = data['final_nun']
data[800] = data['final_pe']
data[900] = data['final_tsade']

hebrew_roman_values = {}

for num, d in data.items():
  for l in d['letter']:
    # greek small letter value
    hebrew_roman_values[l] = num
    # greek capital letter value
    hebrew_roman_values[l.upper()] = num
    # roman small letter value
    hebrew_roman_values[d['roman']] = num
    # roman capital letter value
    hebrew_roman_values[d['roman'].upper()] = num

regex_hebrew_roman_values = re.compile('|'.join(hebrew_roman_values.keys()))
regex_has_numbers = re.compile('\d')
gematria_error_msg = "String '%s' contains unsupported characters for isopsephy calculation"

class GematriaException(Exception):
    pass

def gematria(string):
    """
    String is a greek letter, word or sentence OR roman letter representation (transliteration) 
    of the greek letter, word or sentence that will be converted to the numerical value letter by letter
    Main function will convert input to unicode format for easier frontend, but on module logic
    more straightforward function unicode_isopsephy is used.
    """
    return unicode_gematria(unicode(string, encoding="utf-8"))

def unicode_gematria(string):
    """
    String argument must be in unicode format.
    """
    result = 0
    # don't accept strings that contain numbers
    if regex_has_numbers.search(string):
        raise GematriaException(gematria_error_msg % string)
    else:
        num_str = regex_hebrew_roman_values.sub(lambda x: '%s ' % hebrew_roman_values[x.group()],
                                               string)
        # don't accept strings, that contains letters which haven't been be converted to numbers
        try:
            result = sum([int(i) for i in num_str.split()])
        except Exception as e:
            raise GematriaException(gematria_error_msg % string)
    return result

def to_roman(word):
    return he.convert(word)

def to_hebrew(word):
    return he.convert(word)

def preprocess_roman(string):
    return he.preprocess(string)

def preprocess_hebrew(string):
    return he.preprocess(string)

def find(text, num, cumulative = False):
    words = text.split()
    numbers = list(map(isopsephy, words))
    if cumulative:
        result = []
        for incides in search.find_cumulative_indices(numbers, num):
            result.append(' '.join([words[idx] for idx in incides]))
        return result
    else:
        return [words[idx] for idx in map(numbers.index, numbers) if numbers[idx] == num]
