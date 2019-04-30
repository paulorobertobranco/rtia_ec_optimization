#!/usr/bin/env python3

from flask import Flask, render_template, request
import googlemaps
import util
import sys
import ec_model
import json
import numpy as np

app = Flask(__name__)
api_key = util.get_google_api_key()

@app.route("/")
def index():
	return render_template('index.html', app_name="- PHARMACY -", api_key=api_key, lat=-23.543196, lng=-46.632432)


@app.route('/get_pharmacies', methods = ['POST'])
def get_pharmacies():
	
	if request.method == 'POST':
	
		lat = float(request.form['latitude'])
		lng = float(request.form['longitude'])
		radius = int(request.form['radius'])
		population = int(request.form['population'])
		generation = int(request.form['generation'])
		cxprob = float(request.form['cxprob'])
		mtprob = float(request.form['mtprob'])

		location = (lat, lng)

		# try:

		(init_pop, log, pareto, pharmacies, hospitals) = ec_model.run(location, radius, population=population, n_gen=generation, cxpb=cxprob, mtpb=mtprob, test=True)

		response = {
			'status': "ok",
			'center_spot': location,
			'best_spot_lats': list(map(lambda x: x[0], pareto[0:5])),
			'best_spot_longs': list(map(lambda x: x[1], pareto[0:5])),
			'pharm_lats': list(map(lambda x: x.latitude, pharmacies)),
			'pharm_longs': list(map(lambda x: x.longitude, pharmacies)),
			'pharm_names': list(map(lambda x: x.name, pharmacies)),
			'hosp_lats': list(map(lambda x: x.latitude, hospitals)),
			'hosp_longs': list(map(lambda x: x.longitude, hospitals)),
			'hosp_names': list(map(lambda x: x.name, hospitals)),
			'init_pop_lats': list(map(lambda x: x[0], init_pop)),
			'init_pop_longs': list(map(lambda x: x[1], init_pop)),
			'gens': list(map(lambda x: x['gen'],log)),
			'std_pharm': list(map(lambda x: x['std'][0],log)),
			'std_hosp': list(map(lambda x: x['std'][1],log)),
			'avg_pharm': list(map(lambda x: x['avg'][0],log)),
			'avg_hosp': list(map(lambda x: x['avg'][1],log))
		}

		# except Exception as e:	

		# 	response = {
		# 		'status': str(e)
		# 	}

		return json.dumps(response), 200


if __name__ == "__main__":
	app.run(debug=True)
	