"""
IoT Sensor Simulation for Traffic Congestion Prediction System
Simulates real-time sensor data from traffic cameras and GPS devices
"""

import json
import time
import random
import requests
from datetime import datetime
import threading

class TrafficSensorSimulator:
    """Simulates IoT sensors for traffic data collection"""
    
    def __init__(self, api_url="http://localhost:5000"):
        self.api_url = api_url
        self.running = False
        
        # Sample locations (Delhi area)
        self.locations = [
            {'id': 'sensor_1', 'lat': 28.6139, 'lng': 77.2090, 'name': 'Connaught Place'},
            {'id': 'sensor_2', 'lat': 28.5355, 'lng': 77.3910, 'name': 'Gurgaon'},
            {'id': 'sensor_3', 'lat': 28.4595, 'lng': 77.0266, 'name': 'Dwarka'},
            {'id': 'sensor_4', 'lat': 28.7041, 'lng': 77.1025, 'name': 'North Delhi'},
            {'id': 'sensor_5', 'lat': 28.5355, 'lng': 77.2590, 'name': 'South Delhi'}
        ]
        
        # Traffic patterns
        self.rush_hours = [7, 8, 17, 18, 19]
        self.medium_hours = [9, 10, 11, 14, 15, 16]
    
    def generate_traffic_data(self, location):
        """Generate realistic traffic data for a location"""
        now = datetime.now()
        hour = now.hour
        is_weekend = now.weekday() >= 5
        
        # Base traffic based on time of day
        if hour in self.rush_hours:
            base_vehicles = random.randint(40, 80)
            base_speed = random.randint(15, 25)
        elif hour in self.medium_hours:
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
        
        return {
            'location_id': location['id'],
            'latitude': location['lat'],
            'longitude': location['lng'],
            'vehicle_count': vehicle_count,
            'average_speed': average_speed,
            'congestion_level': congestion_level,
            'data_source': 'sensor',
            'timestamp': now.isoformat(),
            'raw_data': {
                'sensor_id': location['id'],
                'temperature': random.uniform(20, 35),
                'humidity': random.uniform(40, 80),
                'noise_level': random.uniform(50, 90)
            }
        }
    
    def send_traffic_data(self, data):
        """Send traffic data to the API"""
        try:
            response = requests.post(
                f"{self.api_url}/api/data/upload",
                json={'traffic_data': [data]},
                timeout=5
            )
            if response.status_code == 200:
                print(f"✅ Data sent for {data['location_id']}: {data['vehicle_count']} vehicles, {data['congestion_level']} congestion")
            else:
                print(f"❌ Failed to send data for {data['location_id']}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error sending data for {data['location_id']}: {e}")
    
    def simulate_sensor(self, location, interval=30):
        """Simulate a single sensor"""
        while self.running:
            try:
                # Generate traffic data
                traffic_data = self.generate_traffic_data(location)
                
                # Send to API
                self.send_traffic_data(traffic_data)
                
                # Wait for next reading
                time.sleep(interval)
                
            except Exception as e:
                print(f"❌ Error in sensor {location['id']}: {e}")
                time.sleep(interval)
    
    def start_simulation(self, interval=30):
        """Start the sensor simulation"""
        print(f"🚦 Starting IoT sensor simulation...")
        print(f"   Locations: {len(self.locations)}")
        print(f"   Interval: {interval} seconds")
        print(f"   API URL: {self.api_url}")
        print()
        
        self.running = True
        
        # Start a thread for each sensor
        threads = []
        for location in self.locations:
            thread = threading.Thread(
                target=self.simulate_sensor,
                args=(location, interval),
                daemon=True
            )
            thread.start()
            threads.append(thread)
            print(f"📡 Started sensor: {location['name']} ({location['id']})")
        
        print(f"\n✅ All sensors started. Press Ctrl+C to stop.")
        
        try:
            # Keep main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping sensor simulation...")
            self.running = False
            print("✅ Sensor simulation stopped")

def main():
    """Main function to run sensor simulation"""
    print("🌐 IoT Sensor Simulation for Traffic Congestion Prediction")
    print("=" * 60)
    
    # Check if API is running
    api_url = "http://localhost:5000"
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
        else:
            print("⚠️  API server responded with error, but continuing...")
    except Exception as e:
        print(f"⚠️  Could not connect to API server: {e}")
        print("   Make sure to start the server with: python app.py")
        print("   Continuing simulation anyway...")
    
    # Start simulation
    simulator = TrafficSensorSimulator(api_url)
    simulator.start_simulation(interval=30)  # 30 seconds interval

if __name__ == "__main__":
    main()
