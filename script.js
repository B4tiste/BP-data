document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll('.card');
    const gridContainer = document.getElementById("grid-container");
    const detailView = document.getElementById("detail-view");
    const detailImg = document.getElementById("detail-img");
    const detailCaption = document.getElementById("detail-caption");
    const backButton = document.getElementById("back-button");

    cards.forEach(card => {
        card.addEventListener("click", function () {
            const imgSrc = card.getAttribute("data-image");
            const date = card.getAttribute("data-date");
            detailImg.src = imgSrc;
            detailCaption.innerHTML = "Balance Patch - " + date;
            gridContainer.style.display = "none";
            detailView.style.display = "block";
        });
    });

    backButton.addEventListener("click", function () {
        detailView.style.display = "none";
        gridContainer.style.display = "block";
    });
});
