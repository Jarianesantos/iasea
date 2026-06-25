import os
import sys

# Cria a pasta principal
project_name = "diamond-psv3300-carbon-monitor"
os.makedirs(project_name, exist_ok=True)
os.chdir(project_name)

# Cria as pastas
os.makedirs("templates", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)

# ===== requirements.txt =====
with open("requirements.txt", "w") as f:
    f.write("Flask==3.0.0\n")

# ===== app.py =====
app_py = """from flask import Flask, render_template

app = Flask(__name__)

DIAMOND_PSV3300 = {
    "vessel": {
        "name": "Diamond PSV 3300",
        "type": "Platform Supply Vessel",
        "length": 83.4,
        "breadth": 18.0,
        "draft": 6.0,
        "gross_tonnage": 3300,
        "deadweight": 3800,
        "engines": [
            {"name": "Main Engine 1", "type": "Wärtsilä 6L32", "power": 3000, "fuel_type": "MGO"},
            {"name": "Main Engine 2", "type": "Wärtsilä 6L32", "power": 3000, "fuel_type": "MGO"},
            {"name": "Auxiliary 1", "type": "Caterpillar C9", "power": 350, "fuel_type": "MGO"},
            {"name": "Auxiliary 2", "type": "Caterpillar C9", "power": 350, "fuel_type": "MGO"}
        ],
        "fuel_capacity": {"MGO": 450, "HFO": 600, "LNG": 0},
        "operational_profile": {
            "transit_speed": 12,
            "dp_speed": 2,
            "standby_consumption": 0.8
        }
    },
    "baseline_emissions": {
        "annual_co2": 8500,
        "annual_nox": 120,
        "annual_sox": 15,
        "annual_pm": 2.5
    }
}

@app.route('/')
def dashboard():
    return render_template('index.html',
                         vessel=DIAMOND_PSV3300['vessel'],
                         emissions=DIAMOND_PSV3300['baseline_emissions'])

@app.route('/api/data')
def get_data():
    from datetime import datetime, timedelta
    import random

    monthly_data = {
        "labels": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
        "co2": [820, 850, 880, 840, 860, 830, 810, 800, 790, 780, 770, 760],
        "reduction": [5, 3, 2, 6, 4, 7, 8, 9, 10, 11, 12, 15]
    }

    realtime_data = []
    now = datetime.now()
    for i in range(24):
        time = (now - timedelta(hours=23-i)).strftime("%H:%M")
        realtime_data.append({
            "time": time,
            "co2": round(35 + random.uniform(0, 15), 1),
            "fuel_flow": round(1.2 + random.uniform(0, 0.5), 2),
            "engine_load": round(65 + random.uniform(0, 20), 1)
        })

    ai_forecast = {
        "next_month": {"predicted_co2": 720, "confidence": 0.92, "trend": "descendente"},
        "next_quarter": {"predicted_co2": 2050, "confidence": 0.88, "trend": "descendente"},
        "annual_target": {"target": 6800, "current_projection": 7100, "gap": 300, "probability": 0.78}
    }

    strategies = [
        {"name": "Otimização de Rota", "reduction": 12.5, "cost": "Baixo", "implementation": "Imediato"},
        {"name": "Manutenção de Motores", "reduction": 8.3, "cost": "Médio", "implementation": "3 meses"},
        {"name": "Combustível Alternativo", "reduction": 25.0, "cost": "Alto", "implementation": "6 meses"},
        {"name": "Redução de Velocidade", "reduction": 15.0, "cost": "Baixo", "implementation": "Imediato"},
        {"name": "Sistema de Propulsão", "reduction": 18.0, "cost": "Alto", "implementation": "12 meses"},
        {"name": "Eficiência Energética", "reduction": 10.2, "cost": "Médio", "implementation": "2 meses"}
    ]

    return {
        "monthly": monthly_data,
        "realtime": realtime_data,
        "forecast": ai_forecast,
        "strategies": strategies,
        "fuel": {"labels": ["MGO", "HFO", "Outros"], "values": [450, 600, 50]}
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
"""

with open("app.py", "w") as f:
    f.write(app_py)

