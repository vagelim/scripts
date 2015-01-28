#!/usr/bin/env python

def random_note(file):
	import pickle

	t = pickle.load( open( file , 'rb' ) )

	import random
	#Choose random number between 0 and the length of pickle
	number = random.randrange(0, len(t))

	#'content' is the dictionary key with the note content
	note = t[number]['content']
	print note

	return note

if __name__ == '__main__':
	import sys
	random_note(sys.argv[1])

	
