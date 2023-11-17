let chart;

function updateGraph(wasteData) {
    const ctx = document.getElementById('indexWasteOverview').getContext('2d');

    // Check if chart is already initialized
    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: wasteData.map(item => item.districtName),
            datasets: [{
                label: 'Total Waste Amount (Kg)',
                data: wasteData.map(item => item.totalAmount),
                backgroundColor: 'rgba(0, 123, 255, 0.5)',
                borderColor: 'rgba(0, 123, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value, index, values) {
                            return value + ' Kg'; // Appending 'Kg' to each y-axis label
                        }
                    }
                }
            }
        }
    });
}

document.getElementById('yearFilter').addEventListener('change', function() {
    const selectedYear = this.value;
    fetch(`/waste-data?year=${selectedYear}`) // Fetch the data for the selected year
        .then(response => response.json())
        .then(data => {
            updateGraph(data);
        });
});

updateGraph(initialWasteData);
