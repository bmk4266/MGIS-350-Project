# Storage module - organized for Sai's upcoming Report 2 responsibility.
# Generated starting implementation; this is not a claim of teammate authorship.
import sqlite3
from pathlib import Path


def open_database(filename):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    database = sqlite3.connect(filename)
    database.execute('PRAGMA foreign_keys = ON')
    # IF NOT EXISTS preserves records when the application restarts.
    database.executescript('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE COLLATE NOCASE);
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY,
            location INTEGER NOT NULL REFERENCES locations(id),
            day TEXT NOT NULL, kind TEXT NOT NULL, item TEXT NOT NULL,
            quantity INTEGER NOT NULL, cents INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS monthly (
            location INTEGER NOT NULL REFERENCES locations(id),
            month TEXT NOT NULL, PRIMARY KEY(location, month));
    ''')
    database.commit()
    return database


def locations(database):
    return database.execute('SELECT id, name FROM locations ORDER BY id').fetchall()


def add_location(database, name):
    name = name.strip()
    if not name or len(name) > 80:
        raise ValueError('Location name must contain 1 to 80 characters.')
    try:
        with database:
            database.execute('INSERT INTO locations(name) VALUES (?)', (name,))
    except sqlite3.IntegrityError:
        raise ValueError('That location name already exists.')


def check_location(database, location):
    if not database.execute('SELECT id FROM locations WHERE id=?', (location,)).fetchone():
        raise ValueError('Select an existing location.')


def stock(database, location, item):
    row = database.execute('''SELECT COALESCE(SUM(quantity), 0) FROM activity
                              WHERE location=? AND item=?''', (location, item)).fetchone()
    return row[0]
