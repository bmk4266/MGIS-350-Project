# Safe, separate demonstration setup. Existing demo records are never replaced.
from pathlib import Path
import storage
import entries


def create_demo():
    filename = Path(__file__).resolve().parent / 'demo_data' / 'threads_trends.sqlite3'
    if filename.exists():
        print('Demo database already exists; preserved without changes.')
        return
    database = storage.open_database(filename)
    try:
        storage.add_location(database, 'DEMO - Central')
        storage.add_location(database, 'DEMO - East')
        entries.record(database, 1, '2026-10-01', 'Purchase', {'T-Shirt': 10})
        entries.record(database, 1, '2026-10-02', 'Sale', {'T-Shirt': 3})
        entries.apply_monthly(database, 1, '2026-10')
        entries.record(database, 2, '2026-10-01', 'Opening', {'Jeans': 5})
        print('Demo ready. Central: 7 T-Shirts; October net income -$22,376.00.')
        print('Run: python app.py --demo')
    finally:
        database.close()


if __name__ == '__main__':
    create_demo()
