
//get data
//process data
//add it to this



function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
	const j = Math.floor(Math.random() * (i + 1));
	[array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function parseTextWithDropdowns(text) {
  let dropdownIndex = 0;
  return text.replace(/\{(.*?)\}/g, (match, contents) => {
    // grab the raw options out of the curly‐braces
    const options = contents.split(',').map(o => o.trim());
    shuffle(options);

    // build the <select>
    const select = document.createElement('select');
    select.id = `dropdown-${dropdownIndex}`;

    // 🔑 Pull the correct answer by index, not by assuming it's first in `contents`
    select.dataset.answer = correctAnswers[dropdownIndex];

    // populate the shuffled options
    options.forEach(opt => {
      const optEl = document.createElement('option');
      optEl.value       = opt;
      optEl.textContent = opt;
      select.appendChild(optEl);
    });

    dropdownIndex++;
    return select.outerHTML;
  });
}

document.addEventListener('DOMContentLoaded', function() {
	const outputDiv = document.getElementById("output");
	if (outputDiv) {
		outputDiv.innerHTML = parseTextWithDropdowns(inputText);
	} else {
		console.error("Error: Div with ID 'output' not found!");
	}
});

function checkAnswers() {
  let allCorrect = true;
  document.querySelectorAll('select').forEach((select, i) => {
    // compare against the answer we stashed on each <select>
    if (select.value.trim() !== select.dataset.answer) {
      select.style.border = "2px solid red";
      allCorrect = false;
    } else {
      select.style.border = "2px solid green";
    }
  });
  alert(allCorrect ? "✅ All correct!" : "❌ Some answers are incorrect.");
}