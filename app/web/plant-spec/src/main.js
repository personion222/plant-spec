import '@knadh/oat/oat.min.css';
import '@knadh/oat/oat.min.js';
import Chart from 'chart.js/auto'

document.getElementById("folder-form").reset()

const wl = [410, 435, 460, 485, 510, 535, 560, 585, 610, 645, 680, 705, 730, 760, 810, 860, 900, 940]
const backend_url = "http://127.0.0.1:8080"
const pics = [];
var cur_page = -1;
const unscanned_badge = document.createElement("span");
unscanned_badge.textContent = "not scanned!";
unscanned_badge.className = "badge danger";
const unknown_badge = document.createElement("span");
unknown_badge.textContent = "unknown";
unknown_badge.className = "badge warning";
const scanned_badge = document.createElement("span");
scanned_badge.textContent = "scanned";
scanned_badge.className = "badge success";
var scans_json;
var entries_processed;
var mission_files;
document.getElementById("folder-inp").addEventListener("change", async (event) => {
	mission_files = event.target.files;
	const scans_file = Array.from(mission_files).find(f => f.name == "scans.json");
	const json_reader = new FileReader();
	json_reader.onload = async () => {
		scans_json = JSON.parse(json_reader.result);
		const entries_res = await fetch(`${backend_url}/process-entries`, {
			method: "POST",
			headers: {
				"Accept": "application/json",
				"Content-Type": "application/json"
			},
			body: json_reader.result,
		});
		entries_processed = await entries_res.json();
		for (let tag_id in scans_json["missed"]) {
			const tag_obj = document.createElement("a");
			tag_obj.textContent = `${tag_id}: ${scans_json["missed"][tag_id]["plant"]}`;
			tag_obj.appendChild(unscanned_badge.cloneNode(true));
			tag_obj.onclick = () => render_tag_scan(tag_id, true);
			document.getElementById("missed-ls").appendChild(tag_obj);
			scans_json["missed"][tag_id]["obj"] = tag_obj;
		}
		for (let tag_id in scans_json["entries"]) {
			const tag_obj = document.createElement("a");
			tag_obj.textContent = `${tag_id}: ${scans_json["entries"][tag_id]["plant"]}`;
			if (scans_json["entries"][tag_id]["plant"] === null) {
				tag_obj.appendChild(unknown_badge.cloneNode(true));
			} else {
				tag_obj.appendChild(scanned_badge.cloneNode(true));
			}
			tag_obj.onclick = () => render_tag_scan(tag_id);
			document.getElementById("scanned-ls").appendChild(tag_obj);
			scans_json["entries"][tag_id]["obj"] = tag_obj;
		}
		render_gen_settings();
	}
	json_reader.readAsText(scans_file);
});

function render_gen_settings() {
	document.getElementsByTagName("main")[0].innerHTML = `
	<h1>Mission info</h1>
	<p>Tag offset: x: <code id="offset-x"></code> mm, y: <code id="offset-y"></code> mm, z: <code id="offset-z"></code> mm</p>
	<p>Integration cycles: <code id="intcycles-txt"></code> (exposure time: <code id="intms-txt"></code> ms)</p>
	<p>April tag size (mm): <code id="tagsize-txt"></code></p>
	<p>AS7265x lens FOV: <code id="fov-txt"></code></p>
	`;
	document.getElementById("offset-x").textContent = scans_json["offset"][0].toString();
	document.getElementById("offset-y").textContent = scans_json["offset"][1].toString();
	document.getElementById("offset-z").textContent = scans_json["offset"][2].toString();
	document.getElementById("intcycles-txt").textContent = scans_json["intcycles"].toString();
	document.getElementById("intms-txt").textContent = (scans_json["intcycles"] * 2.8).toString();
	document.getElementById("tagsize-txt").textContent = scans_json["tagsize"].toString();
	document.getElementById("fov-txt").textContent = scans_json["fov"].toString();
}
document.getElementById("gen-settings-tab").onclick = () => {
	if (cur_page != -1) {
		cur_page = -1;
		render_gen_settings();
	}
}

