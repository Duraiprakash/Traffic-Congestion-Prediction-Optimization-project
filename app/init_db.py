"""
Database initialization script for Traffic Congestion Prediction System
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models.database import db
from app.models.traffic_models import TrafficData, TrafficPrediction, RouteOptimization, AlertSubscription
from app.utils.data_processor import DataProcessor
from app.utils.model_manager import ModelManager

def init_database():
    """Initialize database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Generate sample data
        generate_sample_data()
        
        print("✅ Sample data generated")
        print("🚦 Traffic Congestion Prediction System is ready!")

def generate_sample_data():
    """Generate sample traffic data for demonstration"""
    
    # Sample locations (Delhi area)
    locations = [
        {'id': 'location_1', 'lat': 28.6139, 'lng': 77.2090, 'name': 'Connaught Place'},
        {'id': 'location_2', 'lat': 28.5355, 'lng': 77.3910, 'name': 'Gurgaon'},
        {'id': 'location_3', 'lat': 28.4595, 'lng': 77.0266, 'name': 'Dwarka'},
        {'id': 'location_4', 'lat': 28.7041, 'lng': 77.1025, 'name': 'North Delhi'},
        {'id': 'location_5', 'lat': 28.5355, 'lng': 77.2590, 'name': 'South Delhi'}
    ]
    
    # Generate traffic data for the last 24 hours
    now = datetime.utcnow()
    data_processor = DataProcessor()
    
    for i in range(24):  # 24 hours
        for location in locations:
            # Generate data every hour
            timestamp = now - timedelta(hours=23-i)
            
            # Simulate traffic patterns
            hour = timestamp.hour
            is_weekend = timestamp.weekday() >= 5
            
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
            
            # Add some randomness
            vehicle_count = max(0, base_vehicles + random.randint(-10, 10))
            average_speed = max(5, base_speed + random.randint(-5, 5))
            
            # Calculate congestion level
            congestion_level = data_processor._calculate_congestion_level(
                vehicle_count, average_speed, 50
            )
            
            # Create traffic data entry
            traffic_data = TrafficData(
                location_id=location['id'],
                latitude=location['lat'],
                longitude=location['lng'],
                vehicle_count=vehicle_count,
                average_speed=average_speed,
                congestion_level=congestion_level,
                data_source=random.choice(['camera', 'sensor', 'gps']),
                raw_data='{"simulated": true}'
            )
            
            db.session.add(traffic_data)
    
    # Generate some predictions
    model_manager = ModelManager()
    
    for location in locations:
        prediction = model_manager.predict_congestion(
            location_id=location['id'],
            horizon_minutes=60
        )
        
        traffic_prediction = TrafficPrediction(
            location_id=location['id'],
            predicted_congestion=prediction['predicted_congestion'],
            confidence_score=prediction['confidence_score'],
            prediction_horizon=60,
            model_version='v1.0'
        )
        
        db.session.add(traffic_prediction)
    
    # Generate some route optimizations
    sample_routes = [
        {
            'origin': {'lat': 28.6139, 'lng': 77.2090},
            'destination': {'lat': 28.5355, 'lng': 77.3910}
        },
        {
            'origin': {'lat': 28.4595, 'lng': 77.0266},
            'destination': {'lat': 28.7041, 'lng': 77.1025}
        }
    ]
    
    for route in sample_routes:
        route_opt = RouteOptimization(
            origin_lat=route['origin']['lat'],
            origin_lng=route['origin']['lng'],
            destination_lat=route['destination']['lat'],
            destination_lng=route['destination']['lng'],
            optimized_route='[{"lat": 28.6139, "lng": 77.2090}, {"lat": 28.5355, "lng": 77.3910}]',
            estimated_time=random.randint(30, 120),
            distance=random.uniform(10, 50),
            congestion_avoidance=True
        )
        
        db.session.add(route_opt)
    
    # Generate some alert subscriptions
    subscriptions = [
        AlertSubscription(
            email='user1@example.com',
            location_id='location_1',
            threshold_level='high'
        ),
        AlertSubscription(
            email='user2@example.com',
            location_id='location_2',
            threshold_level='medium'
        ),
        AlertSubscription(
            email='admin@example.com',
            location_id='all',
            threshold_level='high'
        )
    ]
    
    for subscription in subscriptions:
        db.session.add(subscription)
    
    # Commit all changes
    db.session.commit()
    
    print(f"📊 Generated sample data:")
    print(f"   - Traffic records: {TrafficData.query.count()}")
    print(f"   - Predictions: {TrafficPrediction.query.count()}")
    print(f"   - Route optimizations: {RouteOptimization.query.count()}")
    print(f"   - Alert subscriptions: {AlertSubscription.query.count()}")

if __name__ == '__main__':
    init_database()
