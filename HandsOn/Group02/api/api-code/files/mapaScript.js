$(document).ready(function() {
    var map = L.map("map").setView([40.42, -3.7], 10);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributor | " +
            "&copy; <a href='https://datos.madrid.es/portal/site/egob/menuitem.3efdb29b813ad8241e830cc2a8a409a0/?vgnextoid=108804d4aab90410VgnVCM100000171f5a0aRCRD&vgnextchannel=b4c412b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default'>Ayuntamiento de Madrid</a> source"
    }).addTo(map);

    map.invalidateSize();

    // Conjunto de capas para los marcadores
    var markersLayer = new L.LayerGroup().addTo(map);

    // Array para almacenar las coordenadas de los marcadores
    var markerCoords = [];

    // Llamar a la función con "default" al cargar la página
    realizarAutocompletado("default");

    function realizarAutocompletado(inputText) {
        // Hacer una solicitud al servidor para obtener resultados
        $.ajax({
            url: '/api/search/distrito/' + inputText,
            type: 'GET',
            dataType: 'json', // Especifica el tipo de datos como JSON
            success: function(data) {

                // Crear un nuevo elemento select
                var select = $('#autocomplete');

                // Recorrer los nombres devueltos por el servidor y mostrarlos
                data.nombres.forEach(function(result) {
                    // Crear un nuevo elemento option
                    var option = $('<option></option>');
                    option.val(result);
                    option.text(result);

                    // Añadir el elemento option al elemento select
                    select.append(option);
                });
            },
            error: function() {
                console.error('Error en la solicitud AJAX');
                var select = $('#autocomplete')[0];
                while (select.options.length > 1) {
                    select.remove(1);
                }
            }
        });
    }

    // Función de autocompletado
    $('#street-input').on('input', function() {
        var inputText = $(this).val().toLowerCase();

        var select = $('#autocomplete')[0];
        while (select.options.length > 1) {
            select.remove(1);
        }
        if (inputText.trim() === "") {
            realizarAutocompletado("default");
        } else{
            realizarAutocompletado(inputText);
        }

    });

    

    // Manejar clic en resultado de autocompletado
    $('#autocomplete-select').on('change', 'select', function() {
        var selectedStreet = $(this).find('option:selected').text();
        if("Selecciona un distrito" === selectedStreet){
            return;
        }
        alert('Has seleccionado el distrito: ' + selectedStreet);
        var loadingBar = document.getElementById('loading-bar');
        loadingBar.style.display = 'flex';
        loadingBar.classList.remove('hidden');
        $('#search-box').css('display', 'none');
        $('#autocomplete-select').css('display', 'none');

        // Vaciar el array de coordenadas
        markerCoords = [];
        markersLayer.clearLayers();
        map.setView([40.42, -3.7], 10);
        var loadingText = document.querySelector('#loading-text');
        loadingText.textContent = 'Cargando...';

        // Hacer una solicitud al servidor para obtener resultados de locales
        $.ajax({
            url: '/api/search/distrito/' + selectedStreet+ '/locales',
            type: 'GET',
            dataType: 'json', // Especifica el tipo de datos como JSON
            success: function(data) {
                // Recorrer los resultados devueltos por el servidor
                // Borrar marcadores anteriores
                markersLayer.clearLayers();
                
                // Hacer una solicitud al servidor para obtener resultados de imagen de distrito
                var img = "";
                var wikidataUrl = data.locales[0].sameAsNombreDistrito;
                var entityId = wikidataUrl.split('/').pop();
                var apiUrl = 'https://www.wikidata.org/w/api.php?action=wbgetentities&ids=' + entityId + '&props=claims&format=json&origin=*';
                fetch(apiUrl).then(response => response.json()).then(data => {
                        // Extrae la imagen de los datos
                        var imageClaim = data.entities[entityId].claims.P18;
                        if (imageClaim) {
                            var imageFileName = imageClaim[0].mainsnak.datavalue.value;
                            var imageUrl = "https://commons.wikimedia.org/wiki/Special:FilePath/" + encodeURIComponent(imageFileName);
                            // Crea un elemento img
                            img = document.createElement('img');
                            img.src = imageUrl;
                            img.style.position = 'absolute';
                            img.style.width = '10%'; // Ajusta el tamaño de la imagen según tus necesidades
                            img.style.display = 'none';
                            img.style.zIndex = 5000;
                            document.body.appendChild(img);
                        }
                    });

                data.locales.forEach(function(result) {
                    if(result.lat < 43.75 && result.lat > 27.75 && result.long < 4.75 && result.long > -18.75){
                        // Crear un marcador en el mapa con las coordenadas
                        var marker = L.marker([result.lat, result.long]).addTo(markersLayer);
                        marker.bindPopup(`
                            <strong>Local:</strong> ${result.rotulo} <br>
                            <strong>Distrito:</strong> <a href="${result.sameAsNombreDistrito}" target="_blank">${selectedStreet}</a> <br>
                            <strong>Situación:</strong> ${result.situacion} <br>
                            <strong>Lat, long:</strong> ${result.lat},${result.long} <br>
                            <strong>HoraApertura:</strong> ${result.horaApertura} horas <br>
                            <strong>HoraCierre:</strong> ${result.horaCierre} horas <br>
                            <strong>Terraza:</strong>
                            <ul>
                                <li><strong>sillas:</strong> ${result.sillas}</li>
                                <li><strong>mesas:</strong> ${result.mesas}</li>
                                <li><strong>superficie:</strong> ${result.superficie} m<sup>2</sup></li>
                            </ul>
                        `).on('popupopen', function() {
                            var link = document.querySelector('.leaflet-popup-content a');
                        
                            // Muestra la imagen cuando el ratón se coloca sobre el enlace
                            link.addEventListener('mouseover', function(event) {
                                img.style.display = 'block';
                                img.style.left = (event.pageX+15) + 'px';
                                img.style.top = (event.pageY+15) + 'px';
                            });
                        
                            // Oculta la imagen cuando el ratón se aleja del enlace
                            link.addEventListener('mouseout', function() {
                                img.style.display = 'none';
                            });
                        });

                        var autocompleteResults = $('#autocomplete-results');
                        autocompleteResults.empty();
                        // Añadir las coordenadas del marcador al array
                        markerCoords.push([parseFloat(result.lat), parseFloat(result.long)]);

                        // Mostrar la URL al hacer clic en el marcador
                        marker.on('click', function() {
                            $('#local-url').html('<a href="' + result.local + '" target="_blank">Ver más información</a>');
                        });
                        map.on('click', function() {
                            $('#local-url').empty(); // Borra la URL al hacer clic en otro lugar del mapa
                        });
                        $('#street-input').on('click', function() {
                            $('#local-url').empty(); // Borra la URL al hacer clic en otro lugar del mapa
                        });
                    }
                });
                // Calcular la media de las coordenadas de los marcadores
                var avgLat = markerCoords.reduce(function(sum, coord) {
                    return sum + coord[0];
                }, 0) / markerCoords.length;
                var avgLng = markerCoords.reduce(function(sum, coord) {
                    return sum + coord[1];
                }, 0) / markerCoords.length;
                // Centrar el mapa en la media de las coordenadas
                // Supongamos que este código se ejecuta después de que el distrito haya cargado
                loadingText.textContent = 'Ha cargado el distrito ' + selectedStreet;
                map.setView([avgLat, avgLng], 13);
                setTimeout(function() {
                    $('#correct-bar').css('display', 'block');
                    $('#correct-bar').css('animation', 'none');
                    $('#autocomplete-select').css('display', 'block');
                    $('#search-box').css('display', 'block');
                    setTimeout(function() {
                        var loadingBar = document.getElementById('loading-bar');
                        loadingBar.classList.add('hidden');
                        setTimeout(function() {
                            $('#correct-bar').css('animation', 'fadeOut 1s forwards');
                            setTimeout(function() {
                                $('#correct-bar').css('display', 'none');
                                loadingText.textContent = 'Cargando...';
                            }, 1000);
                        }, 5000);
                    }, 1000);
                }, 1000);

            },
            error: function() {
                // Borrar marcadores anteriores
                markersLayer.clearLayers();
                console.error('Error en la solicitud AJAX');
            }
        });
    });
});
