import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'traffic-congestion-prediction-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///traffic_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ML Model paths
    YOLO_MODEL_PATH = 'ml_models/vehicle_detection/yolov8n.pt'
    LSTM_MODEL_PATH = 'ml_models/traffic_prediction/lstm_model.h5'
    
    # Data paths
    DATA_DIR = 'data'
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
    
    # API Keys
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    
    # IoT Configuration
    MQTT_BROKER = os.environ.get('MQTT_BROKER') or 'localhost'
    MQTT_PORT = int(os.environ.get('MQTT_PORT') or 1883)
    
    # Traffic thresholds
    CONGESTION_THRESHOLDS = {
        'low': 0.3,
        'medium': 0.6,
        'high': 0.8
    }
    
    # Prediction settings
    PREDICTION_HORIZON = 60  # minutes
    UPDATE_INTERVAL = 30  # seconds

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///traffic_dev.db'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/traffic_db'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
