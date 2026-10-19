# Inventory and sales module - organized for Bret's upcoming responsibility.
from datetime import date
import catalog
import storage


def check_day(text):
    try:
        result = date.fromisoformat(text)
    except (ValueError, TypeError):
        raise ValueError('Enter a real date as YYYY-MM-DD.')
    if result.isoformat() != text:
        raise ValueError('Use the date format YYYY-MM-DD.')
    return text


def check_month(text):
    check_day(text + '-01')
    return text


def whole_number(text, allow_zero=False):
    text = str(text).strip()
    if not text.isascii() or not text.isdigit():
        raise ValueError('Quantity must be a whole number.')
    quantity = int(text)
    if quantity < 1 and not allow_zero:
        raise ValueError('Quantity must be greater than zero.')
    if quantity > 1000000:
        raise ValueError('Enter no more than 1,000,000 units per entry.')
    return quantity


def record(database, location, day, kind, quantities):
    check_day(day)
    storage.check_location(database, location)
    if kind not in ('Purchase', 'Sale', 'Supply purchase', 'Supply usage', 'Opening'):
        raise ValueError('Unknown entry type.')
    if not quantities:
        raise ValueError('Enter at least one item.')
    # Validate all lines before writing any. A transaction also protects against
    # partial saves if an insert fails. BEGIN IMMEDIATE locks other writers.
    try:
        database.execute('BEGIN IMMEDIATE')
        rows = []
        for item in quantities:
            quantity = whole_number(quantities[item])
            cents = 0
            units = quantity
            if kind in ('Purchase', 'Sale'):
                if item not in catalog.CLOTHING:
                    raise ValueError('Choose a clothing item.')
                price = catalog.CLOTHING[item][0]
                if kind == 'Sale':
                    price = catalog.CLOTHING[item][1]
                    units = -quantity
                cents = price * quantity
            elif kind == 'Supply purchase':
                if item not in catalog.SUPPLIES:
                    raise ValueError('Choose a supply.')
                price, pack_size = catalog.SUPPLIES[item]
                cents = price * quantity
                units = pack_size * quantity
            elif kind == 'Supply usage':
                if item not in catalog.SUPPLIES:
                    raise ValueError('Choose a supply.')
                units = -quantity
            elif item not in catalog.CLOTHING and item not in catalog.SUPPLIES:
                raise ValueError('Choose a known item.')
            if storage.stock(database, location, item) + units < 0:
                raise ValueError(f'Insufficient {item}. No part of this entry was saved.')
            rows.append((location, day, kind, item, units, cents))
        database.executemany('''INSERT INTO activity
            (location,day,kind,item,quantity,cents) VALUES (?,?,?,?,?,?)''', rows)
        database.commit()
    except Exception:
        database.rollback()
        raise


def apply_monthly(database, location, month):
    check_month(month)
    storage.check_location(database, location)
    try:
        database.execute('BEGIN IMMEDIATE')
        if database.execute('SELECT 1 FROM monthly WHERE location=? AND month=?',
                            (location, month)).fetchone():
            raise ValueError('Fixed expenses already applied for this location and month.')
        database.execute('INSERT INTO monthly VALUES (?,?)', (location, month))
        for item in catalog.FIXED:
            database.execute('''INSERT INTO activity
                (location,day,kind,item,quantity,cents) VALUES (?,?,?,?,?,?)''',
                (location, month + '-01', 'Fixed', item, 0, catalog.FIXED[item]))
        database.commit()
    except Exception:
        database.rollback()
        raise
