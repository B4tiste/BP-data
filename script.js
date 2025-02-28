document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll('.card');
    const gridContainer = document.getElementById("grid-container");
    const detailView = document.getElementById("detail-view");
    const detailImg = document.getElementById("detail-img");
    const detailCaption = document.getElementById("detail-caption");
    const backButton = document.getElementById("back-button");
    const toggleNegativeButton = document.getElementById('toggle-negative-button');
    const searchInput = document.getElementById('monster-search');
    const searchButton = document.getElementById('search-button');
    const resetButton = document.getElementById('reset-button');

    // Affichage de la vue détaillée lors du clic sur une card
    cards.forEach(card => {
        card.addEventListener("click", function () {
            const imgSrc = card.getAttribute("data-image");
            const date = card.getAttribute("data-date");
            detailImg.src = imgSrc;
            detailCaption.innerHTML = "Balance Patch - " + date;
            gridContainer.style.display = "none";
            detailView.style.display = "block";
            // Par défaut, on s'assure que l'image est en mode négatif
            detailImg.style.filter = "invert(1)";
            toggleNegativeButton.textContent = "Voir original";
        });
    });

    // Bouton retour
    backButton.addEventListener("click", function () {
        detailView.style.display = "none";
        gridContainer.style.display = "block";
    });

    // Bouton pour basculer l'affichage du filtre négatif
    toggleNegativeButton.addEventListener("click", function() {
        if (detailImg.style.filter === 'invert(1)') {
            detailImg.style.filter = 'none';
            toggleNegativeButton.textContent = "Afficher négatif";
        } else {
            detailImg.style.filter = 'invert(1)';
            toggleNegativeButton.textContent = "Voir original";
        }
    });

    // Charger le fichier JSON contenant les dates associées aux monstres
    fetch('monster_dates.json')
        .then(response => response.json())
        .then(monsterDates => {

            // Fonction qui convertit une date "DD/MM/YYYY" en format "DD mois YYYY"
            function formatDate(dateStr) {
                const parts = dateStr.split('/');
                const dateObj = new Date(parts[2], parts[1] - 1, parts[0]);
                return dateObj.toLocaleDateString('fr-FR', {
                    day: '2-digit',
                    month: 'long',
                    year: 'numeric'
                });
            }

            // Fonction de recherche
            function searchMonsters() {
                let searchValue = searchInput.value.trim().toLowerCase();
                searchValue = searchValue.replace(/ & /g, ' and ').replace(/ et /g, ' and ');
                const lowerCaseMonsterDates = Object.keys(monsterDates).reduce((acc, key) => {
                    acc[key.toLowerCase()] = monsterDates[key];
                    return acc;
                }, {});

                if (searchValue in lowerCaseMonsterDates) {
                    const dates = lowerCaseMonsterDates[searchValue];
                    const formattedDates = dates.map(dateStr => formatDate(dateStr));

                    document.querySelectorAll('.card').forEach(card => {
                        const cardDate = card.getAttribute('data-date');
                        if (formattedDates.includes(cardDate)) {
                            card.style.display = 'block';
                        } else {
                            card.style.display = 'none';
                        }
                    });
                } else {
                    alert("Monstre non trouvé !");
                }
            }

            // Recherche sur clic et sur appui sur ENTREE
            searchButton.addEventListener('click', searchMonsters);
            searchInput.addEventListener('keydown', function (event) {
                if (event.key === 'Enter') {
                    searchMonsters();
                }
            });

            // Réinitialisation de la recherche
            resetButton.addEventListener('click', function () {
                searchInput.value = '';
                document.querySelectorAll('.card').forEach(card => {
                    card.style.display = 'block';
                });
            });
        })
        .catch(error => {
            console.error('Erreur lors du chargement du fichier JSON:', error);
        });
});
