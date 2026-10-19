# Reporting module - organized for Addas's upcoming responsibility.
import catalog
import entries
import storage


def statement(database, month, location=None):
    entries.check_month(month)
    totals = {'Sale': 0, 'Purchase': 0, 'Supply purchase': 0, 'Fixed': 0}
    if location is not None:
        storage.check_location(database, location)
    rows = database.execute('''SELECT location, kind, cents FROM activity
                               WHERE substr(day,1,7)=?''', (month,)).fetchall()
    for place, kind, cents in rows:
        if (location is None or location == place) and kind in totals:
            totals[kind] = totals[kind] + cents
    totals['Net'] = totals['Sale'] - totals['Purchase'] - totals['Supply purchase'] - totals['Fixed']
    return totals


def income_text(database, month, location=None):
    totals = statement(database, month, location)
    title = 'Entire company'
    selected = storage.locations(database)
    if location is not None:
        for place, name in selected:
            if place == location:
                title = name
    text = f'INCOME STATEMENT: {title}\nMonth: {month}\n\n'
    labels = {'Sale': 'Sales revenue', 'Purchase': 'Clothing purchase expenses',
              'Supply purchase': 'Supply expenses', 'Fixed': 'Fixed expenses', 'Net': 'Net income'}
    for key in labels:
        text += f'{labels[key]}: {catalog.money(totals[key])}\n'
    text += '\nFixed expense detail (recorded charges only):\n'
    for item in catalog.FIXED:
        amount = 0
        for place, cents in database.execute('''SELECT location,cents FROM activity
                WHERE kind='Fixed' AND item=? AND substr(day,1,7)=?''', (item, month)):
            if location is None or place == location:
                amount += cents
        text += f'{item}: {catalog.money(amount)}\n'
    text += '\nFixed expenses must be applied explicitly. Missing charges:\n'
    missing = False
    for place, name in selected:
        if location is None or place == location:
            if not database.execute('SELECT 1 FROM monthly WHERE location=? AND month=?',
                                    (place, month)).fetchone():
                text += name + '\n'
                missing = True
    if not missing:
        text += 'None\n'
    return text


def product_text(database, start, end):
    entries.check_day(start)
    entries.check_day(end)
    if start > end:
        raise ValueError('Start date must be on or before end date.')
    text = f'PRODUCT SALES: {start} through {end} (inclusive)\n'
    for place, name in storage.locations(database):
        text += f'\n{name}\n'
        for item in catalog.CLOTHING:
            quantity = database.execute('''SELECT COALESCE(-SUM(quantity),0)
                FROM activity WHERE location=? AND item=? AND kind='Sale'
                AND day>=? AND day<=?''', (place, item, start, end)).fetchone()[0]
            text += f'  {item}: {quantity}\n'
    return text
