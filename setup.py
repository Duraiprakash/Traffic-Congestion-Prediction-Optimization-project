"""
Setup script for Traffic Congestion Prediction & Optimization System
MCA Final Year Project
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🚦 Traffic Congestion Prediction & Optimization System")
    print("📚 MCA Final Year Project")
    print("=" * 60)
    print()

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print("✅ pip upgraded")
        
        # Install requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "data/raw",
        "data/processed", 
        "data/models",
        "ml_models/vehicle_detection",
        "ml_models/traffic_prediction",
        "ml_models/optimization",
        "app/static/css",
        "app/static/js",
        "app/static/images",
        "app/templates",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")

def setup_environment():
    """Setup environment variables"""
    print("\n🔧 Setting up environment...")
    
    env_content = """# Flask Configuration
SECRET_KEY=traffic-congestion-prediction-2024
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///traffic_data.db

# API Keys (Add your keys here)
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
OPENWEATHER_API_KEY=your-openweather-api-key

# IoT Configuration
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=

# Model Configuration
YOLO_MODEL_PATH=ml_models/vehicle_detection/yolov8n.pt
LSTM_MODEL_PATH=ml_models/traffic_prediction/lstm_model.h5

# Data Paths
DATA_DIR=data
RAW_DATA_DIR=data/raw
PROCESSED_DATA_DIR=data/processed
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Environment file created (.env)")

def initialize_database():
    """Initialize database with sample data"""
    print("\n🗄️ Initializing database...")
    
    try:
        from app.init_db import init_database
        init_database()
        print("✅ Database initialized with sample data")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def run_tests():
    """Run system tests"""
    print("\n🧪 Running system tests...")
    
    try:
        # Import test functions
        from test_system import test_api_endpoints, test_web_interface
        
        # Note: Tests require server to be running
        print("ℹ️  Note: Full tests require server to be running")
        print("   Run 'python test_system.py' after starting the server")
        return True
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        return False

def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("\n📋 Usage Instructions:")
    print("\n1. Start the server:")
    print("   python app.py")
    print("\n2. Open your browser:")
    print("   http://localhost:5000")
    print("\n3. Available pages:")
    print("   - Dashboard: http://localhost:5000/")
    print("   - Traffic Map: http://localhost:5000/map")
    print("   - Predictions: http://localhost:5000/predictions")
    print("   - Route Optimization: http://localhost:5000/routes")
    print("   - Alerts: http://localhost:5000/alerts")
    print("   - Analytics: http://localhost:5000/analytics")
    print("\n4. API Documentation:")
    print("   - Health Check: http://localhost:5000/health")
    print("   - Dashboard Data: http://localhost:5000/api/dashboard-data")
    print("   - Traffic Prediction: POST http://localhost:5000/api/prediction/forecast")
    print("   - Route Optimization: POST http://localhost:5000/api/routes/optimize")
    print("\n5. Test the system:")
    print("   python test_system.py")
    print("\n6. Development mode:")
    print("   python app.py --debug")
    print("\n" + "=" * 60)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_environment()
    
    # Initialize database
    if not initialize_database():
        print("\n⚠️  Database initialization failed, but you can continue")
        print("   Run 'python app/init_db.py' manually if needed")
    
    # Setup tests
    run_tests()
    
    # Print usage instructions
    print_usage_instructions()

if __name__ == "__main__":
    main()
