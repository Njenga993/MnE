document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/v1/indicators/api/v1/indicators/')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#indicator-table tbody');
            tbody.innerHTML = ''; // clear existing rows if any

            data.forEach(indicator => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${indicator.id}</td>
                    <td>${indicator.name}</td>
                    <td>${indicator.description}</td>
                    <td>${indicator.unit || '-'}</td>
                    <td>${indicator.baseline}</td>
                    <td>${indicator.target}</td>
                    <td>${indicator.actual}</td>
                    <td>${indicator.progress}</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching indicators:', error);
        });
});
