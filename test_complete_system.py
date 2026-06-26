"""
Comprehensive Test Script for Traffic Congestion Prediction System
Tests all major functionality and provides detailed results
"""

import requests
import json
import time
from datetime import datetime

def test_system():
    """Comprehensive system test"""
    base_url = "http://localhost:5000"
    
    print("🚦 Traffic Congestion Prediction System - Complete Test Suite")
    print("=" * 70)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test results tracking
    tests_passed = 0
    tests_failed = 0
    total_tests = 0
    
    def run_test(test_name, test_func):
        nonlocal tests_passed, tests_failed, total_tests
        total_tests += 1
        print(f"🧪 Test {total_tests}: {test_name}")
        try:
            result = test_func()
            if result:
                print(f"   ✅ PASSED")
                tests_passed += 1
            else:
                print(f"   ❌ FAILED")
                tests_failed += 1
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            tests_failed += 1
        print()
    
    # Test 1: Health Check
    def test_health():
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('status') == 'healthy'
        return False
    
    # Test 2: Traffic Data
    def test_traffic_data():
        response = requests.get(f"{base_url}/api/traffic/current", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return 'locations' in data and len(data['locations']) > 0
        return False
    
    # Test 3: Traffic Prediction
    def test_prediction():
        prediction_data = {
            "locations": [{"id": "location_1"}],
            "horizon": 60
        }
        response = requests.post(f"{base_url}/api/prediction/forecast", 
                                json=prediction_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return 'predictions' in data and len(data['predictions']) > 0
        return False
    
    # Test 4: Route Optimization
    def test_route_optimization():
        route_data = {
            "origin": {"lat": 28.6139, "lng": 77.2090},
            "destination": {"lat": 19.0760, "lng": 72.8777},
            "avoid_congestion": True
        }
        response = requests.post(f"{base_url}/api/routes/optimize", 
                                json=route_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return 'distance' in data and 'estimated_time' in data
        return False
    
    # Test 5: Web Interface
    def test_web_interface():
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            content = response.text
            return 'Traffic Congestion Prediction System' in content
        return False
    
    # Test 6: Data Quality
    def test_data_quality():
        response = requests.get(f"{base_url}/api/traffic/current", timeout=5)
        if response.status_code == 200:
            data = response.json()
            locations = data.get('locations', [])
            if not locations:
                return False
            
            # Check data structure
            required_fields = ['location_id', 'latitude', 'longitude', 'vehicle_count', 'congestion_level']
            for location in locations:
                for field in required_fields:
                    if field not in location:
                        return False
            
            # Check congestion levels
            valid_levels = ['low', 'medium', 'high']
            for location in locations:
                if location['congestion_level'] not in valid_levels:
                    return False
            
            return True
        return False
    
    # Test 7: Performance Test
    def test_performance():
        start_time = time.time()
        response = requests.get(f"{base_url}/api/traffic/current", timeout=5)
        end_time = time.time()
        
        if response.status_code == 200:
            response_time = end_time - start_time
            return response_time < 1.0  # Should respond within 1 second
        return False
    
    # Test 8: Error Handling
    def test_error_handling():
        # Test invalid endpoint
        response = requests.get(f"{base_url}/api/invalid", timeout=5)
        return response.status_code == 404
    
    # Run all tests
    run_test("Health Check", test_health)
    run_test("Traffic Data API", test_traffic_data)
    run_test("Traffic Prediction", test_prediction)
    run_test("Route Optimization", test_route_optimization)
    run_test("Web Interface", test_web_interface)
    run_test("Data Quality", test_data_quality)
    run_test("Performance", test_performance)
    run_test("Error Handling", test_error_handling)
    
    # Print summary
    print("=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"✅ Tests Passed: {tests_passed}")
    print(f"❌ Tests Failed: {tests_failed}")
    print(f"📈 Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    print(f"⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if tests_failed == 0:
        print("\n🎉 ALL TESTS PASSED! System is working correctly.")
        return True
    else:
        print(f"\n⚠️  {tests_failed} test(s) failed. Please check the issues above.")
        return False

def test_detailed_functionality():
    """Test detailed functionality with data analysis"""
    base_url = "http://localhost:5000"
    
    print("\n🔍 DETAILED FUNCTIONALITY TEST")
    print("=" * 50)
    
    try:
        # Get traffic data
        response = requests.get(f"{base_url}/api/traffic/current", timeout=5)
        if response.status_code == 200:
            data = response.json()
            locations = data.get('locations', [])
            
            print(f"📊 Traffic Data Analysis:")
            print(f"   - Total locations: {len(locations)}")
            
            # Analyze congestion levels
            congestion_counts = {'low': 0, 'medium': 0, 'high': 0}
            total_vehicles = 0
            total_speed = 0
            
            for location in locations:
                congestion_counts[location['congestion_level']] += 1
                total_vehicles += location['vehicle_count']
                total_speed += location['average_speed']
            
            print(f"   - Congestion distribution:")
            for level, count in congestion_counts.items():
                print(f"     {level}: {count} locations")
            
            print(f"   - Average vehicles: {total_vehicles/len(locations):.1f}")
            print(f"   - Average speed: {total_speed/len(locations):.1f} km/h")
            
            # Test prediction
            print(f"\n🔮 Prediction Test:")
            prediction_data = {
                "locations": [{"id": "location_1"}],
                "horizon": 60
            }
            pred_response = requests.post(f"{base_url}/api/prediction/forecast", 
                                        json=prediction_data, timeout=5)
            if pred_response.status_code == 200:
                pred_data = pred_response.json()
                predictions = pred_data.get('predictions', [])
                if predictions:
                    pred = predictions[0]
                    print(f"   - Predicted congestion: {pred['predicted_congestion']}")
                    print(f"   - Confidence: {pred['confidence_score']*100:.1f}%")
                    print(f"   - Horizon: {pred['horizon_minutes']} minutes")
            
            # Test route optimization
            print(f"\n🗺️ Route Optimization Test:")
            route_data = {
                "origin": {"lat": 28.6139, "lng": 77.2090},
                "destination": {"lat": 19.0760, "lng": 72.8777},
                "avoid_congestion": True
            }
            route_response = requests.post(f"{base_url}/api/routes/optimize", 
                                          json=route_data, timeout=5)
            if route_response.status_code == 200:
                route_data_result = route_response.json()
                print(f"   - Distance: {route_data_result['distance']:.2f} km")
                print(f"   - Estimated time: {route_data_result['estimated_time']:.0f} minutes")
                print(f"   - Congestion avoidance: {route_data_result['congestion_avoidance']}")
            
            return True
            
    except Exception as e:
        print(f"❌ Detailed test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚦 Traffic Congestion Prediction System - Complete Test Suite")
    print("=" * 70)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not running. Please start the server first:")
            print("   python simple_app.py")
            exit(1)
    except:
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python simple_app.py")
        exit(1)
    
    # Run tests
    success = test_system()
    test_detailed_functionality()
    
    if success:
        print("\n🎉 SYSTEM IS WORKING PERFECTLY!")
        print("\n📋 Available Endpoints:")
        print("   - Dashboard: http://localhost:5000")
        print("   - Health: http://localhost:5000/health")
        print("   - Traffic Data: http://localhost:5000/api/traffic/current")
        print("   - Predictions: POST http://localhost:5000/api/prediction/forecast")
        print("   - Routes: POST http://localhost:5000/api/routes/optimize")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
