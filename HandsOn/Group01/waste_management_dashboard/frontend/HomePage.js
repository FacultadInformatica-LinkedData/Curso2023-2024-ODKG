function loadDistrictData(wikidataId) {
    // Use AJAX to fetch data without reloading the page
    $.ajax({
        url: 'http://127.0.0.1:5000/district_population', // Update this URL to where your Flask app is hosted
        data: {wikidataId: wikidataId},
        success: function(response) {
            // Display the response in the result div
            document.getElementById('result').textContent = JSON.stringify(response, null, 2);
        },
        error: function(xhr, status, error) {
            // Log the error to the console for debugging
            console.error('Error fetching district data:', xhr.responseText);
            // Show a user-friendly message
            document.getElementById('result').textContent = 'Error fetching district data. Please check the console for more details.';
        }
    });
}
