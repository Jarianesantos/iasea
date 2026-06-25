// Dados padrão (serão substituídos pelo fetch se disponível)
let appData = {
    monthly: {
        labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
        co2: [820, 850, 880, 840, 860, 830, 810, 800, 790, 780, 770, 760],
        reduction: [5, 3, 2, 6, 4, 7, 8, 9, 10, 11, 12, 15]
    },
    strategies: [
        {name: 'Otimização de Rota', reduction: 12.5},
        {name: 'Manutenção de Motores', reduction: 8.3},
        {name: 'Combustível Alternativo', reduction: 25.0},
        {name: 'Redução de Velocidade', reduction: 15.0},
        {name: 'Sistema de Propulsão', reduction: 18.0}
    ],
    fuel: {
        labels: ['MGO', 'HFO', 'Outros'],
        values: [450, 600, 50],
        colors: ['#3b82f6', '#6b7280', '#9ca3af']
    }
};

// Buscar dados da API
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        if (response.ok) {
            appData = await response.json();
            initCharts();
        }
    } catch (error) {
        console.log('Usando dados padrão:', error);
        initCharts();
    }
}

// Generate realtime data
function generateRealtimeData() {
    const now = new Date();
    const data = [];
    for (let i = 0; i < 24; i++) {
        const time = new Date(now);
        time.setHours(now.getHours() - (23 - i));
        data.push({
            time: time.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
            co2: 35 + Math.random() * 15
        });
    }
    return data;
}

// Initialize Charts
function initCharts() {
    const realtimeData = generateRealtimeData();

    // Monthly Chart
    new Chart(document.getElementById('monthlyChart'), {
        type: 'line',
        data: {
            labels: appData.monthly.labels,
            datasets: [{
                label: 'CO2 (toneladas)',
                data: appData.monthly.co2,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: false, grid: { color: '#e5e7eb' }, ticks: { color: '#6b7280' } },
                x: { grid: { color: '#e5e7eb' }, ticks: { color: '#6b7280' } }
            }
        }
    });

    // Strategies Chart
    new Chart(document.getElementById('strategiesChart'), {
        type: 'bar',
        data: {
            labels: appData.strategies.map(s => s.name),
            datasets: [{
                label: 'Redução (%)',
                data: appData.strategies.map(s => s.reduction),
                backgroundColor: ['#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe'],
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { beginAtZero: true, grid: { color: '#e5e7eb' }, ticks: { color: '#6b7280' } },
                y: { grid: { color: '#e5e7eb' }, ticks: { color: '#6b7280' } }
            }
        }
    });

    // Realtime Chart
    new Chart(document.getElementById('realtimeChart'), {
        type: 'line',
        data: {
            labels: realtimeData.map(d => d.time),
            datasets: [{
                label: 'CO2 (kg/h)',
                data: realtimeData.map(d => d.co2),
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: '#e5e7eb' }, ticks: { color: '#6b7280' } },
                x: { grid: { display: false }, ticks: { color: '#6b7280', maxRotation: 45, minRotation: 45 } }
            }
        }
    });

    // Update realtime grid
    const grid = document.getElementById('realtime-grid');
    if (grid) {
        grid.innerHTML = '';
        realtimeData.slice(-4).forEach(data => {
            const item = document.createElement('div');
            item.className = 'realtime-item';
            item.innerHTML = `
                <p class="realtime-time">${data.time}</p>
                <p class="realtime-value">${data.co2.toFixed(1)} kg/h</p>
            `;
            grid.appendChild(item);
        });
    }

    // Update metrics
    updateMetrics();
}

function updateMetrics() {
    const historicalData = appData.monthly.co2;
    const totalCO2 = historicalData.reduce((sum, item) => sum + item, 0);
    const monthlyCO2 = totalCO2 / historicalData.length;
    const annualProjection = monthlyCO2 * 12;
    const baseline = 8500;
    const reductionFromBaseline = ((baseline - annualProjection) / baseline) * 100;

    document.getElementById('annual-emissions').textContent = annualProjection.toFixed(0);
    document.getElementById('reduction-percent').textContent = reductionFromBaseline.toFixed(1);
}

// Page Navigation
function showPage(page) {
    document.getElementById('dashboard-page').style.display = 'none';
    document.getElementById('analytics-page').style.display = 'none';
    document.getElementById('vessel-page').style.display = 'none';
    document.getElementById(`${page}-page`).style.display = 'block';
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchData();
    showPage('dashboard');
});