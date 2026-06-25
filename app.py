from flask import Flask, render_template

app = Flask(__name__)

# Dados do Diamond PSV 3300
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
    """Endpoint para dados em JSON (para requisições AJAX)"""
    from datetime import datetime, timedelta
    import random

    # Dados históricos
    monthly_data = {
        "labels": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
        "co2": [820, 850, 880, 840, 860, 830, 810, 800, 790, 780, 770, 760],
        "reduction": [5, 3, 2, 6, 4, 7, 8, 9, 10, 11, 12, 15]
    }

    # Dados em tempo real
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

    # Previsões de IA
    ai_forecast = {
        "next_month": {"predicted_co2": 720, "confidence": 0.92, "trend": "descendente"},
        "next_quarter": {"predicted_co2": 2050, "confidence": 0.88, "trend": "descendente"},
        "annual_target": {"target": 6800, "current_projection": 7100, "gap": 300, "probability": 0.78}
    }

    # Estratégias de redução
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