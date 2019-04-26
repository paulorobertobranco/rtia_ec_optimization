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
	return render_template('index.html', app_name="- PHARMACY -", api_key=api_key, lat=-8.066427, lng=-34.985096)


@app.route('/get_pharmacies', methods = ['POST'])
def get_pharmacies():
	
	if request.method == 'POST':
	
		lat = float(request.form['latitude'])
		lng = float(request.form['longitude'])
		radius = int(request.form['radius'])
		population = int(request.form['population'])
		generation = int(request.form['generation'])
		best = int(request.form['hof'])

		location = (lat, lng)

		try:

			(pop, log, hof, data) = ec_model.run(location, radius, pop=population, n_hof=best, n_gen=generation, test=False)

			response = {
				'status': "ok",
				'center_spot': location,
				'best_spot_lats': list(map(lambda x: x[0], hof)),
				'best_spot_longs': list(map(lambda x: x[1], hof)),
				'lats': list(map(lambda x: x.latitude, data)),
				'longs': list(map(lambda x: x.longitude, data)),
				'pop_lats': list(map(lambda x: x[0], pop)),
				'pop_longs': list(map(lambda x: x[1], pop)),
				'names': list(map(lambda x: x.name, data)),
				'gens': list(map(lambda x: x['gen'],log)),
				'nevals': list(map(lambda x: x['nevals'],log)),
				'avg': list(map(lambda x: x['avg'],log))
			}

		except Exception as e:	

			response = {
				'status': str(e)
			}

		return json.dumps(response), 200


if __name__ == "__main__":
	app.run(debug=True)
	