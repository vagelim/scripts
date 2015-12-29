#!/usr/bin/env python
# __author__ = 'vageli'

import cgi, cgitb
import sys

print "Content-Type: text/html"
print

#Get all fields
form = cgi.FieldStorage()
MESSAGE = form.getvalue('string')

CODE = {'A': '.-',     'B': '-...',   'C': '-.-.',
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.', ' ': '_'
        }
# From: https://en.wikipedia.org/wiki/Morse_code#Representation.2C_timing_and_speeds
DIT = 60
DAH = DIT * 3
INTER = DIT # Gap between sounds in letter
SHORT = DIT * 3 # Between letters
MED = DIT * 7 # Between words

def to_csv(msg):
    """Takes a msg in morse code and converts to a signal"""
    csv = []
    for each in msg:
        if each is '.':
            csv.append(DIT)
            csv.append(INTER)
        elif each == '..':
            csv.append(DIT)
            csv.append(INTER)
            csv.append(DIT)
            csv.append(INTER)
        elif each == '...':
            csv.append(DIT)
            csv.append(INTER)
            csv.append(DIT)
            csv.append(INTER)
            csv.append(DIT)
            csv.append(INTER)
        elif each == '....':
            csv.append(DIT)
            csv.append(INTER)
            csv.append(DIT)
            csv.append(INTER)
            csv.append(DIT)
            csv.append(INTER)
            csv.append(DIT)
            csv.append(INTER)
        elif each == '-':
            csv.append(DAH)
            csv.append(INTER)
        elif each == '--':
            csv.append(DAH)
            csv.append(INTER)
            csv.append(DAH)
            csv.append(INTER)
        elif each == '---':
            csv.append(DAH)
            csv.append(INTER)
            csv.append(DAH)
            csv.append(INTER)
            csv.append(DAH)
            csv.append(INTER)
        elif each == '----':
            csv.append(DAH)
            csv.append(INTER)
            csv.append(DAH)
            csv.append(INTER)
            csv.append(DAH)
            csv.append(INTER)
            csv.append(DAH)
            csv.append(INTER)
        elif each == ' ':
            csv.append(SHORT)
        elif each == '_':
            csv.append(MED)
    return csv
def main():%
    if MESSAGE is not None:
        msg = MESSAGE
    else:
        msg = raw_input('MESSAGE: ')
    translated = []
    for char in msg:
        try:
            translated.append(CODE[char.upper()])
        except:
            pass
    csv = to_csv(translated)
    print str(csv)[1:-1].replace(' ', '')



if __name__ == "__main__":
    main()
