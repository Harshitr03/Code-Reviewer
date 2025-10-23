    const form = document.getElementById('review-form');
    const messageBox = document.getElementById('message-box');
    const submitButton = document.getElementById('submit-button');
    const buttonText = document.getElementById('button-text');
    const reportSection = document.getElementById('report-section');
    const RAW_CODE_URL = window.location.origin + '/api/report/'; // Base URL for report fetching

    function showMessage(message, isError = false) {
        messageBox.classList.remove('hidden', 'bg-red-100', 'text-red-700', 'bg-green-100', 'text-green-700');
        messageBox.textContent = message;
        if (isError) {
            messageBox.classList.add('bg-red-100', 'text-red-700');
        } else {
            messageBox.classList.add('bg-green-100', 'text-green-700');
        }
    }

    function setLoading(isLoading) {
        submitButton.disabled = isLoading;
        buttonText.textContent = isLoading ? 'Analyzing Code...' : 'Start Code Review';
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        setLoading(true);
        messageBox.classList.add('hidden');
        reportSection.classList.add('hidden');

        const fileInput = document.getElementById('code_file');
        const file = fileInput.files[0];

        if (!file) {
            showMessage("Please select a file to upload.", true);
            setLoading(false);
            return;
        }

        // Simple check to prevent sending massive files to the LLM/API
        if (file.size > 1024 * 1024) { // 1MB limit
            showMessage("File too large. Please select a file under 1MB.", true);
            setLoading(false);
            return;
        }

        const formData = new FormData();
        formData.append('code_file', file);

        try {
            const response = await fetch('/api/review', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (!response.ok) {
                const errorMessage = result.error || 'Unknown API error occurred.';
                showMessage(`Review Failed: ${errorMessage}`, true);
                setLoading(false);
                return;
            }

            showMessage(`Review complete! Report ID: ${result.report_id}. Now loading report...`);
            loadReport(result.report_id);

        } catch (error) {
            showMessage(`Network or server error: ${error.message}`, true);
        } finally {
            setLoading(false);
        }
    });

    async function loadReport(reportId) {
        try {
            const response = await fetch(`/api/report/${reportId}`);
            const reportData = await response.json();

            if (!response.ok) {
                showMessage(`Failed to load report: ${reportData.error || 'Report not found.'}`, true);
                return;
            }

            renderReport(reportData);

        } catch (error) {
            showMessage(`Error fetching report: ${error.message}`, true);
        }
    }

    function renderReport(data) {
        const review = data.review;
        const suggestionsContainer = document.getElementById('suggestions-container');
        const bugsContainer = document.getElementById('bugs-container');

        // Clear previous content
        suggestionsContainer.innerHTML = '';
        bugsContainer.innerHTML = '';

        // 1. Header and Scores
        document.getElementById('report-filename').textContent = data.filename;
        document.getElementById('readability-score').textContent = review.readability_score || '--';
        document.getElementById('modularity-score').textContent = review.modularity_score || '--';
        document.getElementById('review-summary').textContent = review.review_summary || 'No summary provided by LLM.';
        document.getElementById('best-practices-adherence').textContent = review.best_practices_adherence || 'No comment provided by LLM.';
        
        // 2. Suggestions
        if (review.suggestions && review.suggestions.length > 0) {
            review.suggestions.forEach(s => {
                const card = document.createElement('div');
                card.className = 'suggestion-card bg-white p-5 rounded-xl shadow-md border border-l-4 border-blue-500';
                
                const codeSnippet = s.example_code ? `<pre class="code-block-container mt-3 p-3 bg-gray-800 text-white rounded-lg overflow-x-auto text-xs">${s.example_code}</pre>` : '';
                
                card.innerHTML = `
                    <h4 class="text-lg font-semibold text-blue-700">${s.area}</h4>
                    <p class="text-gray-600 mt-1">${s.detail}</p>
                    ${codeSnippet}
                `;
                suggestionsContainer.appendChild(card);
            });
        } else {
            suggestionsContainer.innerHTML = '<p class="text-gray-500 italic">No specific improvement suggestions were generated.</p>';
        }

        // 3. Potential Bugs
        if (review.potential_bugs && review.potential_bugs.length > 0) {
            review.potential_bugs.forEach(bug => {
                const li = document.createElement('li');
                li.textContent = bug;
                bugsContainer.appendChild(li);
            });
        } else {
            bugsContainer.innerHTML = '<p class="text-green-700">No critical bugs or vulnerabilities were immediately identified.</p>';
            bugsContainer.classList.remove('list-disc', 'pl-5');
            bugsContainer.classList.remove('bg-red-50', 'border-red-200');
            bugsContainer.classList.add('bg-green-50', 'border-green-200');
        }
        
        // 4. Raw Code
        document.getElementById('raw-code').textContent = data.raw_code;
        document.getElementById('raw-code-container').classList.add('hidden'); // Reset toggle
        
        reportSection.classList.remove('hidden');
        window.scrollTo(0, 0); // Scroll to top to view report
    }

    function toggleRawCode() {
        const container = document.getElementById('raw-code-container');
        container.classList.toggle('hidden');
    }
