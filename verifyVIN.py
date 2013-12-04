#Implementation of VIN check algorithm
#Algorithm found at http://en.wikipedia.org/wiki/Vehicle_identification_number#Check_digit_calculation


def verifyVIN(vin):
	length = len(vin)
	#VIN must be 17 characters
	if length != 17:
		print 'Invalid VIN length - VIN must be 17 characters'
		return -1

	if vin.find('I') != -1 or vin.find('O') != -1 or vin.find('Q') != -1:
		print 'Invalid characters found. No letters I, O or Q'
		return -1
	#I, O, and Q are not valid in any VIN

	#Weights are dependent on character position in VIN
	weight = 8
	vin_checksum = 0
	counter = 1

	def charmap(x):
		return {
			'A':1,
			'B':2,
			'C':3,
			'D':4,
			'E':5,
			'F':6,
			'G':7,
			'H':8,
			'J':1,
			'K':2,
			'L':3,
			'M':4,
			'N':5,
			'P':7,
			'R':9,
			'S':2,
			'T':3,
			'U':4,
			'V':5,
			'W':6,
			'X':7,
			'Y':8,
			'Z':9
			}.get(x, x) #Numbers are equal to themselves


	for each in vin:
		if counter == 8:
			weight = 10
		elif counter == 9:
			weight = 0
		elif counter == 10:
			weight = 9
		value = charmap(each)
		value = int(value)
		value = value * weight

		vin_checksum = vin_checksum + value
		weight = weight - 1
		counter = counter + 1
	
	vin_checksum = vin_checksum % 11 #Checksum is sum of weighted products mod 11

	#9-th character is check digit in VIN

	#Cast vin[8] (string) to int before comparing
	if vin_checksum != int(vin[8]):
		print 'CheckSum: ' + str(vin_checksum % 11)
		print 'CheckDigit: ' + vin[8]
	
		return False
	else:
		return True


if __name__ == '__main__':
	vin = '11111111111111111'
	verifyVIN(vin)
