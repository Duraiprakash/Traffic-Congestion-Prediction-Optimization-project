# Raw Traffic Data

This directory contains raw traffic data from various sources:

- **camera_feeds/**: Traffic camera images and videos
- **sensor_data/**: IoT sensor readings (speed, density, etc.)
- **gps_data/**: GPS tracking data from vehicles
- **historical/**: Historical traffic patterns and events

## Data Sources

1. **Traffic Cameras**: CCTV feeds for vehicle detection
2. **IoT Sensors**: Road sensors for real-time traffic data
3. **GPS Data**: Vehicle tracking and speed data
4. **Weather Data**: Weather conditions affecting traffic
5. **Events Data**: Special events that impact traffic patterns

## Data Format

All data files should follow these naming conventions:
- `YYYY-MM-DD_HH-MM-SS_source_type.json`
- Example: `2024-01-15_14-30-00_camera_vehicles.json`

## Privacy and Security

- All personal data should be anonymized
- GPS coordinates should be rounded to appropriate precision
- License plates should be blurred or removed from images
