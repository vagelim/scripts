#!/usr/bin/env python2

import sys

def generate(callsign):
    seed = 0x73E2

    odd = True
    key = seed
    for char in callsign.upper():
        proc_char = ord(char)
        if odd:
            proc_char <<= 8
        key = key ^ proc_char
        odd = not odd
    key &= 0x7FFF
    return key

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Get your aprs key\n\tusage: {} CALLSIGN".format(sys.argv[0])
        else:
            callsign = sys.argv[1]
            code = generate(callsign)
            print "{} : {}".format(callsign.upper(), code)