function render_tag_scan(id, missing = false) {
	if (cur_page != id) {
		cur_page = id;
		let plantname;
		if (missing) {
			plantname = scans_json["missed"][id]["plant"];
		} else {
			plantname = scans_json["entries"][id]["plant"];
		}
		document.getElementsByTagName("main")[0].innerHTML = `
		<h1 id="tag-title"></h1>
		<div class="tag-dash">
			<img id="plant-img" />
			<div id="spec-chart-container"><canvas id="spec-chart" /></div>
			<table>
				<tbody>
					<tr>
						<td>Time since mission start (hh:mm:ss)</td> <td><code id="time-txt"></code></td>
					</tr>
					<tr>
						<td>Water (mL/day)</td> <td><code id="water-txt"></code></td>
					</tr>
					<tr>
						<td>Infrared proximity (unitless, higher = farther, 0-1.5m)</td> <td><code id="prox-txt"></code></td>
					</tr>
					<tr>
						<td>Ambient light (lux)</td> <td><code id="amb-txt"></code></td>
					</tr>
				</tbody>
			</table>
		</div>
		`;
		document.getElementById("tag-title").textContent = `Tag ID ${id}: ${plantname}`;
		if (!missing) {
			console.log("adding image");
			const img_file = Array.from(mission_files).find(f => f.name == `${id}.jpg`);
			const img_reader = new FileReader();
			img_reader.onload = (e) => {
				document.getElementById("plant-img").src = e.target.result;
			}
			img_reader.readAsDataURL(img_file);
			const rf_data = [];
			const sample_cts_data = [];
			const ref_cts_data = [];
			for (let i = 0; i < wl.length; i++) {
				rf_data.push({x: wl[i], y: entries_processed[id]["rf"][i]});
				sample_cts_data.push({x: wl[i], y: scans_json["entries"][id]["scanwl"][i]});
				ref_cts_data.push({x: wl[i], y: scans_json["entries"][id]["calwl"][i]});
			}
			const chart_ctx = document.getElementById("spec-chart");
			console.log(sample_cts_data);
			const data = {
				datasets: [{
					yAxisID: 'y',
					label: "Reflectance factor",
					data: rf_data,
					fill: false
				}, {
					yAxisID: "y_alt",
					label: "Sample scan (counts)",
					data: sample_cts_data,
					fill: false
				}, {
					yAxisID: "y_alt",
					label: "Reference scan (counts)",
					data: ref_cts_data,
					fill: false
				}]
			}
			new Chart(chart_ctx, {
				type: "line",
				data: data,
				options: {
					scales: {
						x: {
							position: "bottom",
							type: "linear",
							min: wl[0],
							max: wl[wl.length - 1]
						},
						y: {
							display: true,
							position: "left",
							beginAtZero: true
						},
						y_alt: {
							display: true,
							position: "right",
							type: "linear",
							beginAtZero: true
						}
					}
				}
			})
			let ticks_date = new Date(scans_json["entries"][id]["ms"]);
			let time_str = ticks_date.getUTCHours().toString().padStart(2, '0')
			+ ':' + ticks_date.getUTCMinutes().toString().padStart(2, '0')
			+ ':' + ticks_date.getSeconds().toString().padStart(2, '0');
			document.getElementById("time-txt").textContent = time_str;
			if (scans_json["entries"][id]["water"]) {
				document.getElementById("water-txt").textContent = scans_json["entries"][id]["water"].toString();
				document.getElementById("tag-title").appendChild(scanned_badge.cloneNode(true))
			} else {
				document.getElementById("water-txt").textContent = "null";
				document.getElementById("tag-title").appendChild(unknown_badge.cloneNode(true))
			}
			document.getElementById("prox-txt").textContent = scans_json["entries"][id]["prox"].toString();
			document.getElementById("amb-txt").textContent = scans_json["entries"][id]["amb"].toString();
		} else {
			document.getElementById("time-txt").textContent = "null";
			document.getElementById("water-txt").textContent = scans_json["missed"][id]["water"].toString();
			document.getElementById("prox-txt").textContent = "null";
			document.getElementById("amb-txt").textContent = "null";
			document.getElementById("tag-title").appendChild(unscanned_badge.cloneNode(true));
		}
	}
}

document.getElementById("clear").onclick = () => {
	location.reload();
}
