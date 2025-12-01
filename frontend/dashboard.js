const API_URL = "http://localhost:8000";

async function runVisionAttack(type) {
    const resultBox = document.getElementById('vision-result');
    resultBox.textContent = `Running ${type.toUpperCase()} simulation...`;

    try {
        const endpoint = type === 'pgd' ? '/attack/vision/pgd?epsilon=0.3&steps=10' : '/attack/vision/fgsm?epsilon=0.1';
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST'
        });
        const data = await response.json();
        resultBox.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        resultBox.textContent = "Error: " + error.message;
    }
}

async function runNLPAttack() {
    const input = document.getElementById('nlp-input').value;
    const resultBox = document.getElementById('nlp-result');
    resultBox.textContent = "Running attack...";

    try {
        const response = await fetch(`${API_URL}/attack/nlp/synonym`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: input, perturbation_rate: 0.5 })
        });
        const data = await response.json();
        resultBox.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        resultBox.textContent = "Error: " + error.message;
    }
}

async function runLLMAttack() {
    const input = document.getElementById('llm-input').value;
    const resultBox = document.getElementById('llm-result');
    resultBox.textContent = "Running jailbreak simulation...";

    try {
        const response = await fetch(`${API_URL}/attack/llm/jailbreak`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: input })
        });
        const data = await response.json();
        resultBox.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        resultBox.textContent = "Error: " + error.message;
    }
}

async function runAdvTraining() {
    const resultBox = document.getElementById('defense-result');
    resultBox.textContent = "Training model on adversarial examples...";

    try {
        const response = await fetch(`${API_URL}/defend/adversarial_training`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ epochs: 1 })
        });
        const data = await response.json();
        resultBox.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        resultBox.textContent = "Error: " + error.message;
    }
}

async function runScoring() {
    const resultBox = document.getElementById('score-result');
    resultBox.textContent = "Calculating...";

    try {
        const response = await fetch(`${API_URL}/evaluate/score`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                attack_success: true,
                perturbation_norm: 0.04,
                confidence_drop: 0.4,
                attack_type: "FGSM"
            })
        });
        const data = await response.json();
        resultBox.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        resultBox.textContent = "Error: " + error.message;
    }
}
