"""
Test script for Traffic Congestion Prediction System
"""

import requests
import json
import time
from datetime import datetime

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Traffic Congestion Prediction System API")
    print("=" * 50)
    
    # Test health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test dashboard data
    print("\n2. Testing dashboard data...")
    try:
        response = requests.get(f"{base_url}/api/dashboard-data")
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard data retrieved")
            print(f"   Locations: {data['summary']['total_locations']}")
            print(f"   High congestion: {data['summary']['high_congestion']}")
        else:
            print(f"❌ Dashboard data failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard data error: {e}")
    
    # Test traffic prediction
    print("\n3. Testing traffic prediction...")
    try:
        prediction_data = {
            "locations": [{"id": "location_1"}],
            "horizon": 60
        }
        response = requests.post(f"{base_url}/api/prediction/forecast", 
                                json=prediction_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ Traffic prediction successful")
            print(f"   Predictions: {len(data['predictions'])}")
        else:
            print(f"❌ Traffic prediction failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Traffic prediction error: {e}")
    
    # Test route optimization
    print("\n4. Testing route optimization...")
    try:
        route_data = {
            "origin": {"lat": 28.6139, "lng": 77.2090},
            "destination": {"lat": 28.5355, "lng": 77.3910},
            "avoid_congestion": True
        }
        response = requests.post(f"{base_url}/api/routes/optimize", 
                                json=route_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ Route optimization successful")
            print(f"   Distance: {data['distance']:.2f} km")
            print(f"   Time: {data['estimated_time']:.0f} min")
        else:
            print(f"❌ Route optimization failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Route optimization error: {e}")
    
    # Test alert subscription
    print("\n5. Testing alert subscription...")
    try:
        alert_data = {
            "email": "test@example.com",
            "location_id": "location_1",
            "threshold_level": "high"
        }
        response = requests.post(f"{base_url}/api/alerts/subscribe", 
                                json=alert_data)
        if response.status_code == 200:
            print("✅ Alert subscription successful")
        else:
            print(f"❌ Alert subscription failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Alert subscription error: {e}")
    
    # Test traffic statistics
    print("\n6. Testing traffic statistics...")
    try:
        response = requests.get(f"{base_url}/api/stats/summary")
        if response.status_code == 200:
            data = response.json()
            print("✅ Traffic statistics retrieved")
            print(f"   Data points: {data['total_predictions']}")
        else:
            print(f"❌ Traffic statistics failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Traffic statistics error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 API testing completed!")

def test_web_interface():
    """Test web interface accessibility"""
    base_url = "http://localhost:5000"
    
    print("\n🌐 Testing Web Interface")
    print("=" * 30)
    
    pages = [
        "/",
        "/map",
        "/predictions", 
        "/routes",
        "/alerts",
        "/analytics"
    ]
    
    for page in pages:
        try:
            response = requests.get(f"{base_url}{page}")
            if response.status_code == 200:
                print(f"✅ {page} - OK")
            else:
                print(f"❌ {page} - {response.status_code}")
        except Exception as e:
            print(f"❌ {page} - Error: {e}")

if __name__ == "__main__":
    print("🚦 Traffic Congestion Prediction System - Test Suite")
    print("=" * 60)
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    # Test API endpoints
    test_api_endpoints()
    
    # Test web interface
    test_web_interface()
    
    print("\n🎉 All tests completed!")
    print("\nTo run the system:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Initialize database: python app/init_db.py")
    print("3. Start server: python app.py")
    print("4. Open browser: http://localhost:5000")
