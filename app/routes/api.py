"""
API routes for Traffic Congestion Prediction System
"""

from flask import Blueprint, jsonify, request
from app.models.database import db
from app.models.traffic_models import TrafficData, TrafficPrediction, RouteOptimization, AlertSubscription
from app.utils.data_processor import DataProcessor
from app.utils.model_manager import ModelManager
from datetime import datetime, timedelta
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/traffic/current', methods=['GET'])
def get_current_traffic():
    """Get current traffic status for all locations"""
    try:
        # Get recent traffic data (last 5 minutes)
        recent_time = datetime.utcnow() - timedelta(minutes=5)
        traffic_data = TrafficData.query.filter(
            TrafficData.timestamp >= recent_time
        ).all()
        
        result = {
            'timestamp': datetime.utcnow().isoformat(),
            'locations': [data.to_dict() for data in traffic_data]
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/traffic/location/<location_id>', methods=['GET'])
def get_location_traffic(location_id):
    """Get traffic data for a specific location"""
    try:
        # Get recent data for specific location
        recent_time = datetime.utcnow() - timedelta(minutes=30)
        traffic_data = TrafficData.query.filter(
            TrafficData.location_id == location_id,
            TrafficData.timestamp >= recent_time
        ).order_by(TrafficData.timestamp.desc()).all()
        
        if not traffic_data:
            return jsonify({'error': 'No data found for location'}), 404
        
        return jsonify({
            'location_id': location_id,
            'data': [data.to_dict() for data in traffic_data]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/prediction/forecast', methods=['POST'])
def predict_traffic():
    """Predict traffic congestion for given locations and time"""
    try:
        data = request.get_json()
        locations = data.get('locations', [])
        prediction_horizon = data.get('horizon', 60)  # minutes
        
        if not locations:
            return jsonify({'error': 'No locations provided'}), 400
        
        # Initialize model manager
        model_manager = ModelManager()
        
        predictions = []
        for location in locations:
            prediction = model_manager.predict_congestion(
                location_id=location['id'],
                horizon_minutes=prediction_horizon
            )
            predictions.append(prediction)
        
        return jsonify({
            'timestamp': datetime.utcnow().isoformat(),
            'predictions': predictions,
            'horizon_minutes': prediction_horizon
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/routes/optimize', methods=['POST'])
def optimize_route():
    """Optimize route between origin and destination"""
    try:
        data = request.get_json()
        origin = data.get('origin')
        destination = data.get('destination')
        avoid_congestion = data.get('avoid_congestion', True)
        
        if not origin or not destination:
            return jsonify({'error': 'Origin and destination required'}), 400
        
        # Initialize data processor for route optimization
        data_processor = DataProcessor()
        
        optimized_route = data_processor.optimize_route(
            origin_lat=origin['lat'],
            origin_lng=origin['lng'],
            dest_lat=destination['lat'],
            dest_lng=destination['lng'],
            avoid_congestion=avoid_congestion
        )
        
        # Store optimization result
        route_opt = RouteOptimization(
            origin_lat=origin['lat'],
            origin_lng=origin['lng'],
            destination_lat=destination['lat'],
            destination_lng=destination['lng'],
            optimized_route=json.dumps(optimized_route['route']),
            estimated_time=optimized_route['estimated_time'],
            distance=optimized_route['distance'],
            congestion_avoidance=avoid_congestion
        )
        
        db.session.add(route_opt)
        db.session.commit()
        
        # Align response with frontend expectations (provide both keys)
        return jsonify({
            'id': route_opt.id,
            'timestamp': route_opt.timestamp.isoformat(),
            'origin': {'lat': route_opt.origin_lat, 'lng': route_opt.origin_lng},
            'destination': {'lat': route_opt.destination_lat, 'lng': route_opt.destination_lng},
            'route': optimized_route['route'],  # alias for frontend
            'optimized_route': optimized_route['route'],
            'estimated_time': optimized_route['estimated_time'],
            'distance': optimized_route['distance'],
            'congestion_avoidance': avoid_congestion
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/alerts/subscribe', methods=['POST'])
def subscribe_alerts():
    """Subscribe to traffic alerts for a location"""
    try:
        data = request.get_json()
        email = data.get('email')
        location_id = data.get('location_id')
        threshold_level = data.get('threshold_level', 'medium')
        
        if not email or not location_id:
            return jsonify({'error': 'Email and location_id required'}), 400
        
        # Check if subscription already exists
        existing = AlertSubscription.query.filter_by(
            email=email,
            location_id=location_id
        ).first()
        
        if existing:
            existing.is_active = True
            existing.threshold_level = threshold_level
        else:
            subscription = AlertSubscription(
                email=email,
                location_id=location_id,
                threshold_level=threshold_level
            )
            db.session.add(subscription)
        
        db.session.commit()
        
        return jsonify({'message': 'Alert subscription created/updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/alerts/unsubscribe', methods=['POST'])
def unsubscribe_alerts():
    """Unsubscribe from traffic alerts"""
    try:
        data = request.get_json()
        email = data.get('email')
        location_id = data.get('location_id')
        
        if not email:
            return jsonify({'error': 'Email required'}), 400
        
        query = AlertSubscription.query.filter_by(email=email)
        if location_id:
            query = query.filter_by(location_id=location_id)
        
        subscriptions = query.all()
        for sub in subscriptions:
            sub.is_active = False
        
        db.session.commit()
        
        return jsonify({'message': 'Unsubscribed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/data/upload', methods=['POST'])
def upload_traffic_data():
    """Upload traffic data from external sources"""
    try:
        data = request.get_json()
        
        if not data.get('traffic_data'):
            return jsonify({'error': 'No traffic data provided'}), 400
        
        data_processor = DataProcessor()
        processed_data = data_processor.process_traffic_data(data['traffic_data'])
        
        # Store processed data
        for item in processed_data:
            traffic_entry = TrafficData(
                location_id=item['location_id'],
                latitude=item['latitude'],
                longitude=item['longitude'],
                vehicle_count=item['vehicle_count'],
                average_speed=item['average_speed'],
                congestion_level=item['congestion_level'],
                data_source=item['data_source'],
                raw_data=json.dumps(item.get('raw_data', {}))
            )
            db.session.add(traffic_entry)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully processed {len(processed_data)} traffic records',
            'count': len(processed_data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/stats/summary', methods=['GET'])
def get_traffic_stats():
    """Get traffic statistics summary"""
    try:
        # Get data for last 24 hours
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        # Count by congestion level
        congestion_stats = db.session.query(
            TrafficData.congestion_level,
            db.func.count(TrafficData.id)
        ).filter(
            TrafficData.timestamp >= yesterday
        ).group_by(TrafficData.congestion_level).all()
        
        # Average vehicle count
        avg_vehicles = db.session.query(
            db.func.avg(TrafficData.vehicle_count)
        ).filter(
            TrafficData.timestamp >= yesterday
        ).scalar() or 0
        
        # Total predictions made
        total_predictions = TrafficPrediction.query.filter(
            TrafficPrediction.timestamp >= yesterday
        ).count()
        
        return jsonify({
            'period': 'last_24_hours',
            'congestion_distribution': dict(congestion_stats),
            'average_vehicles': round(avg_vehicles, 2),
            'total_predictions': total_predictions,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
