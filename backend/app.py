import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Import routes
from routes.auth import auth_bp
from routes.customers import customers_bp
from routes.stats import stats_bp

# Import models and utilities
from models.admin import Admin
from utils.database import init_database

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'healthcare_crm_secret_key_change_in_production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Tokens don't expire
    
    # Initialize extensions
    CORS(app)
    jwt = JWTManager(app)
    
    # Initialize database
    init_database()
    Admin.create_default_admin()
    
    # Health check endpoints
    @app.route('/api/ping', methods=['GET'])
    def ping():
        return jsonify({
            'message': os.getenv('PING_MESSAGE', 'ping')
        })
    
    @app.route('/api/demo', methods=['GET'])
    def demo():
        return jsonify({
            'message': 'Hello from Flask server'
        })
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(customers_bp, url_prefix='/api/customers')
    app.register_blueprint(stats_bp, url_prefix='/api/stats')
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Flask server starting...")
    print("📱 Backend: http://localhost:5000")
    print("🔧 API: http://localhost:5000/api")
    app.run(debug=True, host='0.0.0.0', port=5000)
