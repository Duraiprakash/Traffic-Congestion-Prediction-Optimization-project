"""
Simplified Traffic Congestion Prediction System
Minimal version for testing and demonstration
"""

from flask import Flask, render_template, jsonify, request
import json
import random
from datetime import datetime, timedelta
import math

app = Flask(__name__)

# Sample traffic data
SAMPLE_LOCATIONS = [
    {'id': 'location_1', 'lat': 28.6139, 'lng': 77.2090, 'name': 'Connaught Place'},
    {'id': 'location_2', 'lat': 28.5355, 'lng': 77.3910, 'name': 'Gurgaon'},
    {'id': 'location_3', 'lat': 28.4595, 'lng': 77.0266, 'name': 'Dwarka'},
    {'id': 'location_4', 'lat': 28.7041, 'lng': 77.1025, 'name': 'North Delhi'},
    {'id': 'location_5', 'lat': 28.5355, 'lng': 77.2590, 'name': 'South Delhi'}
]

def generate_traffic_data():
    """Generate sample traffic data"""
    traffic_data = []
    now = datetime.now()
    
    for location in SAMPLE_LOCATIONS:
        # Simulate traffic patterns
        hour = now.hour
        is_weekend = now.weekday() >= 5
        
        # Rush hour simulation
        if hour in [7, 8, 17, 18, 19]:
            base_vehicles = random.randint(40, 80)
            base_speed = random.randint(15, 25)
        elif hour in [9, 10, 11, 14, 15, 16]:
            base_vehicles = random.randint(25, 50)
            base_speed = random.randint(25, 35)
        else:
            base_vehicles = random.randint(5, 25)
            base_speed = random.randint(30, 50)
        
        # Weekend adjustment
        if is_weekend:
            base_vehicles = int(base_vehicles * 0.7)
            base_speed = int(base_speed * 1.1)
        
        # Add randomness
        vehicle_count = max(0, base_vehicles + random.randint(-10, 10))
        average_speed = max(5, base_speed + random.randint(-5, 5))
        
        # Calculate congestion level
        density = min(vehicle_count / 50, 1.0)
        speed_factor = max(0, min(average_speed / 50.0, 1.0))
        congestion_score = (density * 0.7) + ((1 - speed_factor) * 0.3)
        
        if congestion_score <= 0.3:
            congestion_level = 'low'
        elif congestion_score <= 0.6:
            congestion_level = 'medium'
        else:
            congestion_level = 'high'
        
        traffic_data.append({
            'location_id': location['id'],
            'latitude': location['lat'],
            'longitude': location['lng'],
            'vehicle_count': vehicle_count,
            'average_speed': average_speed,
            'congestion_level': congestion_level,
            'data_source': 'sensor',
            'timestamp': now.isoformat()
        })
    
    return traffic_data

