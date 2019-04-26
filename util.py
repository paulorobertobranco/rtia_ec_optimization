import math
import random
import googlemaps
import numpy as np

class Data():
	def __init__(self, data):
		self.name = data['name']
		self.address = data['formatted_address']
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


def get_api_key():
	with open('../gmaps_api_key.txt', 'r') as f:
		k = f.readline()
	return k


def get_test_data():
	response = [{'formatted_address': 'R. Dez, 11 - Curado IV, Jaboatão dos Guararapes - PE, 54330-110, Brazil', 'geometry': {'location': {'lat': -8.0730337, 'lng': -34.9937103}, 'viewport': {'northeast': {'lat': -8.071655570107277, 'lng': -34.99235232010727}, 'southwest': {'lat': -8.07435522989272, 'lng': -34.99505197989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '4f9e02749e52815ee6fa2a270e37387bba94613f', 'name': 'Farmacia', 'opening_hours': {'open_now': True}, 'photos': [{'height': 4032, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/104549729168652911747/photos">A Google User</a>'], 'photo_reference': 'CmRaAAAAfhVvltohvc60Q2K8ce9TCgtRBjmPrt5IuP5panmgkh31zB3nzX6kryck7g3-HxaUVhIm-IxBxdcclaYTZrMJkLIXaYRJVhQSDHpyJCoilUggUZ-mMPkVk-o-o4iYTnPTEhDzynUlzK9Rf13kDIMcep3AGhQ38yyu4CwCICABJ9S-mZ3Ep49-tQ', 'width': 3024}], 'place_id': 'ChIJPUUARn0cqwcR4q0ss5BgJpo', 'plus_code': {'compound_code': 'W2G4+QG Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W2G4+QG'}, 'rating': 0, 'reference': 'ChIJPUUARn0cqwcR4q0ss5BgJpo', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 0}, {'formatted_address': 'Av. Um, 32 A - Curado, Jaboatão dos Guararapes - PE, 54270-090, Brazil', 'geometry': {'location': {'lat': -8.072587, 'lng': -34.9947109}, 'viewport': {'northeast': {'lat': -8.07121712010728, 'lng': -34.99331087010727}, 'southwest': {'lat': -8.073916779892723, 'lng': -34.99601052989271}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '23fa900fa3634aa132341c5710a2b44430d0ab46', 'name': 'Farmayara', 'place_id': 'ChIJBbYEX30cqwcRkvGgJJmnfOA', 'plus_code': {'compound_code': 'W2G4+X4 Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W2G4+X4'}, 'rating': 4.3, 'reference': 'ChIJBbYEX30cqwcRkvGgJJmnfOA', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 3}, {'formatted_address': 'Av. Um, 07 A - Curado, Jaboatão dos Guararapes - PE, 54270-090, Brazil', 'geometry': {'location': {'lat': -8.071359, 'lng': -34.994962}, 'viewport': {'northeast': {'lat': -8.070011220107277, 'lng': -34.99361877010728}, 'southwest': {'lat': -8.072710879892721, 'lng': -34.99631842989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '06ba8baa27328dcc5efffb445479b66e3388dc2f', 'name': 'Farmácia Popular Nossa Saúde-AquitemPE', 'opening_hours': {'open_now': True}, 'photos': [{'height': 1152, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/103877202020378404429/photos">Aqui Tem PE Pernambuco</a>'], 'photo_reference': 'CmRaAAAAzTg6tgqvDuEMrwn0oQetmWG-9xVrTaxOPBJOqTN9xSNC1E3Pek81W1R72g_Arkbt5CjLcblISV6sFk9aFH3W0M8b6lmdzPGrvq0m-f-1vwfWT-ikCDvKpYN7frxmzCMuEhCHqhoV943MyUQ1bVpRTcX5GhTx0gV2VkOkJa6gnfMQ9FsVZex_gw', 'width': 2048}], 'place_id': 'ChIJ5XUFgYccqwcR38exzsw0kTo', 'plus_code': {'compound_code': 'W2H4+F2 Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W2H4+F2'}, 'rating': 2, 'reference': 'ChIJ5XUFgYccqwcR38exzsw0kTo', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 2}, {'formatted_address': 'Av. Um, 103 - Bloco 41 - Curado, Jaboatão dos Guararapes - PE, 54270-090, Brazil', 'geometry': {'location': {'lat': -8.0704789, 'lng': -34.9954089}, 'viewport': {'northeast': {'lat': -8.069112120107278, 'lng': -34.99401322010728}, 'southwest': {'lat': -8.071811779892721, 'lng': -34.99671287989273}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '47b8703c66c4a7e652e24c8d47d9fa6af03371dd', 'name': 'Farmácia Maia', 'opening_hours': {'open_now': True}, 'place_id': 'ChIJxYVmZYccqwcRq45o6ss3AYg', 'plus_code': {'compound_code': 'W2H3+RR Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W2H3+RR'}, 'rating': 3.9, 'reference': 'ChIJxYVmZYccqwcRq45o6ss3AYg', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 8}, {'formatted_address': 'Av. Um, 48 - Bloco 48 - Curado, Jaboatão dos Guararapes - PE, 54270-090, Brazil', 'geometry': {'location': {'lat': -8.0685024, 'lng': -34.9960581}, 'viewport': {'northeast': {'lat': -8.06714152010728, 'lng': -34.99467082010728}, 'southwest': {'lat': -8.069841179892723, 'lng': -34.99737047989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': 'dad89d64d06af60c6f64dbbcdb785368ee4f12f4', 'name': 'Worker Pharmacy', 'opening_hours': {'open_now': True}, 'photos': [{'height': 835, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/101113410769259201603/photos">Cachorrão Mil Gr4u</a>'], 'photo_reference': 'CmRaAAAAKF9J72xIKzeWgo3wTciP5NS4WZEUoDDEpMc4kYzlWcLnlLiaSi6hBsaJkGk0Oi2p71yQQc6SYsXIi7lzPlr3vajan_QL9U2Qwo2DH8SaTXUks5fzhTx3JG4WbHwL8fqJEhBqoX596n-KYkvhmsE3VAlnGhRzZkNuW977R1C6ocOJy-sH3I9eZg', 'width': 716}], 'place_id': 'ChIJ1wnttYAcqwcRDaq3Co-E1Wk', 'plus_code': {'compound_code': 'W2J3+HH Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W2J3+HH'}, 'rating': 4.5, 'reference': 'ChIJ1wnttYAcqwcRDaq3Co-E1Wk', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 4}, {'formatted_address': 'Av. Oito, n: 279 - Curado IV, Jaboatão dos Guararapes - PE, 54270-070, Brazil', 'geometry': {'location': {'lat': -8.0732023, 'lng': -34.9969191}, 'viewport': {'northeast': {'lat': -8.071812270107278, 'lng': -34.99550017010728}, 'southwest': {'lat': -8.074511929892722, 'lng': -34.99819982989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '2292e41e3aea7bcabc3dd682208a039093b92c2b', 'name': 'Felipe Farma', 'opening_hours': {'open_now': True}, 'photos': [{'height': 766, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109958238156905179315/photos">A Google User</a>'], 'photo_reference': 'CmRaAAAAtiemqVGuFcogJ7L-nc8TILMmHnWrfk4uMvHiLbY-ZFilI_-u-I3OHPkbnYLN7_rV-B7oTQLOuXkBZAnr8JtKjbPSm5FVr70kd_D92edKtBx69KR1gPG_rHRG6IqEX2LdEhCsgvycwlCYqtXrmxyyvZ0QGhSHjhclwRSvCcECoHwVY3Lgls6bNQ', 'width': 750}], 'place_id': 'ChIJ4bVp3AwdqwcRJHgTbP_t4IY', 'plus_code': {'compound_code': 'W2G3+P6 Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W2G3+P6'}, 'rating': 5, 'reference': 'ChIJ4bVp3AwdqwcRJHgTbP_t4IY', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 2}, {'formatted_address': 'Av. Oito, 525 - Curado, Jaboatão dos Guararapes - PE, 54270-070, Brazil', 'geometry': {'location': {'lat': -8.070635, 'lng': -34.9977389}, 'viewport': {'northeast': {'lat': -8.069265420107277, 'lng': -34.99634742010728}, 'southwest': {'lat': -8.07196507989272, 'lng': -34.99904707989273}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': 'f02403b7d44c81d10ff9b079d4970b73dc20573d', 'name': 'Farmácia El-Shaday', 'opening_hours': {'open_now': True}, 'place_id': 'ChIJTcSd_oYcqwcRr_O0cVi0SPY', 'plus_code': {'compound_code': 'W2H2+PW Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W2H2+PW'}, 'rating': 3.7, 'reference': 'ChIJTcSd_oYcqwcRr_O0cVi0SPY', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 3}, {'formatted_address': 'R. Leonardo da Vinci, 121 - Curado, Jaboatão dos Guararapes - PE, 54220-000, Brazil', 'geometry': {'location': {'lat': -8.0768077, 'lng': -34.9981726}, 'viewport': {'northeast': {'lat': -8.075457020107278, 'lng': -34.99683007010728}, 'southwest': {'lat': -8.078156679892722, 'lng': -34.99952972989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '43fb1597b6faefd85e435c7a75c82eb577988af7', 'name': 'Farmácia dos Genéricos', 'opening_hours': {'open_now': True}, 'place_id': 'ChIJdagKcokcqwcR9pd1BaeL9Ms', 'plus_code': {'compound_code': 'W2F2+7P Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W2F2+7P'}, 'rating': 3.6, 'reference': 'ChIJdagKcokcqwcR9pd1BaeL9Ms', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 5}, {'formatted_address': 'Av. Dolores Duran, 108 - Curado, Jaboatão dos Guararapes - PE, 54220-140, Brazil', 'geometry': {'location': {'lat': -8.0768958, 'lng': -34.9985785}, 'viewport': {'northeast': {'lat': -8.075574970107278, 'lng': -34.99724457010728}, 'southwest': {'lat': -8.078274629892721, 'lng': -34.99994422989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '0149c66b00c726984dc7e57eed39752db86e7c26', 'name': 'Liberdade', 'opening_hours': {'open_now': True}, 'place_id': 'ChIJqxjRa4kcqwcRxRQfRLt7mMA', 'plus_code': {'compound_code': 'W2F2+6H Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W2F2+6H'}, 'rating': 4.8, 'reference': 'ChIJqxjRa4kcqwcRxRQfRLt7mMA', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 4}, {'formatted_address': 'Av. Dolores Duran, 25 - Curado, Jaboatão dos Guararapes - PE, 54220-140, Brazil', 'geometry': {'location': {'lat': -8.077164, 'lng': -34.998594}, 'viewport': {'northeast': {'lat': -8.07577742010728, 'lng': -34.99722352010728}, 'southwest': {'lat': -8.078477079892723, 'lng': -34.99992317989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '6df2bed0f517bfa8dd996b3d80fcfc92c9d5a265', 'name': 'Farmácia Shalom', 'opening_hours': {}, 'place_id': 'ChIJs6SSb4kcqwcR5IpurONSsK0', 'plus_code': {'compound_code': 'W2F2+4H Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W2F2+4H'}, 'rating': 5, 'reference': 'ChIJs6SSb4kcqwcR5IpurONSsK0', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 1}, {'formatted_address': 'Av. Dolores Duran, 68 - Curado, Jaboatão dos Guararapes - PE, 54220-140, Brazil', 'geometry': {'location': {'lat': -8.0762166, 'lng': -34.9999948}, 'viewport': {'northeast': {'lat': -8.074899070107282, 'lng': -34.99866027010727}, 'southwest': {'lat': -8.077598729892726, 'lng': -35.00135992989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '69df4738585c816042a96ddf03adbce53c2a5ed6', 'name': 'MV Farmácia Popular', 'place_id': 'ChIJA_URNIkcqwcRYawXT7aQoow', 'plus_code': {'compound_code': 'W2F2+G2 Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W2F2+G2'}, 'rating': 0, 'reference': 'ChIJA_URNIkcqwcRYawXT7aQoow', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 0}, {'formatted_address': 'Alto da Colina, Jaboatão dos Guararapes - State of Pernambuco, 50950-000, Brazil', 'geometry': {'location': {'lat': -8.0820112, 'lng': -34.9771146}, 'viewport': {'northeast': {'lat': -8.080671570107276, 'lng': -34.97577007010727}, 'southwest': {'lat': -8.08337122989272, 'lng': -34.97846972989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '57b695b3234399e0a43cc0970fce6715012e9426', 'name': 'Rp Pharma', 'place_id': 'ChIJ7bSZy2scqwcRB2cpDHkwNMM', 'plus_code': {'compound_code': 'W29F+55 Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W29F+55'}, 'rating': 0, 'reference': 'ChIJ7bSZy2scqwcRB2cpDHkwNMM', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 0}, {'formatted_address': 'R. Vicente Celestino, 207 - Cristo Redentor, Jaboatão dos Guararapes - PE, 54250-031, Brazil', 'geometry': {'location': {'lat': -8.0820162, 'lng': -34.9771765}, 'viewport': {'northeast': {'lat': -8.080695320107278, 'lng': -34.97578037010728}, 'southwest': {'lat': -8.083394979892722, 'lng': -34.97848002989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '461fb05fd3d8b7460a97da8fe14b4001635c278a', 'name': 'Farma Freitas', 'opening_hours': {'open_now': True}, 'place_id': 'ChIJZ-oWy2scqwcReeZM8J3YjuU', 'plus_code': {'compound_code': 'W29F+54 Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W29F+54'}, 'rating': 0, 'reference': 'ChIJZ-oWy2scqwcReeZM8J3YjuU', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 0}, {'formatted_address': 'Av. Dolores Duran, 37 - Curado, Jaboatão dos Guararapes - PE, 54220-140, Brazil', 'geometry': {'location': {'lat': -8.076067, 'lng': -35.000845}, 'viewport': {'northeast': {'lat': -8.074626570107277, 'lng': -34.99946647010727}, 'southwest': {'lat': -8.077326229892721, 'lng': -35.00216612989271}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '1aec2f0780f0bd55e5e6323de88329e904da5531', 'name': 'Farmácia Nossa Sra. do Carmo', 'opening_hours': {'open_now': True}, 'place_id': 'ChIJWyQ3z44cqwcRaOlwp1FM1cc', 'plus_code': {'compound_code': 'WXFX+HM Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6936WXFX+HM'}, 'rating': 4, 'reference': 'ChIJWyQ3z44cqwcRaOlwp1FM1cc', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 2}, {'formatted_address': 'R. Juvêncio Marquês da Cunha, 133 A - Totó, Recife - PE, 50791-450, Brazil', 'geometry': {'location': {'lat': -8.0815869, 'lng': -34.9686249}, 'viewport': {'northeast': {'lat': -8.080233970107278, 'lng': -34.96720682010729}, 'southwest': {'lat': -8.082933629892722, 'lng': -34.96990647989273}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '13ebb743c7f733c01bcdcddd451967cab3d617e3', 'name': 'RedMed pharmacies - Farmalider', 'opening_hours': {'open_now': True}, 'photos': [{'height': 2336, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/100894881176720650228/photos">A Google User</a>'], 'photo_reference': 'CmRaAAAAQpU3R483_FNGMEB3_JoXW74hAmXUAjTNdqPZ3NcANn6cZjXGDKDfmVNWwBREjoeiVcvMedArztpqUoLJX1jWDQh_gr9XLC9x5giYmdEYHw3EaDzmukl5BmCNh62H3tI_EhAUaEJfKVu2S-g3x4LYl5FAGhRibKLjHcWgaLYxcDmhw_PBFQqNWQ', 'width': 4160}], 'place_id': 'ChIJp-lkbBQcqwcRCH_-fGmMCi8', 'plus_code': {'compound_code': 'W29J+9H Recife - Paratibe, Recife - State of Pernambuco, Brazil', 'global_code': '6937W29J+9H'}, 'rating': 4.5, 'reference': 'ChIJp-lkbBQcqwcRCH_-fGmMCi8', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 12}, {'formatted_address': 'Rua 16 - Curado I, Jaboatão dos Guararapes - PE, 54240-130, Brazil', 'geometry': {'location': {'lat': -8.0834649, 'lng': -34.9828286}, 'viewport': {'northeast': {'lat': -8.082114970107279, 'lng': -34.98148967010727}, 'southwest': {'lat': -8.084814629892723, 'lng': -34.98418932989271}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '056202560a764e13526fd114e73d15c8fd4345da', 'name': 'Drogaria Nova Farma', 'place_id': 'ChIJT7aVAE8dqwcRUZvI02IIIXg', 'plus_code': {'compound_code': 'W288+JV Jaboatão dos Guararapes, State of Pernambuco, Brazil', 'global_code': '6937W288+JV'}, 'rating': 0, 'reference': 'ChIJT7aVAE8dqwcRUZvI02IIIXg', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 0}, {'formatted_address': 'B, Av. Liberdade, 1677 - Totó, Recife - PE, 50940-280, Brazil', 'geometry': {'location': {'lat': -8.081255, 'lng': -34.96815}, 'viewport': {'northeast': {'lat': -8.079850320107276, 'lng': -34.96678992010727}, 'southwest': {'lat': -8.08254997989272, 'lng': -34.96948957989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': 'd983fce58e158afbffdea9567e3d4f6a8ceb774a', 'name': 'Farma Center', 'opening_hours': {'open_now': True}, 'place_id': 'ChIJZ8kXDhQcqwcRqzQPLg3A7Sg', 'plus_code': {'compound_code': 'W29J+FP Recife - Paratibe, Recife - State of Pernambuco, Brazil', 'global_code': '6937W29J+FP'}, 'rating': 5, 'reference': 'ChIJZ8kXDhQcqwcRqzQPLg3A7Sg', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 6}, {'formatted_address': 'R. Ananias Catanho, 25C - Coqueiral, Recife - PE, 50791-361, Brazil', 'geometry': {'location': {'lat': -8.0869391, 'lng': -34.9720476}, 'viewport': {'northeast': {'lat': -8.085587170107278, 'lng': -34.97067317010728}, 'southwest': {'lat': -8.088286829892722, 'lng': -34.97337282989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': 'c24ff56cc510efa8ad955a6a1273cf453f2de6df', 'name': "FARMÁCIA SANT'ANGELO", 'opening_hours': {'open_now': True}, 'place_id': 'ChIJWZWxhD8cqwcRV-OSHzBkGoI', 'plus_code': {'compound_code': 'W27H+65 Recife - Paratibe, Recife - State of Pernambuco, Brazil', 'global_code': '6937W27H+65'}, 'rating': 3.7, 'reference': 'ChIJWZWxhD8cqwcRV-OSHzBkGoI', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 3}, {'formatted_address': 'R. Paulino de Farias, 1030 - Coqueiral, Recife - PE, 50791-235, Brazil', 'geometry': {'location': {'lat': -8.0869924, 'lng': -34.9655298}, 'viewport': {'northeast': {'lat': -8.085657820107278, 'lng': -34.96421882010728}, 'southwest': {'lat': -8.088357479892721, 'lng': -34.96691847989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': 'e4337032e76f7d70ba2a39da9916363b31d39ade', 'name': 'Farmácia San Diego', 'opening_hours': {'open_now': True}, 'place_id': 'ChIJAQC7vj0cqwcRzGva7VNkHgI', 'plus_code': {'compound_code': 'W27M+6Q Recife - Paratibe, Recife - State of Pernambuco, Brazil', 'global_code': '6937W27M+6Q'}, 'rating': 3.1, 'reference': 'ChIJAQC7vj0cqwcRzGva7VNkHgI', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 7}, {'formatted_address': 'R. Aprígio Guimarães, 1030 - Sancho, Recife - PE, 50920-640, Brazil', 'geometry': {'location': {'lat': -8.0866972, 'lng': -34.965204}, 'viewport': {'northeast': {'lat': -8.085496220107277, 'lng': -34.96380192010727}, 'southwest': {'lat': -8.088195879892721, 'lng': -34.96650157989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/shopping-71.png', 'id': '197fe7c43b990da44f52e6f25a1dac0a3975d99e', 'name': 'Dealcyr Dias de Souza Farmácia', 'opening_hours': {}, 'place_id': 'ChIJTUWUlz0cqwcRVvQa72_W3yA', 'plus_code': {'compound_code': 'W27M+8W Recife - Paratibe, Recife - State of Pernambuco, Brazil', 'global_code': '6937W27M+8W'}, 'rating': 0, 'reference': 'ChIJTUWUlz0cqwcRVvQa72_W3yA', 'types': ['pharmacy', 'store', 'health', 'point_of_interest', 'establishment'], 'user_ratings_total': 0}]
	
	data = list(map(lambda x: Data(x), response))
	
	return data

def get_data(location, radius, query="pharmacy"):
	gmaps = googlemaps.Client(key=get_api_key())
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