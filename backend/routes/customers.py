from flask import Blueprint, request, jsonify
from models.customer import Customer
from utils.auth import jwt_required_custom
import uuid
from datetime import datetime

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('', methods=['GET'])
@jwt_required_custom
def get_customers():
    try:
        filters = {
            'search': request.args.get('search', ''),
            'status': request.args.get('status', ''),
            'familyType': request.args.get('familyType', ''),
            'salesmanId': request.args.get('salesmanId', '')
        }
        
        customers = Customer.search(filters)
        
        return jsonify({
            'success': True,
            'data': customers,
            'total': len(customers)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch customers',
            'error': str(e)
        }), 500

@customers_bp.route('/bulk', methods=['POST'])
@jwt_required_custom
def add_customers_bulk():
    try:
        data = request.get_json()
        customers_data = data.get('customers', [])
        
        if not isinstance(customers_data, list) or len(customers_data) == 0:
            return jsonify({
                'success': False,
                'message': 'Invalid customers data. Expected array of customers.'
            }), 400
        
        added = 0
        errors = []
        
        for i, customer_data in enumerate(customers_data):
            try:
                # Validate required fields
                if not customer_data.get('regId') or not customer_data.get('name') or not customer_data.get('contact'):
                    errors.append(f'Customer {i + 1}: Missing required fields')
                    continue
                
                # Create customer
                customer = Customer(
                    regId=customer_data['regId'],
                    name=customer_data['name'],
                    contact=customer_data['contact'],
                    salesmanId=customer_data.get('salesmanId', ''),
                    status=customer_data.get('status', 'Active'),
                    familyType=customer_data.get('familyType', 'Individual'),
                    familyMembers=customer_data.get('familyMembers', ''),
                    joinDate=customer_data.get('joinDate', datetime.now().strftime('%Y-%m-%d')),
                    membership=customer_data.get('membership', 'Silver')
                )
                
                if customer.save():
                    added += 1
                else:
                    errors.append(f'Failed to save customer {customer_data.get("regId", i+1)}')
                    
            except Exception as e:
                errors.append(f'Error adding customer {customer_data.get("regId", i+1)}: {str(e)}')
        
        return jsonify({
            'success': True,
            'message': f'Successfully added {added} customers',
            'added': added,
            'errors': errors,
            'total': len(customers_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to add customers',
            'error': str(e)
        }), 500
