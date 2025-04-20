# Scattergraph 3.0

A creative image scattering tool that allows users to create unique compositions from a curated collection of images. Built with vanilla JavaScript and Python, featuring a modern, aesthetic interface with real-time canvas manipulation.

## Features

- Interactive image selection interface with directory-based organization
- Real-time canvas manipulation with dynamic image placement
- Adjustable scale, rotation, and position parameters
- Image usage tracking with serial number system
- Administrative interface for usage analytics
- Modern, aesthetic UI with custom animations and effects

## Requirements

- Python 3.6+
- Modern web browser with JavaScript enabled
- Local image directory structure

## Installation

1. Clone the repository:
```bash
git clone https://github.com/thfnul/scattergraph.git
cd scattergraph
```

2. Start the Python server:
```bash
python3 server.py
```

3. Access the application:
- Main application: http://localhost:8000/index.html
- Admin interface: http://localhost:8000/admin.html

## Usage

1. Select images from the directory grid
2. Use the toolbar controls to adjust:
   - Scale (Min/Max)
   - Rotation range
   - Position wobble
3. Click or drag on the canvas to scatter images
4. Save your composition with automatic watermarking

## Controls

- **Q/Shift+Q**: Adjust minimum scale
- **W/Shift+W**: Adjust maximum scale
- **A/Shift+A**: Adjust rotation range
- **S/Shift+S**: Adjust position wobble
- **L**: Lock current image selection

## Development

The project uses:
- Vanilla JavaScript for front-end functionality
- Python with SQLite for back-end services
- Custom CSS animations and transitions
- OCR-A and BW Stretch fonts for typography

## Database Management

The application uses SQLite for data storage. While database files are not version controlled, we maintain database integrity through:

1. Schema Version Control:
   - Database structure is defined in `schema.sql`
   - Run `sqlite3 scattergraph.db < schema.sql` to initialize the database

2. Backup System:
   - Use `python3 backup_db.py` to create timestamped backups
   - Backups include both .db file copies and SQL dumps
   - Backup files are stored in the `backups/` directory

## License

All rights reserved. © 2024 Therefore, Nul 