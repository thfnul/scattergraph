#!/usr/bin/env python3
import sqlite3
import os
from datetime import datetime
import shutil

def backup_database():
    # Create backups directory if it doesn't exist
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Generate timestamp for backup filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'scattergraph_{timestamp}.db')

    try:
        # Copy the database file
        shutil.copy2('scattergraph.db', backup_path)
        print(f"Database backed up successfully to {backup_path}")

        # Create SQL dump
        conn = sqlite3.connect('scattergraph.db')
        with open(os.path.join(backup_dir, f'scattergraph_{timestamp}.sql'), 'w') as f:
            for line in conn.iterdump():
                f.write(f'{line}\n')
        print(f"SQL dump created successfully")
        conn.close()

    except Exception as e:
        print(f"Backup failed: {str(e)}")

if __name__ == '__main__':
    backup_database() 