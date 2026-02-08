let siteData = null;

// Початкове значення лічильника (зберігається в браузері)
let totalSaved = parseInt(localStorage.getItem('totalSaved')) || 124500;

// --- ЗАВАНТАЖЕННЯ ---
async function loadData() {
    try {
        const response = await fetch('data.json');
        siteData = await response.json();
        
        applySavedSettings();
        initCustomMenu();
        renderSite();
        updateCounter(0); 
        
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('sw.js').catch(() => {});
        }
    } catch (e) { 
        console.error("Data loading error:", e); 
    }
}

// --- ЛІЧИЛЬНИК ---
function updateCounter(add) {
    totalSaved += add;
    localStorage.setItem('totalSaved', totalSaved);
    const counterEl = document.getElementById('moneyCounter');
    if (counterEl) {
        counterEl.innerText = totalSaved.toLocaleString();
    }
}

// --- РЕНДЕРИНГ ---
function renderSite() {
    const lang = localStorage.getItem('lang') || 'UA';
    const info = siteData.languages[lang] || siteData.languages['UA'];
    const container = document.getElementById('siteContent');
    
    if (!container) return;
    container.innerHTML = '';

    // Оновлення текстів інтерфейсу
    document.getElementById('mainTitle').innerText = info.title;
    document.getElementById('mainDesc').innerText = info.desc;
    document.getElementById('searchInput').placeholder = info.search_placeholder || "Search...";
    document.getElementById('seoContent').innerHTML = info.seo_text || "";
    document.getElementById('donateTitle').innerText = info.donate_t;
    document.getElementById('donateDesc').innerText = info.donate_d;
    document.getElementById('donateBtn').innerText = info.donate_b;
    document.getElementById('modalTitle').innerText = info.feedback_title || "Add service";
    document.getElementById('modalDesc').innerText = info.feedback_desc || "";
    document.getElementById('modalBtn').innerText = info.feedback_btn || "Send";

    // Групування за категоріями
    const groups = {};
    siteData.services.forEach(service => {
        // Якщо тип сервісу збігається з мовою (UA/EN), кидаємо в Local
        let catKey = (service.type === lang) ? 'local' : (service.category || 'other');
        if (!groups[catKey]) groups[catKey] = [];
        groups[catKey].push(service);
    });

    // Сортування: спочатку локальні, потім решта
    const sortedCats = Object.keys(groups).sort((a, b) => a === 'local' ? -1 : 1);

    sortedCats.forEach(catKey => {
        const wrapper = document.createElement('div');
        // Локальні розгорнуті за замовчуванням
        wrapper.className = `category-wrapper ${catKey === 'local' ? 'active' : ''}`;
        
        const catTitle = info[`cat_${catKey}`] || catKey.toUpperCase();

        wrapper.innerHTML = `
            <div class="category-header" onclick="this.parentElement.classList.toggle('active')">
                <span>${catTitle} (${groups[catKey].length})</span>
                <span class="arrow-cat">▼</span>
            </div>
            <div class="category-content">
                ${groups[catKey].map(s => `
                    <a href="${s.url}" class="card" target="_blank" onclick="updateCounter(${s.price || 200})">
                        <img src="${s.img}" alt="${s.name} cancellation" loading="lazy" onerror="this.src='https://cdn-icons-png.flaticon.com/512/1055/1055183.png'">
                        <div>${s.name}</div>
                    </a>
                `).join('')}
            </div>
        `;
        container.appendChild(wrapper);
    });
}

// --- ПОШУК (БЕЗ акордеонів для зручності) ---
function filterServices() {
    const query = document.getElementById('searchInput').value.toLowerCase().trim();
    const container = document.getElementById('siteContent');
    const lang = localStorage.getItem('lang') || 'UA';
    const info = siteData.languages[lang];

    if (!query) {
        renderSite();
        return;
    }

    const matches = siteData.services.filter(s => s.name.toLowerCase().includes(query));
    container.innerHTML = '';

    if (matches.length > 0) {
        const grid = document.createElement('div');
        grid.className = 'category-content';
        grid.style.display = 'grid'; // Показуємо сітку при пошуку
        matches.forEach(s => {
            grid.innerHTML += `
                <a href="${s.url}" class="card" target="_blank" onclick="updateCounter(${s.price || 200})">
                    <img src="${s.img}" alt="${s.name}">
                    <div>${s.name}</div>
                </a>`;
        });
        container.appendChild(grid);
    } else {
        container.innerHTML = `<p style="text-align:center; opacity:0.5; margin-top:20px;">${info.search_not_found || "Not found"}</p>`;
    }
}

// --- МЕНЮ МОВ ТА ТЕМА ---
function initCustomMenu() {
    const list = document.getElementById('dropdownList');
    if (!list) return;
    list.innerHTML = '';
    Object.keys(siteData.languages).forEach(code => {
        const item = document.createElement('div');
        item.className = 'select-item';
        item.innerHTML = `<img src="flags/${code}.png" class="flag-icon"><span>${siteData.languages[code].label}</span>`;
        item.onclick = () => {
            localStorage.setItem('lang', code);
            updateVisuals(code);
            renderSite();
            document.getElementById('dropdownList').classList.remove('active');
        };
        list.appendChild(item);
    });
    updateVisuals(localStorage.getItem('lang') || 'UA');
}

function updateVisuals(code) {
    document.getElementById('currentFlag').src = `flags/${code}.png`;
    document.getElementById('currentShort').innerText = siteData.languages[code]?.short || code;
}

function toggleMenu() {
    document.getElementById('dropdownList').classList.toggle('active');
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    document.getElementById('themeBtn').innerText = next === 'dark' ? '☀️' : '🌙';
}

function applySavedSettings() {
    const theme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    document.getElementById('themeBtn').innerText = theme === 'dark' ? '☀️' : '🌙';
}

function toggleModal() {
    document.getElementById('feedbackModal').classList.toggle('active');
}

function closeModalOutside(e) {
    if (e.target.id === 'feedbackModal') toggleModal();
}

// Закриття меню
document.addEventListener('click', (e) => {
    if (!document.getElementById('langSelector').contains(e.target)) {
        document.getElementById('dropdownList').classList.remove('active');
    }
});

loadData();
