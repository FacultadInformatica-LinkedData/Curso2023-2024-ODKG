// Initialize the map on the 'map1' div and set its view to Madrid
var map1 = L.map('map1').setView([40.416775, -3.703790], 11);
var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map1);

// List of district GeoJSON files
var districts = [
    'Moncloa-Aravaca.geojson',
    'Arganzuela.geojson',
    'Barajas.geojson',
    'Carabanchel.geojson',
    'Centro.geojson',
    'Chamartin.geojson',
    'Chamberi.geojson',
    'Ciudad Lineal.geojson',
    'Fuencarral-El Pardo.geojson',
    'Hortaleza.geojson',
    'Latina.geojson',
    'Moratalaz.geojson',
    'Puente de Vallecas.geojson',
    'Retiro.geojson',
    'Salamanca.geojson',
    'San Blas.geojson',
    'Usera.geojson',
    'Vicalvaro.geojson',
    'Tetuán.geojson',
    'Villa de Vallecas.geojson',
    'Villaverde.geojson',
];

// Function to generate a color based on cartodb_id
function getColor(id) {
    var colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF'];
    return colors[id % colors.length];
}


function style(feature) {
    return {
        fillColor: getColor(feature.properties.cartodb_id),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

// Function to fetch and add a district to the map1
function addDistrict(districtFile) {
    fetch(districtFile)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            L.geoJson(data, {
                onEachFeature: function (feature, layer) {
                    layer.on({
                        mouseover: function(e) {
                            var layer = e.target;
                            layer.bindPopup(feature.properties.name).openPopup();
                        },
                        mouseout: function(e) {
                            var layer = e.target;
                            layer.closePopup();
                        },
                        click: function(e) {
                            var districtName = feature.properties.name;
                            var districtWikidataID = feature.properties.wikidataID;
                            window.location.href = '/district?name=' + encodeURIComponent(districtName) + "&wikidataID=" + encodeURIComponent(districtWikidataID);
                        }
                    });
                },
                style: style
            }).addTo(map1);
        });
}

// Update the file path to include the directory where the GeoJSON files are stored
var basePath = '/static/data/Districts/Districts/';
districts.forEach(function(district) {
    addDistrict(basePath + district);
});
