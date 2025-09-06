from flask import Blueprint, jsonify
from utils.auth import jwt_required_custom

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/summary', methods=['GET'])
@jwt_required_custom
def get_customer_stats():
    try:
        from models.customer import Customer
        stats = Customer.get_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch customer statistics',
            'error': str(e)
        }), 500

@stats_bp.route('/trends', methods=['GET'])
@jwt_required_custom
def get_trends():
    # TODO: Implement actual database queries for trends
    return jsonify({
        'success': True,
        'data': [
            {'month': 'Jan', 'enrollments': 87},
            {'month': 'Feb', 'enrollments': 124},
            {'month': 'Mar', 'enrollments': 156},
            {'month': 'Apr', 'enrollments': 132},
            {'month': 'May', 'enrollments': 198},
            {'month': 'Jun', 'enrollments': 234}
        ]
    })
