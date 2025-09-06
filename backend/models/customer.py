from utils.database import get_db_connection, dict_factory
from datetime import datetime
import uuid

class Customer:
    def __init__(self, id=None, regId=None, name=None, contact=None, 
                 salesmanId=None, status='Active', familyType='Individual',
                 familyMembers='', joinDate=None, membership='Silver'):
        self.id = id or str(uuid.uuid4())
        self.regId = regId
        self.name = name
        self.contact = contact
        self.salesmanId = salesmanId
        self.status = status
        self.familyType = familyType
        self.familyMembers = familyMembers
        self.joinDate = joinDate or datetime.now().strftime('%Y-%m-%d')
        self.membership = membership

    def save(self):
        """Save customer to database"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO customers 
                (id, regId, name, contact, salesmanId, status, familyType, familyMembers, joinDate, membership)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.id, self.regId, self.name, self.contact, self.salesmanId,
                self.status, self.familyType, self.familyMembers, self.joinDate, self.membership
            ))
            conn.commit()
            return True

    @staticmethod
    def search(filters):
        """Search customers with filters"""
        with get_db_connection() as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            
            query = 'SELECT * FROM customers WHERE 1=1'
            params = []
            
            if filters.get('search'):
                query += ' AND (name LIKE ? OR contact LIKE ? OR regId LIKE ?)'
                search_term = f"%{filters['search']}%"
                params.extend([search_term, search_term, search_term])
            
            query += ' ORDER BY created_at DESC'
            
            cursor.execute(query, params)
            return cursor.fetchall()

    @staticmethod
    def get_stats():
        """Get customer statistics"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active,
                    SUM(CASE WHEN status = 'Inactive' THEN 1 ELSE 0 END) as inactive,
                    SUM(CASE WHEN familyType = 'Family' THEN 1 ELSE 0 END) as families,
                    SUM(CASE WHEN familyType = 'Individual' THEN 1 ELSE 0 END) as individuals,
                    SUM(CASE WHEN membership = 'Gold' THEN 1 ELSE 0 END) as gold,
                    SUM(CASE WHEN membership = 'Silver' THEN 1 ELSE 0 END) as silver,
                    SUM(CASE WHEN membership = 'Platinum' THEN 1 ELSE 0 END) as platinum
                FROM customers
            ''')
            
            result = cursor.fetchone()
            return {
                'total': result[0] or 0,
                'active': result[1] or 0,
                'inactive': result[2] or 0,
                'families': result[3] or 0,
                'individuals': result[4] or 0,
                'membershipBreakdown': {
                    'gold': result[5] or 0,
                    'silver': result[6] or 0,
                    'platinum': result[7] or 0
                }
            }
