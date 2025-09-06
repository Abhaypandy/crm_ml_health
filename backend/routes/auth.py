from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.admin import Admin
from utils.auth import jwt_required_custom

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        admin = Admin.verify_credentials(username, password)
        
        if admin:
            access_token = create_access_token(identity=admin)
            return jsonify({
                'success': True,
                'data': {
                    'token': access_token,
                    'admin': admin
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required_custom
def logout():
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })

@auth_bp.route('/profile', methods=['GET'])
@jwt_required_custom
def profile():
    current_user = get_jwt_identity()
    return jsonify({
        'success': True,
        'data': current_user
    })
