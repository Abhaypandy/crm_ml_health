import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = 'healthcare_crm.db'

def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create admins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id TEXT PRIMARY KEY,
            regId TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            salesmanId TEXT NOT NULL,
            status TEXT CHECK(status IN ('Active', 'Inactive')) NOT NULL DEFAULT 'Active',
            familyType TEXT CHECK(familyType IN ('Family', 'Individual')) NOT NULL,
            familyMembers TEXT NOT NULL,
            joinDate TEXT NOT NULL,
            membership TEXT CHECK(membership IN ('Gold', 'Silver', 'Platinum')) NOT NULL DEFAULT 'Silver',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def dict_factory(cursor, row):
    """Convert sqlite3.Row to dictionary"""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
