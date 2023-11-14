if (distributionData && distributionData.length > 0) {
    const colors = [
        'rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)',
        'rgba(201, 203, 207, 0.2)', 'rgba(233, 30, 99, 0.2)', 'rgba(156, 39, 176, 0.2)',
        'rgba(3, 169, 244, 0.2)', 'rgba(102, 187, 106, 0.2)', 'rgba(255, 87, 34, 0.2)',
        'rgba(121, 85, 72, 0.2)', 'rgba(158, 158, 158, 0.2)', 'rgba(96, 125, 139, 0.2)',
        'rgba(0, 150, 136, 0.2)', 'rgba(103, 58, 183, 0.2)', 'rgba(63, 81, 181, 0.2)',
        'rgba(33, 150, 243, 0.2)', 'rgba(76, 175, 80, 0.2)', 'rgba(139, 195, 74, 0.2)'
    ];

    // Group data by district
    let groupedData = {};
    distributionData.forEach(item => {
        if (!groupedData[item.districtName]) {
            groupedData[item.districtName] = {};
        }
        groupedData[item.districtName][item.month] = item.amount;
    });

    let months = [...new Set(distributionData.map(item => item.month))];
    months.sort((a, b) => a - b); // Sorting months numerically

    let datasets = [];
    Object.keys(groupedData).forEach((districtName, idx) => {
        let dataPoints = months.map(month => groupedData[districtName][month] || 0);
        datasets.push({
            label: districtName,
            data: dataPoints,
            backgroundColor: colors[idx % colors.length],
            borderColor: colors[idx % colors.length].replace('0.2', '1'),
            borderWidth: 1
        });
    });

    const ctx = document.getElementById('wasteChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: months,
            datasets: datasets
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                },
                x: {
                    stacked: false
                }
            }
        }
    });
}
