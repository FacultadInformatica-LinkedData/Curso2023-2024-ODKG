if (document.readyState == "loading") {
    document.addEventListener("DOMContentLoaded", onDocumentReady);
} else {
    onDocumentReady();
}

function onDocumentReady() {
    let items = document.getElementsByClassName("item-outer");
    let search = document.getElementById("search");
    for (let item of items) {
        item.addEventListener("click", toggleItemDetails);
    }
    search.addEventListener("input", filterItemsByName);
}

function filterItemsByName() {
    console.log(1);
}

function toggleItemDetails() {
    const itemContainer = this.parentElement;
    const itemDetails = this.nextElementSibling;

    itemContainer.classList.toggle("active");

    const toggleIcon = itemContainer.querySelector('.toggle-icon img');

    if (itemContainer.classList.contains("active")) {
        // Mostrar detalles
        itemDetails.style.padding = "20px";
        itemDetails.style.maxHeight = itemDetails.scrollHeight + "px";
        toggleIcon.classList.add("rotate"); // Agrega la clase de rotación al ícono
    } else {
        // Ocultar detalles
        itemDetails.style.padding = null;
        itemDetails.style.maxHeight = null;
        toggleIcon.classList.remove("rotate"); // Elimina la clase de rotación del ícono
    }
}



// Función para alternar la visibilidad de los filtros
function toggleFilters() {
    var filtersContainer = document.querySelector('.filters');
    var filtersList = document.querySelector('.filters-list');

    filtersContainer.classList.toggle('hidden');
    filtersList.classList.toggle('hidden');

    // Obtener el botón de alternar filtros
    var toggleFiltersBtn = document.getElementById('toggle-filters-btn');

    // Actualizar el texto del botón en base al estado de los filtros
    if (filtersList.classList.contains('hidden')) {
        toggleFiltersBtn.textContent = 'Mostrar Filtros';
    } else {
        toggleFiltersBtn.textContent = 'Ocultar Filtros';
    }

}