from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import sqlite3
from datetime import datetime
from urllib.parse import parse_qs

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.end_headers()

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def init_db(self):
        db_path = 'scattergraph.db'
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Create scattergrams table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scattergrams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_agent TEXT,
                    ip_location TEXT,
                    total_placements INTEGER,
                    unique_serials INTEGER,
                    browser TEXT,
                    platform TEXT
                )
            """)
            
            # Create serial usage table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS serial_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scattergram_id INTEGER,
                    serial_number TEXT,
                    usage_count INTEGER,
                    FOREIGN KEY (scattergram_id) REFERENCES scattergrams(id)
                )
            """)
            
            conn.commit()

    def do_POST(self):
        if self.path == '/api/init-db':
            try:
                self.init_db()
                self.send_json_response({'success': True, 'message': 'Database initialized successfully'})
            except Exception as e:
                self.send_json_response(
                    {'success': False, 'message': f'Failed to initialize database: {str(e)}'}, 
                    500
                )
            
        elif self.path == '/api/track-usage':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                with sqlite3.connect('scattergraph.db') as conn:
                    cursor = conn.cursor()
                    
                    # Insert main record
                    cursor.execute("""
                        INSERT INTO scattergrams 
                        (created_at, user_agent, total_placements, 
                         unique_serials, browser, platform)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (datetime.now(), data['userAgent'],
                          data['totalPlacements'], data['uniqueSerials'],
                          data['browser'], data['platform']))
                    
                    scattergram_id = cursor.lastrowid
                    
                    # Insert serial usage
                    for serial_data in data['serialUsage']:
                        cursor.execute("""
                            INSERT INTO serial_usage (scattergram_id, serial_number, usage_count)
                            VALUES (?, ?, ?)
                        """, (scattergram_id, serial_data['serial'], serial_data['count']))
                    
                    self.send_json_response({
                        'success': True,
                        'sequenceNumber': scattergram_id
                    })
            except Exception as e:
                self.send_json_response({
                    'success': False,
                    'message': f'Failed to track usage: {str(e)}'
                }, 500)
        else:
            self.send_error(404)

    def do_GET(self):
        if self.path == '/images':
            images = {}
            # Look for PNG files in all subdirectories
            for dir_name in os.listdir('.'):
                if os.path.isdir(dir_name) and not dir_name.startswith('.'):
                    images[dir_name] = []
                    for file in os.listdir(dir_name):
                        if file.lower().endswith('.png'):
                            images[dir_name].append(f"{dir_name}/{file}")
            
            self.send_json_response(images)
        elif self.path == '/api/entries':
            try:
                with sqlite3.connect('scattergraph.db') as conn:
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()
                    
                    # First get all scattergrams
                    cursor.execute("""
                        SELECT * FROM scattergrams
                        ORDER BY created_at DESC
                    """)
                    
                    rows = cursor.fetchall()
                    entries = []
                    
                    for row in rows:
                        entry = dict(row)
                        
                        # Get serial usage for this scattergram
                        cursor.execute("""
                            SELECT serial_number, usage_count
                            FROM serial_usage
                            WHERE scattergram_id = ?
                        """, (entry['id'],))
                        
                        serial_rows = cursor.fetchall()
                        entry['serial_usage'] = [
                            {
                                'serial_number': sr['serial_number'],
                                'usage_count': sr['usage_count']
                            }
                            for sr in serial_rows
                        ]
                        
                        entries.append(entry)
                    
                    self.send_json_response(entries)
            except Exception as e:
                print(f"Database error: {str(e)}")  # Add server-side logging
                self.send_json_response({
                    'error': True,
                    'message': f'Failed to fetch entries: {str(e)}'
                }, 500)
        else:
            # Serve files directly
            return SimpleHTTPRequestHandler.do_GET(self)

# Initialize database when server starts
handler = CORSRequestHandler
handler.init_db(None)  # Initialize database on startup

print("Starting server at http://localhost:8000")
print("Make sure to access your app through: http://localhost:8000/index.html")
print("SQLite database initialized at: scattergraph.db")
HTTPServer(('localhost', 8000), handler).serve_forever()