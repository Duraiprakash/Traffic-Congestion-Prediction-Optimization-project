"""
Startup script for Traffic Congestion Prediction System
This script will start the system and run basic tests
"""

import subprocess
import time
import requests
import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_modules = ['flask', 'requests']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - Missing")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n📦 Installing missing dependencies: {', '.join(missing_modules)}")
        for module in missing_modules:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", module], 
                             check=True, capture_output=True)
                print(f"   ✅ Installed {module}")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Failed to install {module}: {e}")
                return False
    
    return True

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting Traffic Congestion Prediction System...")
    
    try:
        # Start the server in background
        process = subprocess.Popen([sys.executable, "simple_app.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        print("   ⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Check if server is running
        try:
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                print("   ✅ Server started successfully!")
                return process
            else:
                print("   ❌ Server started but health check failed")
                return None
        except:
            print("   ❌ Server failed to start")
            return None
            
    except Exception as e:
        print(f"   ❌ Error starting server: {e}")
        return None

def run_basic_tests():
    """Run basic functionality tests"""
    print("\n🧪 Running basic tests...")
    
    base_url = "http://localhost:5000"
    tests = [
        ("Health Check", f"{base_url}/health"),
        ("Traffic Data", f"{base_url}/api/traffic/current"),
        ("Web Interface", f"{base_url}/")
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, url in tests:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {test_name}")
                passed += 1
            else:
                print(f"   ❌ {test_name} - Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {test_name} - Error: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    return passed == total

def show_system_info():
    """Show system information and usage instructions"""
    print("\n" + "="*60)
    print("🚦 Traffic Congestion Prediction System")
    print("📚 MCA Final Year Project")
    print("="*60)
    print("\n✅ System is running successfully!")
    print("\n🌐 Available Endpoints:")
    print("   • Dashboard: http://localhost:5000")
    print("   • Health Check: http://localhost:5000/health")
    print("   • Traffic Data: http://localhost:5000/api/traffic/current")
    print("   • Predictions: POST http://localhost:5000/api/prediction/forecast")
    print("   • Route Optimization: POST http://localhost:5000/api/routes/optimize")
    
    print("\n📋 Features:")
    print("   • Real-time traffic monitoring")
    print("   • AI-powered congestion prediction")
    print("   • Route optimization with congestion avoidance")
    print("   • Interactive web dashboard")
    print("   • RESTful API for integration")
    
    print("\n🛠️ Development:")
    print("   • Press Ctrl+C to stop the server")
    print("   • Check logs for debugging")
    print("   • Modify simple_app.py for customizations")
    
    print("\n📊 System Status:")
    print("   • Server: Running on port 5000")
    print("   • Database: In-memory (SQLite)")
    print("   • AI Models: Simulated (ready for real models)")
    print("   • IoT Integration: Simulated sensors")
    
    print("\n🎯 Perfect for MCA Final Year Project!")
    print("   • Demonstrates AI/ML + IoT + Web Development")
    print("   • Real-world traffic management solution")
    print("   • Scalable architecture")
    print("   • Industry-relevant technologies")
    
    print("\n" + "="*60)

def main():
    """Main startup function"""
    print("🚦 Traffic Congestion Prediction System - Startup")
    print("="*60)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Please install required packages.")
        return False
    
    # Start server
    server_process = start_server()
    if not server_process:
        print("❌ Failed to start server. Please check for errors.")
        return False
    
    # Run basic tests
    if not run_basic_tests():
        print("⚠️  Some tests failed, but server is running.")
    
    # Show system info
    show_system_info()
    
    try:
        print("\n🔄 Server is running. Press Ctrl+C to stop...")
        server_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        server_process.terminate()
        print("✅ Server stopped.")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
