async function startResearch() {
    const queryInput = document.getElementById('queryInput');
    const query = queryInput.value.trim();
    if (!query) return;

    const submitBtn = document.getElementById('submitBtn');
    const statusSection = document.getElementById('statusSection');
    const resultSection = document.getElementById('resultSection');
    const reportContent = document.getElementById('reportContent');

    // UI state: Loading
    submitBtn.disabled = true;
    submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
    statusSection.classList.remove('hidden');
    resultSection.classList.add('hidden');

    try {
        const response = await fetch('/api/research', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: query })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const data = await response.json();
        
        // Parse markdown output into HTML
        const rawText = data.report || data.result || "No report generated.";
        reportContent.innerHTML = marked.parse(rawText);
        resultSection.classList.remove('hidden');
        
    } catch (error) {
        reportContent.innerHTML = `<p class="text-red-400 font-medium">Error: ${error.message}</p>`;
        resultSection.classList.remove('hidden');
    } finally {
        // Reset UI state
        statusSection.classList.add('hidden');
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
}

// Optional: Allow pressing "Enter" in the input field to trigger research
document.addEventListener('DOMContentLoaded', () => {
    const queryInput = document.getElementById('queryInput');
    if (queryInput) {
        queryInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                startResearch();
            }
        });
    }
});