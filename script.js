document.addEventListener("DOMContentLoaded", function () {
    // Get tab elements
    const galleryTab = document.getElementById("gallery-tab");
    const statsTab = document.getElementById("stats-tab");
    const listTab = document.getElementById("list-tab");
    const aboutTab = document.getElementById("about-tab");

    // Get container elements
    const galleryContainer = document.getElementById("gallery-container");
    const statsContainer = document.getElementById("stats-container");
    const listContainer = document.getElementById("list-container");
    const aboutContainer = document.getElementById("about-container");

    // Onglet Gallery
    galleryTab.addEventListener("click", function () {
        galleryContainer.style.display = "block";
        statsContainer.style.display = "none";
        listContainer.style.display = "none";
        aboutContainer.style.display = "none";
        galleryTab.classList.add("active");
        statsTab.classList.remove("active");
        listTab.classList.remove("active");
        aboutTab.classList.remove("active");
    });

    // Onglet Stats
    statsTab.addEventListener("click", function () {
        galleryContainer.style.display = "none";
        statsContainer.style.display = "block";
        listContainer.style.display = "none";
        aboutContainer.style.display = "none";
        statsTab.classList.add("active");
        galleryTab.classList.remove("active");
        listTab.classList.remove("active");
        aboutTab.classList.remove("active");
    });

    // Onglet List
    listTab.addEventListener("click", function () {
        galleryContainer.style.display = "none";
        statsContainer.style.display = "none";
        listContainer.style.display = "block";
        aboutContainer.style.display = "none";
        listTab.classList.add("active");
        galleryTab.classList.remove("active");
        statsTab.classList.remove("active");
        aboutTab.classList.remove("active");
    });

    // Nouvel onglet About Me
    aboutTab.addEventListener("click", function () {
        galleryContainer.style.display = "none";
        statsContainer.style.display = "none";
        listContainer.style.display = "none";
        aboutContainer.style.display = "block";
        aboutTab.classList.add("active");
        galleryTab.classList.remove("active");
        statsTab.classList.remove("active");
        listTab.classList.remove("active");
    });

    // Gestion des cards et de la vue détaillée
    const cards = document.querySelectorAll('.card');
    const gridContainer = document.getElementById("grid-container");
    const detailView = document.getElementById("detail-view");
    const detailImg = document.getElementById("detail-img");
    const detailCaption = document.getElementById("detail-caption");
    const backButton = document.getElementById("back-button");
    const toggleNegativeButton = document.getElementById("toggle-negative-button");

    cards.forEach(card => {
        card.addEventListener("click", function () {
            const imgSrc = card.getAttribute("data-image");
            const date = card.getAttribute("data-date");
            detailImg.src = imgSrc;
            detailCaption.innerHTML = "Balance Patch - " + date;
            gridContainer.style.display = "none";
            detailView.style.display = "block";
            // On s'assure que l'image est affichée en mode négatif par défaut
            detailImg.style.filter = "invert(1)";
            toggleNegativeButton.textContent = "Show white picture";
        });
    });

    backButton.addEventListener("click", function () {
        detailView.style.display = "none";
        gridContainer.style.display = "block";
    });

    toggleNegativeButton.addEventListener("click", function () {
        if (detailImg.style.filter === "invert(1)") {
            detailImg.style.filter = "none";
            toggleNegativeButton.textContent = "Show dark picture";
        } else {
            detailImg.style.filter = "invert(1)";
            toggleNegativeButton.textContent = "Show white picture";
        }
    });

    // Fonctionnalités de recherche
    const searchInput = document.getElementById("monster-search");
    const searchButton = document.getElementById("search-button");
    const resetButton = document.getElementById("reset-button");
    const searchResultsElement = document.getElementById("search-results");

    fetch("monster_dates.json")
        .then(response => response.json())
        .then(monsterDates => {
            // Fonction qui formate une date "DD/MM/YYYY"
            function formatDate(dateStr) {
                const parts = dateStr.split("/");
                const dateObj = new Date(parts[2], parts[1] - 1, parts[0]);
                return dateObj.toLocaleDateString("fr-FR", {
                    day: "2-digit",
                    month: "2-digit",
                    year: "numeric"
                });
            }

            // Fonction de recherche qui filtre les cartes en fonction du monstre
            function searchMonsters() {
                let searchValue = searchInput.value.trim().toLowerCase();
                searchValue = searchValue.replace(/ & /g, " and ").replace(/ et /g, " and ");
                const lowerCaseMonsterDates = Object.keys(monsterDates).reduce((acc, key) => {
                    acc[key.toLowerCase()] = monsterDates[key];
                    return acc;
                }, {});

                if (searchValue in lowerCaseMonsterDates) {
                    const dates = lowerCaseMonsterDates[searchValue];
                    const formattedDates = dates.map(dateStr => formatDate(dateStr));

                    document.querySelectorAll(".card").forEach(card => {
                        const cardDate = card.getAttribute("data-date");
                        if (formattedDates.includes(cardDate)) {
                            card.style.display = "block";
                        } else {
                            card.style.display = "none";
                        }
                    });

                    const visibleCards = Array.from(document.querySelectorAll(".card"))
                        .filter(card => card.style.display !== "none").length;
                    searchResultsElement.textContent = `Search : ${searchInput.value} (${visibleCards} result${visibleCards > 1 ? "s" : ""})`;
                } else {
                    alert("Did not find any results for " + searchInput.value);
                    searchResultsElement.textContent = "";
                }
            }

            searchButton.addEventListener("click", searchMonsters);
            searchInput.addEventListener("keydown", function (event) {
                if (event.key === "Enter") {
                    searchMonsters();
                }
            });
            resetButton.addEventListener("click", function () {
                searchInput.value = "";
                document.querySelectorAll(".card").forEach(card => {
                    card.style.display = "block";
                });
                searchResultsElement.textContent = "";
            });

            // Ajout de l'événement sur chaque monstre dans l'onglet "Monsters List"
            document.querySelectorAll("#list-container li").forEach(li => {
                li.addEventListener("click", function () {
                    // Hide the detail view and show the gallery grid for search results.
                    detailView.style.display = "none";
                    gridContainer.style.display = "block";
                    // Remplit le champ de recherche avec le nom du monstre cliqué et déclenche la recherche
                    searchInput.value = li.innerText;
                    searchMonsters();
                    // Basculer vers l'onglet de la galerie pour afficher les résultats
                    galleryTab.click();
                });
            });
        })
        .catch(error => {
            console.error("Erreur lors du chargement du fichier JSON:", error);
        });

    // Boutons More/Less pour la section Stats
    const moreBpButton = document.getElementById("more-bp-button");
    if (moreBpButton) {
        moreBpButton.addEventListener("click", function () {
            const hiddenItems = document.querySelectorAll(".more-bp");
            hiddenItems.forEach(item => {
                if (item.style.display === "list-item") {
                    item.style.display = "none";
                    moreBpButton.textContent = "More";
                } else {
                    item.style.display = "list-item";
                    moreBpButton.textContent = "Less";
                }
            });
        });
    }

    const moreMonsterButton = document.getElementById("more-monster-button");
    if (moreMonsterButton) {
        moreMonsterButton.addEventListener("click", function () {
            const hiddenItems = document.querySelectorAll(".more-monsters");
            hiddenItems.forEach(item => {
                if (item.style.display === "list-item") {
                    item.style.display = "none";
                    moreMonsterButton.textContent = "More";
                } else {
                    item.style.display = "list-item";
                    moreMonsterButton.textContent = "Less";
                }
            });
        });
    }

    // Bouton More pour la colonne "Monsters Natural 5 (Not in Dates)"
    const moreCollabButton = document.getElementById("more-non-bp-button");
    if (moreCollabButton) {
        moreCollabButton.addEventListener("click", function () {
            const hiddenItems = document.querySelectorAll(".more-non-bp");
            hiddenItems.forEach(item => {
                if (item.style.display === "list-item") {
                    item.style.display = "none";
                    moreCollabButton.textContent = "More";
                } else {
                    item.style.display = "list-item";
                    moreCollabButton.textContent = "Less";
                }
            });
        });
    }

});
