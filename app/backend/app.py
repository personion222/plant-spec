from flask import Flask, request, jsonify
import vegspec as vs

app = Flask(__name__)
WL = (
	410, 435, 460, 485, 510, 535, 560, 585, 610, 645, 680, 705, 730, 760, 810, 860, 900, 940
) # wavelengths of sensors in nanaometers


@app.route("/process-entries", methods=["POST"])
def process_entries():
	res = {"entries": []}
	for entry in enumerate(request.json["entries"]):
		rf = [] # reflectance factors, 0 to 1
		for sample_cts, ref_cts in zip(request.json["sample"]["ref"]):
			rf.append(min(1, sample_counts / ref_counts))
		spectrum = vs.VegSpec(WL, rf)
		res["entries"].append({
			"indices": []
		})
		for spect_index in request.json["indices"]:
			res["entries"][-1]["indices"].append(spectrum.indices[spect_index.upper()])

	return jsonify(request.json)
