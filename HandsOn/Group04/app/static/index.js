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
    let allItemDetails = document.getElementsByClassName("item-details-outer");
    for (let itemDetails of allItemDetails) {
        if (itemDetails == this.nextElementSibling) {
            /* for the details of the clicked item */
            if (itemDetails.style.maxHeight && itemDetails.style.maxHeight != "0px") {
                /* if item was expanded, collapse it (and rotate icon to original position) */
                itemDetails.classList.remove("active");
                this.firstElementChild.firstElementChild.firstElementChild.style.transform = "rotate(0deg)";
                itemDetails.style.padding = null;
                itemDetails.style.maxHeight = null;
            }
            else {
                /* if item was collapsed, expand it (and rotate icon) */
                this.firstElementChild.firstElementChild.firstElementChild.style.transform = "rotate(180deg)";
                itemDetails.classList.add("active");
                itemDetails.style.padding = "20px";
                itemDetails.style.maxHeight = itemDetails.scrollHeight + "px";
            }
        }
        else {
           /* for the rest of the items, collapse/keep collapsed (and rotate icon if the item was active) */
           if ((itemDetails.classList.contains("active"))) {
               itemDetails.previousElementSibling.firstElementChild.firstElementChild.firstElementChild.style.transform = "rotate(0deg)";
               itemDetails.classList.remove("active");
           }
            itemDetails.style.paddingTop = "0px";
            itemDetails.style.paddingBottom = "0px";
            itemDetails.style.maxHeight = "0px";
        }
    }
}