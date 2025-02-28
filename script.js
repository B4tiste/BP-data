document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll('.card');
    const gridContainer = document.getElementById("grid-container");
    const detailView = document.getElementById("detail-view");
    const detailImg = document.getElementById("detail-img");
    const detailCaption = document.getElementById("detail-caption");
    const backButton = document.getElementById("back-button");
    const searchInput = document.getElementById('monster-search');
    const searchButton = document.getElementById('search-button');
    const resetButton = document.getElementById('reset-button');

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

    // Charger le fichier JSON contenant les dates associées aux monstres
    fetch('monster_dates.json')
        .then(response => response.json())
        .then(monsterDates => {

            // Fonction qui convertit une date "DD/MM/YYYY" en format "DD mois YYYY"
            function formatDate(dateStr) {
                const parts = dateStr.split('/');
                // Création d'un objet Date (les mois commencent à 0)
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
                searchValue = searchValue.replace(/&/g, 'and').replace(/et/g, 'and');
                const lowerCaseMonsterDates = Object.keys(monsterDates).reduce((acc, key) => {
                    acc[key.toLowerCase()] = monsterDates[key];
                    return acc;
                }, {});

                if (searchValue in lowerCaseMonsterDates) {
                    // Récupérer et formater les dates associées au monstre recherché
                    const dates = lowerCaseMonsterDates[searchValue];
                    const formattedDates = dates.map(dateStr => formatDate(dateStr));

                    // Afficher uniquement les cards dont data-date correspond à une des dates
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

            // Événement lors du clic sur le bouton de recherche
            searchButton.addEventListener('click', searchMonsters);

            // Événement lors de l'appui sur la touche ENTREE dans le champ de recherche
            searchInput.addEventListener('keydown', function (event) {
                if (event.key === 'Enter') {
                    searchMonsters();
                }
            });

            // Bouton pour réinitialiser et afficher toutes les cards
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
