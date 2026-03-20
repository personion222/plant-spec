import '@knadh/oat/oat.min.css';
import '@knadh/oat/oat.min.js';

const tags = [];
document.getElementById("add-tag").onclick = () => {
	const row = document.createElement("tr");
	row.innerHTML = `
		<td><input type="number" min=0 max=272 placeholder=0 value=0></td>
		<td><input type="text" placeholder="beetroot" value="beetroot"></td>
		<td><input type="number" min=0 max=1000 placeholder=40 value="40"></td>
	`;
	document.getElementById("tag-ls").appendChild(row);
	row.children[0].children[0].value = tags.length;
	tags.push(row);
}

document.getElementById("remove-tag").onclick = () => {
	tags.pop();
	let tagls = document.getElementById("tag-ls");
	if (tagls.lastChild) {
		tagls.removeChild(tagls.lastChild);
	}
}

document.getElementById("get-conf").onclick = () => {
	const res = {
		"tags": {},
		"intcycles": document.getElementById("intcycles").valueAsNumber,
		"fov": document.getElementById("fov").valueAsNumber,
		"tagsize": document.getElementById("tagsize").valueAsNumber,
		"offset": [document.getElementById("xoff").valueAsNumber, document.getElementById("yoff").valueAsNumber, document.getElementById("zoff").valueAsNumber]
	};
	for (let row of tags) {
		res["tags"][row.children[0].children[0].valueAsNumber] = {
			"plant": row.children[1].children[0].value,
			"water": row.children[2].children[0].valueAsNumber
		}
	}
	const json = JSON.stringify(res, null, "	");
	const blob = new Blob([json], {type: "application/json"});
	const url = URL.createObjectURL(blob);
	const a = document.createElement("a");
	a.href = url;
	a.download = "config.json";
	a.click();

	URL.revokeObjectURL(url);
}

document.getElementById("add-tag").click();
