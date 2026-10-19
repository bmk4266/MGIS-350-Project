# Repeatable checks use temporary storage and never touch live or demo records.
from pathlib import Path
from tempfile import TemporaryDirectory
import sqlite3
import catalog
import storage
import entries
import reports


def rejected(function, *arguments):
    try:
        function(*arguments)
    except ValueError:
        return
    raise AssertionError('Invalid entry was accepted.')


def snapshot(database):
    return (database.execute('SELECT * FROM activity ORDER BY id').fetchall(),
            database.execute('SELECT * FROM monthly ORDER BY location,month').fetchall())


def main():
    with TemporaryDirectory() as folder:
        filename = Path(folder) / 'test.sqlite3'
        database = storage.open_database(filename)
        storage.add_location(database, 'First')
        storage.add_location(database, 'Second')
        rejected(storage.add_location, database, ' first ')
        rejected(storage.add_location, database, ' ')
        entries.record(database, 1, '2026-10-01', 'Purchase', {'T-Shirt': 10})
        assert storage.stock(database, 1, 'T-Shirt') == 10
        assert reports.statement(database, '2026-10', 1)['Purchase'] == 8000
        entries.record(database, 1, '2026-10-02', 'Sale', {'T-Shirt': 3})
        entries.apply_monthly(database, 1, '2026-10')
        total = reports.statement(database, '2026-10', 1)
        assert total == {'Sale': 5400, 'Purchase': 8000, 'Supply purchase': 0,
                         'Fixed': 2235000, 'Net': -2237600}
        assert storage.stock(database, 1, 'T-Shirt') == 7
        before = snapshot(database)
        rejected(entries.record, database, 1, '2026-10-03', 'Sale', {'T-Shirt': 8})
        rejected(entries.record, database, 1, '2026-10-03', 'Sale', {'T-Shirt': 1, 'Jeans': 1})
        rejected(entries.apply_monthly, database, 1, '2026-10')
        assert snapshot(database) == before
        assert storage.stock(database, 2, 'T-Shirt') == 0
        entries.record(database, 2, '2026-10-01', 'Opening', {'Jeans': 5})
        assert reports.statement(database, '2026-10', 2)['Purchase'] == 0
        entries.record(database, 2, '2026-10-31', 'Sale', {'Jeans': 2})
        entries.record(database, 2, '2026-11-01', 'Sale', {'Jeans': 1})
        entries.record(database, 2, '2026-09-30', 'Purchase', {'Jacket': 1})
        entries.record(database, 2, '2026-11-01', 'Purchase', {'Dress': 1})
        assert reports.statement(database, '2026-10', 2)['Sale'] == 9600
        assert reports.statement(database, '2026-10', 2)['Purchase'] == 0
        assert reports.statement(database, '2026-11', 2)['Sale'] == 4800
        assert 'Jeans: 2' in reports.product_text(database, '2026-10-31', '2026-10-31')
        assert 'Jeans: 1' in reports.product_text(database, '2026-11-01', '2026-11-01')
        for month in ('2026-09', '2026-10', '2026-11'):
            company = reports.statement(database, month)
            first = reports.statement(database, month, 1)
            second = reports.statement(database, month, 2)
            for key in company:
                assert company[key] == first[key] + second[key]
        entries.record(database, 1, '2026-10-04', 'Supply purchase',
                       {'Shopping bags': 2, 'Gift boxes': 1, 'Receipt paper': 3})
        assert storage.stock(database, 1, 'Shopping bags') == 1000
        assert storage.stock(database, 1, 'Gift boxes') == 100
        assert storage.stock(database, 1, 'Receipt paper') == 3
        assert reports.statement(database, '2026-10', 1)['Supply purchase'] == 14400
        entries.record(database, 1, '2026-10-04', 'Supply usage',
                       {'Shopping bags': 7, 'Gift boxes': 2, 'Receipt paper': 1})
        assert storage.stock(database, 1, 'Shopping bags') == 993
        assert storage.stock(database, 1, 'Gift boxes') == 98
        assert storage.stock(database, 1, 'Receipt paper') == 2
        before = snapshot(database)
        rejected(entries.record, database, 1, '2026-10-05', 'Supply usage', {'Shopping bags': 994})
        for day in ('2026-02-29', '2026-13-01', '20261001', '2026-1-01', ''):
            rejected(entries.record, database, 1, day, 'Purchase', {'T-Shirt': 1})
        for quantity in ('-1', '0', '1.5', 'text', '1000001'):
            rejected(entries.record, database, 1, '2026-10-05', 'Purchase', {'T-Shirt': quantity})
        rejected(entries.record, database, 99, '2026-10-05', 'Purchase', {'T-Shirt': 1})
        rejected(entries.record, database, 1, '2026-10-05', 'Purchase', {'Unknown': 1})
        rejected(reports.product_text, database, '2026-11-01', '2026-10-01')
        rejected(reports.statement, database, '2026-1')
        assert snapshot(database) == before
        reports.income_text(database, '2026-10')
        reports.income_text(database, '2026-10', 1)
        reports.product_text(database, '2026-01-01', '2026-12-31')
        assert snapshot(database) == before
        entries.check_day('2024-02-29')
        entries.apply_monthly(database, 2, '2026-10')
        entries.apply_monthly(database, 1, '2026-11')
        before = snapshot(database)
        database.close()
        database = storage.open_database(filename)
        assert snapshot(database) == before
        assert storage.stock(database, 1, 'T-Shirt') == 7
        rejected(entries.apply_monthly, database, 1, '2026-10')
        # Force a failure on the second line to verify rollback after an insert.
        database.execute('''CREATE TEMP TRIGGER fail_jeans BEFORE INSERT ON activity
            WHEN NEW.item='Jeans' BEGIN SELECT RAISE(ABORT, 'test failure'); END''')
        try:
            entries.record(database, 1, '2026-10-06', 'Purchase', {'T-Shirt': 1, 'Jeans': 1})
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError('Expected simulated storage failure.')
        assert snapshot(database) == before
        database.close()
        assert catalog.money(-2237600) == '-$22,376.00'
    print('PASS: purchases, sales, atomic rejection/rollback, supplies, opening stock,')
    print('locations, boundaries, company totals, read-only reports, validation,')
    print('restart persistence, duplicate monthly expenses, exact money formatting.')


if __name__ == '__main__':
    main()
