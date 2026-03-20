from flask import Flask, request, jsonify
from flask_cors import CORS
import vegspec as vs
import numpy
import sys
import os

app = Flask(__name__)
CORS(app)
WL = (
	410, 435, 460, 485, 510, 535, 560, 585, 610, 645, 680, 705, 730, 760, 810, 860, 900, 940
) # wavelengths of sensors in nanaometers


@app.route("/process-entries", methods=["POST"])
def process_entries():
	res = {}
	for tag_id, entry in request.json["entries"].items():
		print(tag_id, entry)
		rf = [] # reflectance factors, 0 to 1
		for sample_cts, ref_cts in zip(entry["scanwl"], entry["calwl"]):
			if ref_cts != 0:
				rf.append(min(1, sample_cts / ref_cts))
			else:
				rf.append(0)
		spectrum = vs.VegSpec(WL, rf)
		indices_proc = {}
		for index, val in spectrum.indices.items():
			if numpy.isnan(val) or numpy.isinf(val):
				indices_proc[index] = None
			else:
				indices_proc[index] = round(float(val), 10)
		res[tag_id] = {
			"rf": rf,
			"indices": indices_proc
		}

	return jsonify(res)

if __name__ == "__main__":
	app.run()
