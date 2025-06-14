document.addEventListener("DOMContentLoaded", () => {
  const fills = document.querySelectorAll(".progress-fill");
  fills.forEach(fill => {
    const width = fill.style.width;
    fill.style.width = "0%";
    setTimeout(() => {
      fill.style.width = width;
    }, 100);
  });

  // Donut Chart (Overall Progress)
  const donut = document.getElementById("progressChart");
  if (donut) {
    const progressText = document.querySelector(".progress-fill span")?.textContent || "0";
    const progress = parseFloat(progressText.replace('%', '')) || 0;

    new Chart(donut.getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: ['Completed', 'Remaining'],
        datasets: [{
          data: [progress, 100 - progress],
          backgroundColor: ['#1e8e3e', '#ccc'],
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom' },
        }
      }
    });
  }

  // Bar Chart (Top 5 Indicators)
  const bar = document.getElementById("barChart");
  if (bar) {
    const labels = JSON.parse(bar.getAttribute("data-labels") || "[]");
    const values = JSON.parse(bar.getAttribute("data-values") || "[]");

    new Chart(bar.getContext("2d"), {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Progress (%)',
          data: values,
          backgroundColor: '#1e8e3e',
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    });
  }

  // Category filter
  const filter = document.getElementById('categoryFilter');
  filter?.addEventListener('change', () => {
    const selected = filter.value;
    document.querySelectorAll('.trend-item').forEach(item => {
      const category = item.getAttribute('data-category');
      item.style.display = (selected === 'all' || category === selected) ? '' : 'none';
    });
  });
});
