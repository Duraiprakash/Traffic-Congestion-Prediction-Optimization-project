"""
Data processing utilities for traffic data
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import math

class DataProcessor:
    """Handles traffic data processing and analysis"""
    
    def __init__(self):
        self.congestion_thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8
        }
    
    def process_traffic_data(self, raw_data):
        """Process raw traffic data and calculate congestion levels"""
        processed_data = []
        
        for item in raw_data:
            # Calculate congestion level based on vehicle count and speed
            congestion_level = self._calculate_congestion_level(
                vehicle_count=item.get('vehicle_count', 0),
                average_speed=item.get('average_speed', 0),
                max_capacity=item.get('max_capacity', 50)  # Default max capacity
            )
            
            processed_item = {
                'location_id': item.get('location_id'),
                'latitude': item.get('latitude'),
                'longitude': item.get('longitude'),
                'vehicle_count': item.get('vehicle_count', 0),
                'average_speed': item.get('average_speed', 0),
                'congestion_level': congestion_level,
                'data_source': item.get('data_source', 'unknown'),
                'timestamp': item.get('timestamp', datetime.utcnow().isoformat()),
                'raw_data': item
            }
            
            processed_data.append(processed_item)
        
        return processed_data
    
    def _calculate_congestion_level(self, vehicle_count, average_speed, max_capacity):
        """Calculate congestion level based on vehicle density and speed"""
        # Normalize vehicle count (0-1)
        density = min(vehicle_count / max_capacity, 1.0)
        
        # Speed factor (lower speed = higher congestion)
        speed_factor = max(0, min(average_speed / 50.0, 1.0))  # Normalize speed
        
        # Combined congestion score
        congestion_score = (density * 0.7) + ((1 - speed_factor) * 0.3)
        
        if congestion_score <= self.congestion_thresholds['low']:
            return 'low'
        elif congestion_score <= self.congestion_thresholds['medium']:
            return 'medium'
        else:
            return 'high'
    
    def optimize_route(self, origin_lat, origin_lng, dest_lat, dest_lng, avoid_congestion=True):
        """Optimize route between origin and destination"""
        # Simple route optimization algorithm
        # In a real implementation, this would use actual routing algorithms
        
        # Calculate straight-line distance
        distance = self._calculate_distance(origin_lat, origin_lng, dest_lat, dest_lng)
        
        # Simulate route optimization
        if avoid_congestion:
            # Add some waypoints to avoid congested areas
            waypoints = self._generate_waypoints(origin_lat, origin_lng, dest_lat, dest_lng)
            route = [{'lat': origin_lat, 'lng': origin_lng}] + waypoints + [{'lat': dest_lat, 'lng': dest_lng}]
            # Increase time slightly for congestion avoidance
            estimated_time = distance * 0.02 * 1.2  # 20% longer for congestion avoidance
        else:
            route = [{'lat': origin_lat, 'lng': origin_lng}, {'lat': dest_lat, 'lng': dest_lng}]
            estimated_time = distance * 0.02  # 2 minutes per km
        
        return {
            'route': route,
            'distance': distance,
            'estimated_time': estimated_time,
            'congestion_avoidance': avoid_congestion
        }
    
    def _calculate_distance(self, lat1, lng1, lat2, lng2):
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth's radius in kilometers
        
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlng/2) * math.sin(dlng/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance
    
    def _generate_waypoints(self, origin_lat, origin_lng, dest_lat, dest_lng):
        """Generate waypoints to avoid congested areas"""
        # Simple waypoint generation - in reality, this would use actual traffic data
        waypoints = []
        
        # Add one waypoint in the middle, slightly offset
        mid_lat = (origin_lat + dest_lat) / 2
        mid_lng = (origin_lng + dest_lng) / 2
        
        # Add small offset to simulate avoiding congested areas
        offset_lat = mid_lat + 0.001
        offset_lng = mid_lng + 0.001
        
        waypoints.append({'lat': offset_lat, 'lng': offset_lng})
        
        return waypoints
    
    def analyze_traffic_patterns(self, traffic_data, time_window_hours=24):
        """Analyze traffic patterns from historical data"""
        if not traffic_data:
            return {}
        
        df = pd.DataFrame(traffic_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Group by hour to find patterns
        hourly_stats = df.groupby(df['timestamp'].dt.hour).agg({
            'vehicle_count': ['mean', 'std'],
            'average_speed': ['mean', 'std'],
            'congestion_level': lambda x: (x == 'high').sum()
        }).round(2)
        
        # Find peak hours
        peak_hours = hourly_stats[('vehicle_count', 'mean')].nlargest(3).index.tolist()
        
        # Calculate overall statistics
        total_records = len(df)
        high_congestion_ratio = (df['congestion_level'] == 'high').sum() / total_records
        
        return {
            'total_records': total_records,
            'high_congestion_ratio': high_congestion_ratio,
            'peak_hours': peak_hours,
            'hourly_stats': hourly_stats.to_dict(),
            'analysis_period_hours': time_window_hours
        }
    
    def detect_anomalies(self, traffic_data):
        """Detect traffic anomalies and unusual patterns"""
        if len(traffic_data) < 10:
            return []
        
        df = pd.DataFrame(traffic_data)
        
        # Calculate z-scores for vehicle count and speed
        vehicle_mean = df['vehicle_count'].mean()
        vehicle_std = df['vehicle_count'].std()
        speed_mean = df['average_speed'].mean()
        speed_std = df['average_speed'].std()
        
        anomalies = []
        for idx, row in df.iterrows():
            vehicle_zscore = abs((row['vehicle_count'] - vehicle_mean) / vehicle_std) if vehicle_std > 0 else 0
            speed_zscore = abs((row['average_speed'] - speed_mean) / speed_std) if speed_std > 0 else 0
            
            # Mark as anomaly if z-score > 2
            if vehicle_zscore > 2 or speed_zscore > 2:
                anomalies.append({
                    'timestamp': row['timestamp'],
                    'location_id': row['location_id'],
                    'anomaly_type': 'traffic_spike' if vehicle_zscore > 2 else 'speed_anomaly',
                    'severity': 'high' if max(vehicle_zscore, speed_zscore) > 3 else 'medium',
                    'vehicle_count': row['vehicle_count'],
                    'average_speed': row['average_speed']
                })
        
        return anomalies
