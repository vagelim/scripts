import requests

API_KEY = "YOUR GOOGLE GEOLOCATION API HERE"

URL = "https://maps.googleapis.com/maps/api/geocode/json"

address = "125 E 11st New York, New York"

#Strip user input of periods
address = address.replace(' ', '+')
#Strip input of commas - they are not needed
address = address.replace(',' , '')

params = {'key' : API_KEY, 'address' : address, 'sensor' : 'false'}

r = requests.get(URL, params=params)

response = r.json()['status']

#Check response
if response != 'OK':
	#Problem with the request
	if response == "OVER_QUERY_LIMIT":
		print 'OVER REQUEST LIMIT'
	print response

latitude = r.json()['results'][0]['geometry']['location']['lat']
longitude = r.json()['results'][0]['geometry']['location']['lng']
