from simplenote import Simplenote
import time
t = time.strftime("%c")

def save_notes():
	user = ''
	pw = ''
	note = []
	simple = Simplenote(user,pw)

	#Get auth
	token = simple.authenticate(user, pw)

	#Get list of notes
	print "Retrieving list"
	l = simple.get_note_list()
	length = len(l[0])
	print length
	count = 0
	print "Processing list.."
	while count < length:
		print count
		note += simple.get_note(l[0][count]['key'])
		count += 1
	filename = t + '.txt'
	file = open(filename, 'w')
	#To track progress
	for item in note:
		print >> file, item
	file.close()
	#Dump note object to pickle for use by other programs
	import pickle
	pickle.dump(note, open( t + '.pickle', 'wb'))
	
if __name__ == '__main__':
	save_notes()
