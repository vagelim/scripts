#!/usr/bin/python

#############################################
#prints argv[1] as QR code to screen        #
#alter parameters to encode more information#
#############################################

import qrcode
import sys

#Codes to display Black/White Boxes
BLACK = '\033[40m\033[30m'
WHITE = '\033[47m\033[37m'
RESET = '\033[0m'

#Set QR Parameters
qr = qrcode.QRCode(
	version=1,
	error_correction=qrcode.constants.ERROR_CORRECT_L,
	box_size=1,
	border=1,
)

qr.add_data(sys.argv[1])
qr.make(fit=True)

matrix = qr.get_matrix()


#Print the QR matrix (True = Black, White = False)
#sys.stdout used to prevent printing of newline character following print
#sys.stdout.write(WHITE + "______________________________________________" + RESET)
for row in matrix:
	sys.stdout.write("\n")
	#sys.stdout.write(WHITE + "__" + BLACK)
	for col in row:
		if col == True:
			sys.stdout.write(BLACK + "__")
		else:
			sys.stdout.write(WHITE + "__")
	sys.stdout.write(WHITE + "__" + BLACK)
	sys.stdout.write(RESET)

#sys.stdout.write(WHITE + "______________________________________________" + RESET)

sys.stdout.write(RESET)