@app.route('/')
def index():
    """Main dashboard"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Traffic Congestion Prediction System</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
            .nav { display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap; }
            .nav a { padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; transition: background 0.3s; }
            .nav a:hover { background: #2980b9; }
            .card { background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #3498db; }
            .status { display: inline-block; padding: 5px 10px; border-radius: 15px; color: white; font-weight: bold; }
            .status.low { background: #27ae60; }
            .status.medium { background: #f39c12; }
            .status.high { background: #e74c3c; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
            .btn { padding: 10px 20px; background: #27ae60; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .btn:hover { background: #229954; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚦 Traffic Congestion Prediction System</h1>
            <p style="text-align: center; color: #7f8c8d; margin-bottom: 30px;">MCA Final Year Project - AI/ML + IoT + Web Development</p>
            
            <div class="nav">
                <a href="/">Dashboard</a>
                <a href="/api/traffic/current">API Data</a>
                <a href="/api/prediction/forecast">Predictions</a>
                <a href="/api/routes/optimize">Route Optimization</a>
                <a href="/health">Health Check</a>
            </div>
            
            <div class="card">
                <h2>📊 System Status</h2>
                <p><strong>Status:</strong> <span class="status low">Operational</span></p>
                <p><strong>Locations Monitored:</strong> 5</p>
                <p><strong>Last Update:</strong> <span id="lastUpdate">Loading...</span></p>
                <button class="btn" onclick="loadTrafficData()">Refresh Data</button>
            </div>
            
            <div class="card">
                <h2>🚗 Current Traffic Status</h2>
                <div id="trafficData">Loading traffic data...</div>
            </div>
            
            <div class="card">
                <h2>🔮 Traffic Predictions</h2>
                <div id="predictions">Loading predictions...</div>
                <button class="btn" onclick="loadPredictions()">Generate Predictions</button>
            </div>
            
            <div class="card">
                <h2>🗺️ Route Optimization</h2>
                <p>Origin: <input type="text" id="origin" placeholder="Enter origin" value="Delhi" style="padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px;"></p>
                <p>Destination: <input type="text" id="destination" placeholder="Enter destination" value="Mumbai" style="padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px;"></p>
                <button class="btn" onclick="optimizeRoute()">Find Optimal Route</button>
                <div id="routeResult" style="margin-top: 15px;"></div>
            </div>
        </div>
        
        <script>
            function loadTrafficData() {
                fetch('/api/traffic/current')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('lastUpdate').textContent = new Date().toLocaleString();
                        let html = '<div class="grid">';
                        data.locations.forEach(location => {
                            html += `
                                <div class="card">
                                    <h3>${location.location_id}</h3>
                                    <p><strong>Vehicles:</strong> ${location.vehicle_count}</p>
                                    <p><strong>Speed:</strong> ${location.average_speed.toFixed(1)} km/h</p>
                                    <p><strong>Congestion:</strong> <span class="status ${location.congestion_level}">${location.congestion_level}</span></p>
                                </div>
                            `;
                        });
                        html += '</div>';
                        document.getElementById('trafficData').innerHTML = html;
                    })
                    .catch(error => {
                        document.getElementById('trafficData').innerHTML = '<p style="color: red;">Error loading traffic data</p>';
                    });
            }
            
            function loadPredictions() {
                fetch('/api/prediction/forecast', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({locations: [{id: 'location_1'}], horizon: 60})
                })
                .then(response => response.json())
                .then(data => {
                    let html = '<div class="grid">';
                    data.predictions.forEach(pred => {
                        html += `
                            <div class="card">
                                <h3>${pred.location_id}</h3>
                                <p><strong>Predicted Congestion:</strong> <span class="status ${pred.predicted_congestion}">${pred.predicted_congestion}</span></p>
                                <p><strong>Confidence:</strong> ${(pred.confidence_score * 100).toFixed(1)}%</p>
                                <p><strong>Horizon:</strong> ${pred.horizon_minutes} minutes</p>
                            </div>
                        `;
                    });
                    html += '</div>';
                    document.getElementById('predictions').innerHTML = html;
                })
                .catch(error => {
                    document.getElementById('predictions').innerHTML = '<p style="color: red;">Error loading predictions</p>';
                });
            }
            
            function optimizeRoute() {
                const origin = document.getElementById('origin').value;
                const destination = document.getElementById('destination').value;
                
                fetch('/api/routes/optimize', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        origin: {lat: 28.6139, lng: 77.2090},
                        destination: {lat: 19.0760, lng: 72.8777},
                        avoid_congestion: true
                    })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('routeResult').innerHTML = `
                        <div class="card">
                            <h3>Optimized Route</h3>
                            <p><strong>Distance:</strong> ${data.distance.toFixed(2)} km</p>
                            <p><strong>Estimated Time:</strong> ${Math.round(data.estimated_time)} minutes</p>
                            <p><strong>Congestion Avoidance:</strong> ${data.congestion_avoidance ? 'Enabled' : 'Disabled'}</p>
                        </div>
                    `;
                })
                .catch(error => {
                    document.getElementById('routeResult').innerHTML = '<p style="color: red;">Error optimizing route</p>';
                });
            }
            
            // Load data on page load
            loadTrafficData();
            loadPredictions();
        </script>
    </body>
    </html>
    """

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Traffic Congestion Prediction System is running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/traffic/current')
def get_current_traffic():
    """Get current traffic data"""
    traffic_data = generate_traffic_data()
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'locations': traffic_data
    })

@app.route('/api/prediction/forecast', methods=['POST'])
def predict_traffic():
    """Predict traffic congestion"""
    data = request.get_json()
    locations = data.get('locations', [])
    horizon = data.get('horizon', 60)
    
    predictions = []
    for location in locations:
        # Simple prediction logic
        congestion_levels = ['low', 'medium', 'high']
        predicted_congestion = random.choice(congestion_levels)
        confidence = random.uniform(0.7, 0.95)
        
        predictions.append({
            'location_id': location.get('id', 'unknown'),
            'predicted_congestion': predicted_congestion,
            'confidence_score': confidence,
            'horizon_minutes': horizon,
            'timestamp': datetime.now().isoformat(),
            'model_version': 'v1.0'
        })
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'predictions': predictions,
        'horizon_minutes': horizon
    })

@app.route('/api/routes/optimize', methods=['POST'])
def optimize_route():
    """Optimize route between origin and destination"""
    data = request.get_json()
    origin = data.get('origin', {})
    destination = data.get('destination', {})
    avoid_congestion = data.get('avoid_congestion', True)
    
    # Calculate distance (simplified)
    lat1, lng1 = origin.get('lat', 0), origin.get('lng', 0)
    lat2, lng2 = destination.get('lat', 0), destination.get('lng', 0)
    
    # Simple distance calculation
    distance = math.sqrt((lat2-lat1)**2 + (lng2-lng1)**2) * 111  # Rough km conversion
    
    # Estimate time based on distance and congestion
    base_time = distance * 2  # 2 minutes per km
    if avoid_congestion:
        base_time *= 1.2  # 20% longer for congestion avoidance
    
    return jsonify({
        'origin': origin,
        'destination': destination,
        'distance': distance,
        'estimated_time': base_time,
        'congestion_avoidance': avoid_congestion,
        'route': [
            {'lat': lat1, 'lng': lng1},
            {'lat': (lat1 + lat2) / 2, 'lng': (lng1 + lng2) / 2},
            {'lat': lat2, 'lng': lng2}
        ]
    })

if __name__ == '__main__':
    print("🚦 Starting Traffic Congestion Prediction System...")
    print("🌐 Dashboard: http://localhost:5000")
    print("📊 API: http://localhost:5000/api")
    print("❤️ Health: http://localhost:5000/health")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
