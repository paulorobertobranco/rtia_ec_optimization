import math
import random
import test_data
import googlemaps
import numpy as np

class Data():
	def __init__(self, data):
		self.name = data['name']
		self.address = data['vicinity']
		self.latitude = float(data['geometry']['location']['lat'])
		self.longitude = float(data['geometry']['location']['lng'])

	@property
	def name(self):
		return self.__name

	@name.setter
	def name(self, name):
		self.__name = name
	
	@property
	def address(self):
		return self.__address

	@address.setter
	def address(self, address):
		self.__address = address

	@property
	def latitude(self):
		return self.__latitude

	@latitude.setter
	def latitude(self, latitude):
		self.__latitude = latitude

	@property
	def longitude(self):
		return self.__longitude

	@longitude.setter
	def longitude(self, longitude):
		self.__longitude = longitude


def get_google_api_key():
	with open('../gmaps_api_key.txt', 'r') as f:
		k = f.readline()
	return k


def get_test_data():
	
	response = test_data.pharm['results']
	pharm = list(map(lambda x: Data(x), response))

	response = test_data.hosp['results']
	hosp = list(map(lambda x: Data(x), response))	
	
	return pharm, hosp

def get_data(location, radius, query="pharmacy"):
	gmaps = googlemaps.Client(key=get_google_api_key())
	response = gmaps.places_nearby(keyword=query, location=location, radius=radius)
	
	if response['results']:
		data = list(map(lambda x: Data(x), response['results']))
	else:
		data = None

	return data

def haversine(origin, destination):
	lat1, lon1 = origin
	lat2, lon2 = destination
	radius = 6371

	dlat = math.radians(lat2-lat1)
	dlon = math.radians(lon2-lon1)
	a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = radius * c

	return d

def get_bounds(latitude, longitude, meters):

	earth = 6378.137
	m = (1 / ((2 * math.pi / 360) * earth)) / 1000
    
	return latitude - (meters * m), latitude + (meters * m), longitude - (meters * m) / math.cos(latitude * (math.pi / 180)), longitude + (meters * m) / math.cos(latitude * (math.pi / 180)) 




def get_lat_with_meter(latitude, radius):

	meters = random.random() * radius
	earth = 6378.137
	m = (1 / ((2 * math.pi / 360) * earth)) / 1000
    
	if random.randint(0,1): 
		return latitude + (meters * m)
	else:
		return latitude - (meters * m)

def get_lng_with_meter(latitude, longitude, radius):

	meters = random.random() * radius
	earth = 6378.137
	m = (1 / ((2 * math.pi / 360) * earth)) / 1000

	if random.randint(0,1):
		return longitude + (meters * m) / math.cos(latitude * (math.pi / 180))
	else:
		return longitude - (meters * m) / math.cos(latitude * (math.pi / 180))