// URL de l'API backend
const API_URL = '/api/weather';

// Sélection des éléments du DOM
const cityInput = document.querySelector('.city-input');
const searchBtn = document.querySelector('.search-btn');
const weatherInfoSection = document.querySelector('.weather-info');
const searchCitySection = document.querySelector('.search-city');
const notFoundSection = document.querySelector('.not-found');
const loadingSection = document.querySelector('.loading-section');

const countryTxt = document.querySelector('.country-txt');
const currentDateTxt = document.querySelector('.current-date-txt');
const tempTxt = document.querySelector('.temp-txt');
const conditionTxt = document.querySelector('.condition-txt');
const weatherSummaryImg = document.querySelector('.weather-summary-img');
const forecastItemsContainer = document.querySelector('.forecast-items-container');

// Fonction qui crée l'animation de pluie dans le loader
function initRain() {
    const rainContainer = document.getElementById('rainContainer');
    rainContainer.innerHTML = '';
    // Création de 20 gouttes de pluie avec des positions et timings aléatoires
    for (let i = 0; i < 20; i++) {
        const drop = document.createElement('div');
        drop.className = 'raindrop';
        drop.style.left = (Math.random() * 92 + 10) + 'px';
        drop.style.animationDuration = (Math.random() * 0.5 + 0.4) + 's';
        drop.style.animationDelay = (Math.random() * 2) + 's';
        rainContainer.appendChild(drop);
    }
}

// Événement au clic sur le bouton de recherche
searchBtn.addEventListener('click', () => {
    if (cityInput.value.trim() !== '') handleWeatherSearch(cityInput.value);
});

// Événement sur la touche Entrée dans le champ de saisie
cityInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && cityInput.value.trim() !== '') handleWeatherSearch(cityInput.value);
});

// Fonction qui gère la recherche météo d'une ville
async function handleWeatherSearch(city) {
    // Affiche la section de chargement
    showDisplaySection(loadingSection);
    initRain();

    try {
        // Appel POST à l'API pour récupérer les données météo
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ city: city })
        });

        const result = await response.json();

        // Si des données sont retournées, met à jour l'interface
        if (result.status === 'success' && result.data.length > 0) {
            updateWeatherUI(result.data);
            showDisplaySection(weatherInfoSection);
            cityInput.value = '';
        } else {
            showDisplaySection(notFoundSection);
        }
    } catch (error) {
        console.error("Erreur Backend:", error);
        showDisplaySection(notFoundSection);
    }
}

// Fonction qui met à jour l'interface avec les données météo
function updateWeatherUI(data) {
    const today = data[0];
    // Mise à jour des informations du jour actuel
    countryTxt.textContent = today.ville;
    tempTxt.textContent = `${Math.round(today.temp_max)} °C`;
    conditionTxt.textContent = today.etat;
    
    // Formatage et affichage de la date actuelle
    const options = { weekday: 'short', day: '2-digit', month: 'short' };
    currentDateTxt.textContent = new Date().toLocaleDateString('en-GB', options);
    weatherSummaryImg.src = `weather/${getWeatherIcon(today.etat)}`;

    // Mise à jour des prévisions des 7 prochains jours
    forecastItemsContainer.innerHTML = '';
    const cityData = data.filter(d => d.ville === today.ville).slice(0, 7);

    // Création d'une carte pour chaque jour
    cityData.forEach(day => {
        const dateFormatted = new Date(day.date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short' });
        const forecastHtml = `
            <div class="forecast-item">
                <h5 class="forecast-item-date regular-txt">${dateFormatted}</h5>
                <img src="weather/${getWeatherIcon(day.etat)}" class="forecast-img">
                <div class="forecast-item-temp-container">
                    <h5 class="forecast-item-temp-max">${Math.round(day.temp_max)} °C</h5>
                    <hr class="temp-separator">
                    <h5 class="forecast-item-temp-min regular-txt">${Math.round(day.temp_min)} °C</h5>
                </div>
            </div>`;
        forecastItemsContainer.insertAdjacentHTML('beforeend', forecastHtml);
    });
}

// Fonction qui retourne l'icône appropriée selon la condition météo
function getWeatherIcon(condition) {
    if (!condition) return 'clouds.svg';
    const c = condition.toLowerCase();
    if (c.includes('orage') || c.includes('thunderstorm')) return 'thunderstorm.svg';
    if (c.includes('bruine') || c.includes('drizzle')) return 'drizzle.svg';
    if (c.includes('pluie') || c.includes('rain')) return 'rain.svg';
    if (c.includes('neige') || c.includes('snow')) return 'snow.svg';
    if (c.includes('clair') || c.includes('clear')) return 'clear.svg';
    if (c.includes('brouillard') || c.includes('mist')) return 'atmosphere.svg';
    return 'clouds.svg'; 
}

// Fonction qui affiche uniquement la section demandée et cache les autres
function showDisplaySection(section) {
    [weatherInfoSection, searchCitySection, notFoundSection, loadingSection].forEach(s => s.style.display = 'none');
    if (section) section.style.display = 'flex';
}

// Au chargement de la page, affiche la dernière ville recherchée si disponible
window.onload = async () => {
    try {
        // Récupère toutes les données stockées
        const response = await fetch(API_URL);
        const result = await response.json();
        // Si des données existent, affiche la dernière ville recherchée
        if (result.status === 'success' && result.data.length > 0) {
            const lastCity = result.data[result.data.length - 1].ville;
            updateWeatherUI(result.data.filter(d => d.ville === lastCity));
            showDisplaySection(weatherInfoSection);
        }
    } catch (e) {
        // Si aucune donnée, affiche l'écran de recherche
        showDisplaySection(searchCitySection);
    }
};