# ===== templates/index.html =====
index_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diamond PSV 3300 - Monitoramento de Carbono com IA</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div id="dashboard-page">
        <div class="container">
            <div class="header">
                <div>
                    <h1>{{ vessel.name }}</h1>
                    <p>Monitoramento de Carbono com IA</p>
                </div>
                <div class="header-actions">
                    <a href="#analytics-page" class="btn btn-primary" onclick="showPage('analytics')">Análises</a>
                    <a href="#vessel-page" class="btn btn-primary" onclick="showPage('vessel')">Navio</a>
                </div>
            </div>

            <div id="alerts-container" class="mb-6">
                <div class="alert alert-success">
                    <span>✅</span>
                    <div>
                        <p class="font-medium">Redução de 15% nas emissões este mês!</p>
                        <p class="text-xs" style="color: #6b7280; margin-top: 0.25rem;">25 Jun 2026, 10:30</p>
                    </div>
                </div>
                <div class="alert alert-warning">
                    <span>⚠️</span>
                    <div>
                        <p class="font-medium">Consumo de combustível acima do esperado</p>
                        <p class="text-xs" style="color: #6b7280; margin-top: 0.25rem;">25 Jun 2026, 09:15</p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-4 mb-8">
                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Emissões Anuais</div>
                            <div class="card-value"><span id="annual-emissions">7100</span><span class="card-unit">tCO2</span></div>
                        </div>
                        <span class="trend-badge trend-positive">+15.0%</span>
                    </div>
                </div>
                <div class="card gradient-bg">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Redução vs Baseline</div>
                            <div class="card-value"><span id="reduction-percent">15.3</span><span class="card-unit">%</span></div>
                        </div>
                        <span class="trend-badge trend-positive">+12.5%</span>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Meta Anual</div>
                            <div class="card-value"><span id="annual-target">{{ emissions.annual_co2 - 1500 }}</span><span class="card-unit">tCO2</span></div>
                        </div>
                        <span class="trend-badge trend-positive">+92%</span>
                    </div>
                    <div class="progress-container">
                        <div class="progress-label"><span>Progresso</span><span>92%</span></div>
                        <div class="progress-bar"><div class="progress-fill" style="width: 92%; background-color: var(--primary);"></div></div>
                    </div>
                </div>
                <div class="card" style="background: linear-gradient(135deg, #e0e7ff, #c7d2fe);">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Eficiência</div>
                            <div class="card-value"><span>A</span></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-2 mb-8">
                <div class="chart-container">
                    <h3>Emissões Mensais de CO2</h3>
                    <canvas id="monthlyChart"></canvas>
                </div>
                <div class="chart-container">
                    <h3>Estratégias de Redução</h3>
                    <canvas id="strategiesChart"></canvas>
                </div>
            </div>

            <div class="chart-container gradient-bg mb-8">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <h3>Previsões de IA</h3>
                    <span class="badge" style="background-color: #dbeafe; color: #1e40af;">Inteligência Artificial</span>
                </div>
                <div class="forecast-grid">
                    <div class="forecast-card">
                        <h4>Próximo Mês</h4>
                        <p class="forecast-value" style="color: var(--primary);">720 tCO2</p>
                        <p style="font-size: 0.875rem; color: var(--gray-500); margin-top: 0.5rem;">Confiança: 92%</p>
                    </div>
                    <div class="forecast-card">
                        <h4>Próximo Trimestre</h4>
                        <p class="forecast-value" style="color: var(--success);">2050 tCO2</p>
                        <p style="font-size: 0.875rem; color: var(--gray-500); margin-top: 0.5rem;">Confiança: 88%</p>
                    </div>
                    <div class="forecast-card">
                        <h4>Meta Anual</h4>
                        <p class="forecast-value" style="color: #8b5cf6;">6800 tCO2</p>
                        <div class="progress-container" style="margin-top: 0.75rem;">
                            <div class="progress-label"><span>Progresso</span><span>78%</span></div>
                            <div class="progress-bar"><div class="progress-fill" style="width: 78%; background-color: #8b5cf6;"></div></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="chart-container">
                <h3>Dados em Tempo Real</h3>
                <canvas id="realtimeChart"></canvas>
                <div class="realtime-grid" id="realtime-grid"></div>
            </div>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
"""

with open("templates/index.html", "w") as f:
    f.write(index_html)

# ===== static/css/style.css =====
style_css = """/* CSS do projeto - cole aqui o conteúdo do style.css que já te passei */
:root {
    --primary: #3b82f6;
    --primary-dark: #1d4ed8;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-500: #6b7280;
    --gray-600: #4b5563;
    --gray-700: #374151;
    --gray-900: #111827;
    --white: #ffffff;
    --shadow: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
    --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: var(--gray-50);
    color: var(--gray-900);
}

