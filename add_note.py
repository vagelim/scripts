#!/usr/bin/env python
from simplenote import Simplenote

USER = 'SIMPLENOTE EMAIL ADDRESS HERE'
PW = 'SIMPLENOTE PASSWORD'

def add_note(note):
        simple = Simplenote(USER, PW)

        #Get auth
        token = simple.authenticate(USER, PW)
	t = simple.add_note(note)
		

if __name__ == '__main__':
        import sys

        if len(sys.argv) > 2:
                note = ' '.join(sys.argv[1:])
        else:
                note = sys.argv[1]
                
        add_note(note)
