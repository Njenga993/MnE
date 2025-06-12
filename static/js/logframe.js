// logframe.js
document.addEventListener('DOMContentLoaded', function() {
    const apiBaseUrl = '/api/v1/logframe/';
    const navButtons = document.querySelectorAll('.nav-btn');
    const dataContainer = document.getElementById('logframe-data');
    const loadingSpinner = document.getElementById('loading-spinner');
    
    // Initial load - fetch the root API data
    fetchLogframeData(apiBaseUrl);
    
    // Set up navigation button click handlers
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Update active button
            navButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Get the section to load
            const section = this.dataset.section;
            loadSection(section);
        });
    });
    
    function fetchLogframeData(url) {
        showLoading();
        
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                displayApiRoot(data);
            })
            .catch(error => {
                showError(error);
            })
            .finally(() => {
                hideLoading();
            });
    }
    
    function displayApiRoot(data) {
        let html = '<h2>Logframe Structure</h2>';
        html += '<p>Select a section from the navigation above to view details.</p>';
        html += '<div class="api-links">';
        
        for (const [key, value] of Object.entries(data)) {
            html += `
                <div class="api-link-item">
                    <strong>${capitalizeFirstLetter(key)}:</strong>
                    <a href="${value}" target="_blank">${value}</a>
                </div>
            `;
        }
        
        html += '</div>';
        dataContainer.innerHTML = html;
        dataContainer.style.display = 'block';
    }
    
    function loadSection(section) {
        showLoading();
        dataContainer.style.display = 'none';
        
        // In a real implementation, you would fetch the specific section data
        // For now, we'll just simulate it with the API root URLs
        setTimeout(() => {
            let html = `<h2>${capitalizeFirstLetter(section)}</h2>`;
            html += `<p>This would display the ${section} data fetched from the API.</p>`;
            html += `<p>In a real implementation, we would fetch data from: <code>${apiBaseUrl}${section}/</code></p>`;
            
            dataContainer.innerHTML = html;
            dataContainer.style.display = 'block';
            hideLoading();
        }, 800);
    }
    
    function showLoading() {
        loadingSpinner.style.display = 'block';
    }
    
    function hideLoading() {
        loadingSpinner.style.display = 'none';
    }
    
    function showError(error) {
        dataContainer.innerHTML = `
            <div class="error-message">
                <p>Error loading data:</p>
                <p>${error.message}</p>
            </div>
        `;
        dataContainer.style.display = 'block';
    }
    
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
});