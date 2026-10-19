# Local browser interface. Uses only Python's standard library and existing modules.
# HTTP forms are beyond the course notes; entry and reporting logic stays shared.
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlencode
from html import escape
from pathlib import Path
from datetime import date
import secrets
import sqlite3
import sys
import catalog
import entries
import storage
import reports

ROOT = Path(__file__).resolve().parent
TOKEN = secrets.token_urlsafe(32)
HOST = '127.0.0.1'
PORT = 8000


def value(form, key, default=''):
    return form.get(key, [default])[0]


def field(label, name, contents='', kind='text'):
    return (f'<label>{escape(label)}<input type="{kind}" name="{name}" '
            f'value="{escape(str(contents), quote=True)}"></label>')


def page(database, form, message=''):
    mode = value(form, 'mode', 'demo')
    places = storage.locations(database)
    location = value(form, 'location', str(places[0][0]) if places else '')
    month = value(form, 'month', '2026-10' if mode == 'demo' else date.today().strftime('%Y-%m'))
    day = value(form, 'day', date.today().isoformat())
    options = '<option value="">Select a location</option>'
    for place, name in places:
        selected = ' selected' if str(place) == location else ''
        options += f'<option value="{place}"{selected}>{escape(name)}</option>'
    report = ''
    action = value(form, 'report', 'inventory')
    try:
        if action == 'company':
            report = reports.income_text(database, month)
        elif action == 'products':
            report = reports.product_text(database, value(form, 'start', month + '-01'),
                                           value(form, 'end', month + '-28'))
        elif location:
            place = int(location)
            storage.check_location(database, place)
            if action == 'income':
                report = reports.income_text(database, month, place)
            else:
                for item in list(catalog.CLOTHING) + list(catalog.SUPPLIES):
                    unit = 'cases' if item == 'Receipt paper' else 'units'
                    report += f'{item:<18} {storage.stock(database, place, item):>8} {unit}\n'
        else:
            report = 'Add your first location to begin. Live storage starts empty.'
    except (ValueError, sqlite3.Error) as error:
        report = str(error)
    shared = (f'<input type="hidden" name="token" value="{TOKEN}">'
              f'<input type="hidden" name="mode" value="{mode}">'
              f'<input type="hidden" name="location" value="{escape(location, quote=True)}">')
    item_fields = ''
    for index, item in enumerate(list(catalog.CLOTHING) + list(catalog.SUPPLIES)):
        item_fields += field(item, f'q{index}', '', 'number')
    notice = f'<div class="notice" role="status">{escape(message)}</div>' if message else ''
    filename = ROOT / ('demo_data' if mode == 'demo' else 'data') / 'threads_trends.sqlite3'
    return f'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Threads &amp; Trends | {mode.upper()}</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f4f5f0;color:#213b36;font:15px system-ui,sans-serif}}
