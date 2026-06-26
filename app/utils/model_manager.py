"""
Model management for traffic prediction and optimization
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class ModelManager:
    """Manages ML models for traffic prediction and optimization"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.model_paths = {
            'lstm': 'ml_models/traffic_prediction/lstm_model.h5',
            'random_forest': 'ml_models/traffic_prediction/rf_model.pkl',
            'yolo': 'ml_models/vehicle_detection/yolov8n.pt'
        }
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained models"""
        try:
            # Load Random Forest model for traffic prediction
            if os.path.exists(self.model_paths['random_forest']):
                self.models['random_forest'] = joblib.load(self.model_paths['random_forest'])
            
            # Initialize scaler
            self.scalers['traffic'] = StandardScaler()
            
        except Exception as e:
            print(f"Warning: Could not load models: {e}")
            # Initialize default models
            self._initialize_default_models()
    
    def _initialize_default_models(self):
        """Initialize default models if pre-trained models are not available"""
        # Initialize a simple Random Forest model
        self.models['random_forest'] = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        self.scalers['traffic'] = StandardScaler()
    
    def predict_congestion(self, location_id, horizon_minutes=60):
        """Predict traffic congestion for a specific location"""
        try:
            # Generate synthetic features for prediction
            # In a real implementation, these would come from actual data
            features = self._generate_prediction_features(location_id, horizon_minutes)
            
            # Use Random Forest model for prediction
            if 'random_forest' in self.models:
                # Prepare features for prediction
                feature_array = np.array(features).reshape(1, -1)
                
                # Scale features
                scaled_features = self.scalers['traffic'].fit_transform(feature_array)
                
                # Make prediction
                congestion_score = self.models['random_forest'].predict(scaled_features)[0]
                
                # Convert score to congestion level
                congestion_level = self._score_to_congestion_level(congestion_score)
                confidence = min(abs(congestion_score) * 0.8 + 0.2, 1.0)
            else:
                # Fallback to rule-based prediction
                congestion_level, confidence = self._rule_based_prediction(location_id, horizon_minutes)
            
            return {
                'location_id': location_id,
                'predicted_congestion': congestion_level,
                'confidence_score': confidence,
                'horizon_minutes': horizon_minutes,
                'timestamp': datetime.utcnow().isoformat(),
                'model_version': 'v1.0'
            }
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            return {
                'location_id': location_id,
                'predicted_congestion': 'medium',
                'confidence_score': 0.5,
                'horizon_minutes': horizon_minutes,
                'timestamp': datetime.utcnow().isoformat(),
                'model_version': 'fallback',
                'error': str(e)
            }
    
    def _generate_prediction_features(self, location_id, horizon_minutes):
        """Generate features for traffic prediction"""
        # In a real implementation, these would be actual historical features
        current_hour = datetime.utcnow().hour
        is_weekend = datetime.utcnow().weekday() >= 5
        is_rush_hour = current_hour in [7, 8, 17, 18, 19]
        
        # Synthetic features based on time patterns
        features = [
            current_hour / 24.0,  # Normalized hour
            1.0 if is_weekend else 0.0,  # Weekend flag
            1.0 if is_rush_hour else 0.0,  # Rush hour flag
            horizon_minutes / 120.0,  # Normalized prediction horizon
            np.random.normal(0.5, 0.2),  # Simulated traffic density
            np.random.normal(30, 10) / 50.0,  # Simulated average speed
        ]
        
        return features
    
    def _score_to_congestion_level(self, score):
        """Convert prediction score to congestion level"""
        if score < 0.3:
            return 'low'
        elif score < 0.7:
            return 'medium'
        else:
            return 'high'
    
    def _rule_based_prediction(self, location_id, horizon_minutes):
        """Fallback rule-based prediction"""
        current_hour = datetime.utcnow().hour
        is_weekend = datetime.utcnow().weekday() >= 5
        
        # Simple rules based on time
        if is_weekend:
            congestion_level = 'low'
            confidence = 0.7
        elif current_hour in [7, 8, 17, 18, 19]:  # Rush hours
            congestion_level = 'high'
            confidence = 0.8
        elif current_hour in [9, 10, 11, 14, 15, 16]:  # Medium traffic
            congestion_level = 'medium'
            confidence = 0.6
        else:  # Low traffic hours
            congestion_level = 'low'
            confidence = 0.7
        
        return congestion_level, confidence
    
    def train_model(self, training_data):
        """Train the traffic prediction model"""
        try:
            if not training_data:
                return False
            
            # Convert to DataFrame
            df = pd.DataFrame(training_data)
            
            # Prepare features and target
            features = self._prepare_training_features(df)
            target = df['congestion_level'].map({'low': 0, 'medium': 0.5, 'high': 1.0})
            
            # Scale features
            scaled_features = self.scalers['traffic'].fit_transform(features)
            
            # Train Random Forest model
            self.models['random_forest'] = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                max_depth=10
            )
            self.models['random_forest'].fit(scaled_features, target)
            
            # Save model
            os.makedirs(os.path.dirname(self.model_paths['random_forest']), exist_ok=True)
            joblib.dump(self.models['random_forest'], self.model_paths['random_forest'])
            
            return True
            
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def _prepare_training_features(self, df):
        """Prepare features for model training"""
        # Extract time-based features
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df['is_rush_hour'] = df['hour'].isin([7, 8, 17, 18, 19]).astype(int)
        
        # Select features
        feature_columns = [
            'hour', 'day_of_week', 'is_weekend', 'is_rush_hour',
            'vehicle_count', 'average_speed', 'latitude', 'longitude'
        ]
        
        return df[feature_columns].fillna(0)
    
    def detect_vehicles(self, image_path):
        """Detect vehicles in an image using YOLO"""
        try:
            # This is a placeholder for YOLO vehicle detection
            # In a real implementation, you would use ultralytics YOLO
            
            # Simulate vehicle detection results
            detection_results = {
                'total_vehicles': np.random.randint(5, 50),
                'cars': np.random.randint(3, 30),
                'buses': np.random.randint(0, 5),
                'trucks': np.random.randint(0, 8),
                'motorcycles': np.random.randint(0, 10),
                'confidence': np.random.uniform(0.7, 0.95),
                'processing_time': np.random.uniform(0.1, 0.5)
            }
            
            return detection_results
            
        except Exception as e:
            print(f"Error in vehicle detection: {e}")
            return {
                'total_vehicles': 0,
                'cars': 0,
                'buses': 0,
                'trucks': 0,
                'motorcycles': 0,
                'confidence': 0.0,
                'processing_time': 0.0,
                'error': str(e)
            }
    
    def get_model_status(self):
        """Get status of all models"""
        status = {}
        
        for model_name, model_path in self.model_paths.items():
            status[model_name] = {
                'loaded': model_name in self.models,
                'path': model_path,
                'exists': os.path.exists(model_path)
            }
        
        return status
