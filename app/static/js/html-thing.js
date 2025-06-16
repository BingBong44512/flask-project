
// loads in the questions based on const defined with jinja
document.addEventListener('DOMContentLoaded', function() {
	
	function parseTextWithDropdowns(text) {
		let dropdownIndex = 0;
		// gets the possible answers and puts it in a dropdown
		return text.replace(/\{(.*?)\}/g, (match, contents) => {
			const options = contents.split(',').map(opt => opt.trim());
			const selectId = `dropdown-${dropdownIndex++}`;
			let selectHTML = ``;
			for (let option of options) {
				if (Math.random()*2<1)
				{
				selectHTML += `<option>${option}</option>`;
				}
				else 
				{
					selectHTML = `<option>${option}</option>`+selectHTML;
				}
			}
			selectHTML = `<select id="${selectId}">`+selectHTML;
			selectHTML += '</select>';
			return selectHTML;
		});
	}
	// pushes the question to the output div
	const outputDiv = document.getElementById("output");
	if (outputDiv) {
		outputDiv.innerHTML = parseTextWithDropdowns(inputText);
	} else {
		console.error("Error: Div with ID 'output' not found!");
	}

});
// loops through answers and checks it with correct answer const to correct it
function checkAnswers() {
	let allCorrect = true;
	for (let i = 0; i < correctAnswers.length; i++) {
		const dropdown = document.getElementById(`dropdown-${i}`);
		if (!dropdown) {
			console.warn(`Dropdown with ID 'dropdown-${i}' not found for checking.`);
			allCorrect = false; // Or handle this error differently
			continue;
		}
		const selected = dropdown.value.trim();
		if (selected !== correctAnswers[i]) {
			dropdown.style.border = "2px solid red";
			allCorrect = false;
		} else {
			dropdown.style.border = "2px solid green";
		}
	}
	alert(allCorrect ? "✅ All correct!" : "❌ Some answers are incorrect.");
}