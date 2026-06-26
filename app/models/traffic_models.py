"""
Traffic-related database models
"""

from datetime import datetime
from app.models.database import db
import json

class TrafficData(db.Model):
    """Model for storing traffic data from various sources"""
    __tablename__ = 'traffic_data'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    location_id = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    vehicle_count = db.Column(db.Integer, default=0)
    average_speed = db.Column(db.Float, default=0.0)
    congestion_level = db.Column(db.String(20), default='low')  # low, medium, high
    data_source = db.Column(db.String(50), nullable=False)  # camera, gps, sensor
    raw_data = db.Column(db.Text)  # JSON string for additional data
    
    def __repr__(self):
        return f'<TrafficData {self.location_id} at {self.timestamp}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'location_id': self.location_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'vehicle_count': self.vehicle_count,
            'average_speed': self.average_speed,
            'congestion_level': self.congestion_level,
            'data_source': self.data_source,
            'raw_data': json.loads(self.raw_data) if self.raw_data else None
        }

class TrafficPrediction(db.Model):
    """Model for storing traffic predictions"""
    __tablename__ = 'traffic_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    location_id = db.Column(db.String(100), nullable=False)
    predicted_congestion = db.Column(db.String(20), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    prediction_horizon = db.Column(db.Integer, nullable=False)  # minutes ahead
    model_version = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<TrafficPrediction {self.location_id} -> {self.predicted_congestion}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'location_id': self.location_id,
            'predicted_congestion': self.predicted_congestion,
            'confidence_score': self.confidence_score,
            'prediction_horizon': self.prediction_horizon,
            'model_version': self.model_version
        }

class RouteOptimization(db.Model):
    """Model for storing route optimization results"""
    __tablename__ = 'route_optimizations'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    origin_lat = db.Column(db.Float, nullable=False)
    origin_lng = db.Column(db.Float, nullable=False)
    destination_lat = db.Column(db.Float, nullable=False)
    destination_lng = db.Column(db.Float, nullable=False)
    optimized_route = db.Column(db.Text, nullable=False)  # JSON string
    estimated_time = db.Column(db.Float, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    congestion_avoidance = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<RouteOptimization {self.origin_lat},{self.origin_lng} -> {self.destination_lat},{self.destination_lng}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'origin': {'lat': self.origin_lat, 'lng': self.origin_lng},
            'destination': {'lat': self.destination_lat, 'lng': self.destination_lng},
            'optimized_route': json.loads(self.optimized_route),
            'estimated_time': self.estimated_time,
            'distance': self.distance,
            'congestion_avoidance': self.congestion_avoidance
        }

class AlertSubscription(db.Model):
    """Model for storing alert subscriptions"""
    __tablename__ = 'alert_subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    location_id = db.Column(db.String(100), nullable=False)
    threshold_level = db.Column(db.String(20), nullable=False)  # low, medium, high
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AlertSubscription {self.email} for {self.location_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'location_id': self.location_id,
            'threshold_level': self.threshold_level,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