header{{background:#183f37;color:white;padding:30px 5%}}h1{{font:38px Georgia,serif;margin:4px 0}}
header p{{color:#c8ddd2;margin:8px 0}}nav{{float:right}}nav a{{color:white;margin-left:16px}}
main{{max-width:1250px;margin:24px auto;padding:0 24px}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}
section{{background:white;border:1px solid #dde3da;border-radius:12px;padding:24px;margin-bottom:22px}}
h2{{font:24px Georgia,serif;margin:0 0 16px}}label{{display:block;color:#476154;font-size:13px;margin-bottom:12px}}
input,select{{display:block;width:100%;border:1px solid #bcc9bf;border-radius:6px;padding:10px;margin-top:5px;background:white;color:#203c32;font:15px system-ui}}
button{{background:#245b48;color:white;border:0;border-radius:6px;padding:11px 16px;cursor:pointer;font:14px system-ui;margin:4px 5px 4px 0}}
button:hover{{background:#173d30}}.row{{display:flex;align-items:end;gap:14px;flex-wrap:wrap}}.row label{{flex:1;min-width:150px}}
.items{{display:grid;grid-template-columns:1fr 1fr;gap:0 16px}}.hint,footer{{color:#647569;font-size:13px;line-height:1.6}}
.badge{{background:#d7e9b8;color:#24432a;border-radius:20px;padding:5px 12px;font-size:12px;font-weight:bold}}
.notice{{background:#e6edce;padding:16px;border-left:4px solid #52744a;margin-bottom:20px}}
pre{{background:#f6f8f3;padding:20px;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.8;font-size:14px;border-radius:8px}}
details{{margin:18px 0}}summary{{cursor:pointer}}footer{{padding-bottom:25px}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}nav{{float:none;margin-bottom:20px}}}}
</style>
<header><nav><a href="/?mode=demo">Demo workspace</a><a href="/?mode=live">Live workspace</a></nav>
<span class="badge">{mode.upper()} · LOCAL WORKSPACE</span><h1>Threads &amp; Trends</h1>
<p>Inventory, daily sales &amp; financial reporting · Team 13 Software Solutions</p></header>
<main>{notice}<section><form method="get" class="row">
<input type="hidden" name="mode" value="{mode}">
<label>Current location<select name="location">{options}</select></label>
{field('Reporting month', 'month', month, 'month')}
<button>Load workspace</button></form>
<details><summary>Add a location</summary><form method="post">{shared}
{field('Location name', 'name')}<button name="action" value="location">Add location</button></form></details>
<p class="hint">{'Separate fictional data for trying the application.' if mode == 'demo' else 'Real records. Review quantities and dates before saving.'}</p></section>
<div class="grid"><div><section><h2>Record activity</h2><form method="post">{shared}
<div class="row">{field('Entry date', 'day', day, 'date')}<label>Entry type<select name="kind">
<option>Purchase</option><option>Sale</option><option>Supply purchase</option><option>Supply usage</option><option>Opening</option>
</select></label></div><div class="items">{item_fields}</div>
<p class="hint">Leave unused rows blank or enter 0. Clothing: individual units. Supply purchases: packages of 500 bags, packages of 100 boxes, or paper cases. Usage/opening: individual bags, boxes, or cases. Opening adds stock without expense.</p>
<button name="action" value="entry">Save entry</button></form></section>
<section><h2>Monthly fixed expenses</h2><p class="hint">Rent $1,500 · Utilities $350 · Labor $18,000 · Equipment $2,500.<br>Total $22,350 per location. Each month can be applied once.</p>
<form method="post">{shared}{field('Expense month', 'month', month, 'month')}
<label><input type="checkbox" name="confirmed" value="yes" required style="width:auto;display:inline"> I checked the selected location and month.</label>
<button name="action" value="fixed">Apply $22,350 fixed expenses</button></form></section></div>
<section><h2>Inventory &amp; reports</h2><form method="get">{shared}
{field('Statement month', 'month', month, 'month')}
<button name="report" value="inventory">Current inventory</button><button name="report" value="income">Location income</button><button name="report" value="company">Company income</button>
<div class="row">{field('Sales range start', 'start', value(form, 'start', month + '-01'), 'date')}
{field('Sales range end', 'end', value(form, 'end', month + '-28'), 'date')}</div>
<button name="report" value="products">Product sales by location</button></form>
<pre>{escape(report)}</pre><p class="hint">Reports show saved entries. Viewing a report does not create monthly charges.</p></section></div>
<footer>Storage: {escape(str(filename))}<br>Close the server and desktop app before backing up the database. Supply usage and monthly charging remain provisional customer decisions.</footer></main></html>'''


class LocalHandler(BaseHTTPRequestHandler):
    def respond(self, status, body):
        encoded = body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(encoded)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Frame-Options', 'DENY')
        self.end_headers()
        self.wfile.write(encoded)

    def handle_page(self, form, save=False):
        mode = value(form, 'mode', 'demo')
        if mode not in ('demo', 'live'):
            self.respond(400, 'Unknown workspace.')
            return
        filename = ROOT / ('demo_data' if mode == 'demo' else 'data') / 'threads_trends.sqlite3'
        database = storage.open_database(filename)
        message = ''
        try:
            if save:
                action = value(form, 'action')
                if action == 'location':
                    storage.add_location(database, value(form, 'name'))
                    form['location'] = [str(storage.locations(database)[-1][0])]
                elif action == 'entry':
                    quantities = {}
                    for index, item in enumerate(list(catalog.CLOTHING) + list(catalog.SUPPLIES)):
                        quantity = value(form, f'q{index}').strip()
                        if quantity and quantity != '0':
                            quantities[item] = quantity
                    entries.record(database, int(value(form, 'location')), value(form, 'day'),
                                   value(form, 'kind'), quantities)
                elif action == 'fixed':
                    if value(form, 'confirmed') != 'yes':
                        raise ValueError('Confirm the location and month before applying expenses.')
                    entries.apply_monthly(database, int(value(form, 'location')), value(form, 'month'))
                else:
                    raise ValueError('Unknown action.')
                # Redirect after saving so browser refresh cannot repeat an entry.
                query = urlencode({'mode': mode, 'location': value(form, 'location'),
                                   'month': value(form, 'month', date.today().strftime('%Y-%m')),
                                   'saved': 'yes'})
                database.close()
                self.send_response(303)
                self.send_header('Location', '/?' + query)
                self.end_headers()
                return
        except (ValueError, sqlite3.Error, OverflowError) as error:
            message = 'Not saved: ' + str(error)
        try:
            if value(form, 'saved') == 'yes' and not message:
                message = 'Saved successfully.'
            self.respond(200, page(database, form, message))
        finally:
            database.close()

    def allowed_host(self):
        return self.headers.get('Host') in (f'127.0.0.1:{PORT}', f'localhost:{PORT}')

    def do_GET(self):
        if not self.allowed_host():
            self.respond(403, 'Use the localhost address.')
        elif self.path.split('?')[0] != '/':
            self.respond(404, 'Page not found.')
        else:
            self.handle_page(parse_qs(self.path.partition('?')[2]))

    def do_POST(self):
        length = int(self.headers.get('Content-Length', '0'))
        if not self.allowed_host() or self.path != '/' or length < 1 or length > 16000:
            self.respond(400, 'Invalid local form request.')
            return
        form = parse_qs(self.rfile.read(length).decode('utf-8'))
        if not secrets.compare_digest(value(form, 'token'), TOKEN):
            self.respond(403, 'Reload the page before submitting.')
            return
        self.handle_page(form, save=True)


if __name__ == '__main__':
    print(f'Threads & Trends: http://{HOST}:{PORT}', flush=True)
    print('Demo is the default workspace. Press Ctrl+C to stop.', flush=True)
    server = HTTPServer((HOST, PORT), LocalHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
