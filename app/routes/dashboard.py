"""
Dashboard routes for Traffic Congestion Prediction System
"""

from flask import Blueprint, render_template, jsonify, request
from app.models.database import db
from app.models.traffic_models import TrafficData, TrafficPrediction
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@dashboard_bp.route('/map')
def traffic_map():
    """Interactive traffic map"""
    return render_template('map.html')

@dashboard_bp.route('/predictions')
def predictions():
    """Traffic predictions page"""
    return render_template('predictions.html')

@dashboard_bp.route('/routes')
def routes():
    """Route optimization page"""
    return render_template('routes.html')

@dashboard_bp.route('/alerts')
def alerts():
    """Traffic alerts page"""
    return render_template('alerts.html')

@dashboard_bp.route('/analytics')
def analytics():
    """Traffic analytics page"""
    return render_template('analytics.html')

@dashboard_bp.route('/api/dashboard-data')
def dashboard_data():
    """Get data for dashboard widgets"""
    try:
        # Get recent traffic data
        recent_time = datetime.utcnow() - timedelta(hours=1)
        recent_traffic = TrafficData.query.filter(
            TrafficData.timestamp >= recent_time
        ).all()
        
        # Calculate statistics
        total_locations = len(set(data.location_id for data in recent_traffic))
        high_congestion = len([d for d in recent_traffic if d.congestion_level == 'high'])
        medium_congestion = len([d for d in recent_traffic if d.congestion_level == 'medium'])
        low_congestion = len([d for d in recent_traffic if d.congestion_level == 'low'])
        
        # Get recent predictions
        recent_predictions = TrafficPrediction.query.filter(
            TrafficPrediction.timestamp >= recent_time
        ).all()
        
        return jsonify({
            'timestamp': datetime.utcnow().isoformat(),
            'summary': {
                'total_locations': total_locations,
                'high_congestion': high_congestion,
                'medium_congestion': medium_congestion,
                'low_congestion': low_congestion,
                'total_predictions': len(recent_predictions)
            },
            'traffic_data': [data.to_dict() for data in recent_traffic[-50:]],  # Last 50 records
            'predictions': [pred.to_dict() for pred in recent_predictions[-20:]]  # Last 20 predictions
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/api/heatmap-data')
def heatmap_data():
    """Get data for traffic heatmap"""
    try:
        # Get traffic data for heatmap visualization
        recent_time = datetime.utcnow() - timedelta(minutes=30)
        traffic_data = TrafficData.query.filter(
            TrafficData.timestamp >= recent_time
        ).all()
        
        heatmap_data = []
        for data in traffic_data:
            # Convert congestion level to intensity
            intensity_map = {'low': 0.3, 'medium': 0.6, 'high': 1.0}
            intensity = intensity_map.get(data.congestion_level, 0.3)
            
            heatmap_data.append({
                'lat': data.latitude,
                'lng': data.longitude,
                'intensity': intensity,
                'vehicle_count': data.vehicle_count,
                'congestion_level': data.congestion_level,
                'location_id': data.location_id
            })
        
        return jsonify({
            'timestamp': datetime.utcnow().isoformat(),
            'heatmap_data': heatmap_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/api/traffic-trends')
def traffic_trends():
    """Get traffic trends data for charts"""
    try:
        # Get data for last 24 hours, grouped by hour
        start_time = datetime.utcnow() - timedelta(hours=24)
        
        # Query traffic data by hour
        hourly_data = db.session.query(
            db.func.date_trunc('hour', TrafficData.timestamp).label('hour'),
            db.func.avg(TrafficData.vehicle_count).label('avg_vehicles'),
            db.func.avg(TrafficData.average_speed).label('avg_speed'),
            db.func.count(TrafficData.id).label('data_points')
        ).filter(
            TrafficData.timestamp >= start_time
        ).group_by(
            db.func.date_trunc('hour', TrafficData.timestamp)
        ).order_by('hour').all()
        
        trends_data = []
        for row in hourly_data:
            trends_data.append({
                'hour': row.hour.isoformat(),
                'avg_vehicles': round(row.avg_vehicles or 0, 2),
                'avg_speed': round(row.avg_speed or 0, 2),
                'data_points': row.data_points
            })
        
        return jsonify({
            'period': '24_hours',
            'trends': trends_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
