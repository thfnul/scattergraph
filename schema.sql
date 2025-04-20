-- Database schema for Scattergraph 3.0

-- Table: scattergrams
CREATE TABLE IF NOT EXISTS scattergrams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    canvas_width INTEGER,
    canvas_height INTEGER,
    intro_text TEXT
);

-- Table: serial_usage
CREATE TABLE IF NOT EXISTS serial_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scattergram_id INTEGER,
    serial_number TEXT,
    instance_count INTEGER,
    FOREIGN KEY (scattergram_id) REFERENCES scattergrams(id)
); 