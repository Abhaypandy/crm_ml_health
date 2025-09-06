from utils.database import get_db_connection, dict_factory
from utils.auth import hash_password, verify_password

class Admin:
    def __init__(self, id=None, username=None, password=None):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def create_default_admin():
        """Create default admin user"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM admins')
            count = cursor.fetchone()[0]
            
            if count == 0:
                hashed_password = hash_password('admin123')
                cursor.execute(
                    'INSERT INTO admins (username, password_hash) VALUES (?, ?)',
                    ('admin@gmail.com', hashed_password)
                )
                conn.commit()
                print('Default admin created: username=admin@gmail.com, password=admin123')
                return True
            return False

    @staticmethod
    def verify_credentials(username, password):
        """Verify admin credentials"""
        with get_db_connection() as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM admins WHERE username = ?', (username,))
            admin = cursor.fetchone()
            
            if admin and verify_password(password, admin['password_hash']):
                return {
                    'id': admin['id'],
                    'username': admin['username']
                }
            return None
