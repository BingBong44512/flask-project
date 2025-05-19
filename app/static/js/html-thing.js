		const inputText = "The {mitochondria, nucleus} is the powerhouse of the cell. {2+2, 4, 5} is equal to 4.";

		const correctAnswers = [
			"mitochondria",
			"4"
		];

		function parseTextWithDropdowns(text) {
			let dropdownIndex = 0;
			
			return text.replace(/\{[A-z-, ]+\}/g, (match) => {
				const options = match.replace(/\{|\}/g,"").split(',').map((opt) => opt.trim());
				const selectId = `dropdown-${dropdownIndex++}`;
				let selectHTML = `<select id="${selectId}">`;
				for (let option of options) {
					selectHTML += `<option>${option}</option>`;
				}
				selectHTML += '</select>';
				return selectHTML;
			});
		}

		function checkAnswers() {
			let allCorrect = true;
			for (let i = 0; i < correctAnswers.length; i++) {
				const dropdown = document.getElementById(`dropdown-${i}`);
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

		document.getElementById("output").innerHTML = parseTextWithDropdowns(inputText);