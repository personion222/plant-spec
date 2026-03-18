import '@knadh/oat/oat.min.css';
import '@knadh/oat/oat.min.js';

document.getElementById("folder-inp").addEventListener("change", (event) => {
	let output = document.getElementById("listing");
	for (const file of event.target.files) {
		console.log(file);
	}
})
