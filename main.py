#!/usr/bin/env python3

from flask import Flask, render_template, request
import googlemaps
import util
import sys
import ec_model
import json
import numpy as np

app = Flask(__name__)
api_key = util.get_api_key()

@app.route("/")
def index():
	return render_template('index.html', app_name="- PHARMACY -", api_key=api_key, lat=40.677810, lng=-73.943432)


@app.route('/get_pharmacies', methods = ['POST'])
def get_pharmacies():
	
	if request.method == 'POST':
	
		lat = float(request.form['latitude'])
		lng = float(request.form['longitude'])
	
		location = (lat, lng)

		radius = int(request.form['radius'])
		(hof, lats, longs) = ec_model.run(location, radius, test=True)

		response = {
			'hof': list(hof[0]),
			'lats': lats,
			'longs': longs
		}

		return json.dumps(response), 200
		#return render_template('index.html', app_name="- PHARMACY -", api_key=api_key, hof=hof[0], lat=lat, lng=lng), 200


if __name__ == "__main__":
	app.run(debug=True)
	