.container { max-width: 1400px; margin: 0 auto; padding: 1.5rem; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.header h1 { font-size: 1.875rem; font-weight: 700; }
.header p { color: var(--gray-500); margin-top: 0.25rem; }
.header-actions { display: flex; gap: 0.75rem; }
.btn { padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.875rem; font-weight: 500; text-decoration: none; display: inline-flex; align-items: center; gap: 0.5rem; transition: all 0.2s; border: none; cursor: pointer; }
.btn-primary { background-color: var(--white); color: var(--gray-700); box-shadow: var(--shadow); }
.btn-primary:hover { background-color: var(--gray-50); }
.btn-back { background-color: var(--primary); color: var(--white); }
.btn-back:hover { background-color: var(--primary-dark); }
.alert { padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.75rem; display: flex; align-items: flex-start; gap: 0.75rem; animation: slideIn 0.3s ease-out; }
@keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.alert-success { background-color: #dcfce7; border: 1px solid #bbf7d0; color: #166534; }
.alert-warning { background-color: #fef3c7; border: 1px solid #fde68a; color: #92400e; }
.card { background-color: var(--white); border-radius: 0.75rem; box-shadow: var(--shadow); padding: 1.5rem; transition: transform 0.2s, box-shadow 0.2s; }
.card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.card-title { font-size: 0.875rem; font-weight: 600; color: var(--gray-500); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
.card-value { font-size: 1.875rem; font-weight: 700; color: var(--gray-900); }
.card-unit { font-size: 0.875rem; color: var(--gray-500); font-weight: 400; }
.trend-badge { padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.trend-positive { background-color: #dcfce7; color: #166534; }
.grid { display: grid; gap: 1.5rem; }
.grid-cols-1 { grid-template-columns: 1fr; }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
@media (max-width: 1024px) { .grid-cols-4 { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .grid-cols-2, .grid-cols-4 { grid-template-columns: 1fr; } }
.progress-container { margin-top: 0.75rem; }
.progress-label { display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--gray-600); margin-bottom: 0.25rem; }
.progress-bar { height: 0.5rem; background-color: var(--gray-200); border-radius: 9999px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 9999px; transition: width 1s ease-out; }
.chart-container { background-color: var(--white); border-radius: 0.75rem; box-shadow: var(--shadow); padding: 1.5rem; margin-bottom: 1.5rem; }
.chart-container h3 { font-size: 1.125rem; font-weight: 600; color: var(--gray-900); margin-bottom: 1.5rem; }
.vessel-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
.vessel-stat { text-align: center; padding: 1rem; background-color: var(--gray-50); border-radius: 0.5rem; }
.vessel-stat-value { font-size: 1.5rem; font-weight: 700; color: var(--primary); }
.vessel-stat-label { font-size: 0.75rem; color: var(--gray-500); margin-top: 0.25rem; }
.table-container { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid var(--gray-200); }
th { background-color: var(--gray-50); font-size: 0.75rem; font-weight: 600; color: var(--gray-500); text-transform: uppercase; letter-spacing: 0.05em; }
tr:hover { background-color: var(--gray-50); }
.forecast-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
.forecast-card { background-color: var(--white); border-radius: 0.5rem; padding: 1rem; border: 1px solid var(--gray-200); }
.forecast-card h4 { font-size: 0.75rem; font-weight: 600; color: var(--gray-500); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
.forecast-value { font-size: 1.5rem; font-weight: 700; }
.realtime-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 0.75rem; margin-top: 1rem; }
.realtime-item { text-align: center; padding: 0.75rem; background-color: var(--gray-50); border-radius: 0.5rem; }
.realtime-time { font-size: 0.75rem; color: var(--gray-500); }
.realtime-value { font-size: 1.125rem; font-weight: 700; color: var(--primary); }
.badge { display: inline-flex; align-items: center; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 500; }
.badge-low { background-color: #dcfce7; color: #166534; }
.badge-medium { background-color: #fef3c7; color: #92400e; }
.badge-high { background-color: #fee2e2; color: #991b1b; }
.gradient-bg { background: linear-gradient(135deg, #dbeafe, #e0e7ff); }
"""

with open("static/css/style.css", "w") as f:
    f.write(style_css)

# ===== static/js/script.js =====
script_js = """// Dados padrão
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

function initCharts() {
    const realtimeData = generateRealtimeData();

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

function showPage(page) {
    document.getElementById('dashboard-page').style.display = 'none';
    document.getElementById('analytics-page').style.display = 'none';
    document.getElementById('vessel-page').style.display = 'none';
    document.getElementById(\\`${page}-page\\`).style.display = 'block';
}

document.addEventListener('DOMContentLoaded', () => {
    fetchData();
    showPage('dashboard');
});
"""

with open("static/js/script.js", "w") as f:
    f.write(script_js)

print("✅ Estrutura do projeto criada com sucesso!")
print(f"\n📁 Pasta do projeto: {os.path.abspath(project_name)}")
print("\n🚀 Para executar:")
print("   cd diamond-psv3300-carbon-monitor")
print("   pip install -r requirements.txt")
print("   python app.py")
print("\n🌐 Acesse: http://localhost:5000")