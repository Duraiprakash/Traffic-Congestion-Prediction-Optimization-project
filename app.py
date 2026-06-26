"""
Traffic Congestion Prediction & Optimization - Main Application
MCA Final Year Project
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from app.models.database import db
from app.routes.api import api_bp
from app.routes.dashboard import dashboard_bp
from app.utils.data_processor import DataProcessor
from app.utils.model_manager import ModelManager

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(
        __name__,
        template_folder='app/templates',
        static_folder='app/static'
    )
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp)
    
    # Initialize utilities
    app.data_processor = DataProcessor()
    app.model_manager = ModelManager()
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def index():
        """Main dashboard route"""
        return render_template('index.html')
    
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'Traffic Congestion Prediction System is running'
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Traffic Congestion Prediction System')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--host', default='0.0.0.0', help='Host to run on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on')
    parser.add_argument('--config', default='development', help='Configuration to use')
    
    args = parser.parse_args()
    
    app = create_app(args.config)
    
    if args.debug:
        app.config['DEBUG'] = True
    
    print(f"🚦 Starting Traffic Congestion Prediction System...")
    print(f"🌐 Dashboard: http://{args.host}:{args.port}")
    print(f"📊 API: http://{args.host}:{args.port}/api")
    
    app.run(host=args.host, port=args.port, debug=args.debug)
