# Threads & Trends - MGIS 350

Team 13 Software Solutions: Bret Kiefer, Sai Bhuyan, Addas Ahmad.

## Local browser interface

Run `python web_app.py`, then visit http://127.0.0.1:8000 in your browser.
The default page uses separate demo storage. Click Live workspace for real records.
Run `python demo_setup.py` first if you want the supplied fictional example data.
The browser interface shares all entry/report rules and storage with the desktop
interface, and uses only the Python standard library. HTTP request handling,
HTML/CSS, and form security extend beyond the professor's Tkinter examples;
the original course-style desktop interface remains available. Keep this server
local, and stop it with Ctrl+C before backing up storage. Use only one interface
at a time. Nothing is published to the internet.

## Setup and run (Windows PowerShell)

Install Python 3.10 or later from python.org with Tcl/Tk and the Python launcher.
The application uses only the standard library; no pip installation is needed.

```powershell
Set-Location 'C:\Users\Bret\OneDrive\Documents\MGIS 350 Project'
py -3 app.py
```

If your installation uses `python` instead of `py -3`, substitute `python` in all
commands. Check Tkinter with `py -3 -m tkinter` if the window does not open.

Live storage is automatically created at `data/threads_trends.sqlite3`, relative
to app.py, regardless of the terminal's current folder. Existing records are
preserved. No initial locations or stock are invented. The window displays the
mode and absolute storage path. Close the application before copying the database
for backup or restoration. See MANUAL.md and the PDF manual for all workflows.

## Safe demonstration

```powershell
py -3 demo_setup.py
py -3 app.py --demo
```

This uses only `demo_data/threads_trends.sqlite3`. Existing demo data is preserved.
Choose October 2026 to view the supplied example. Central begins with 7 T-Shirts,
$54 revenue, $80 clothing purchases, and -$22,376 net income after fixed expenses.
The second fictional demo location has opening stock, without a purchase expense.
To restart a demonstration, close the app and rename the entire demo_data folder
to a backup name before rerunning demo_setup.py. Never reset live storage for a demo.

## Verification

```powershell
py -3 verify.py
```

Checks use temporary databases and leave live/demo records unchanged. Coverage:
purchases, sales, supplies, overselling with multiple lines, rollback on storage
failure, separate locations, opening stock, month/date boundaries, company sums,
read-only reports, persistence, duplicate charges, dates, and quantities.

For a repeatable interface check, launch demo mode, select Central, view inventory,
set month to 2026-10, and view location income. Attempt a sale of 8 T-Shirts with
date 2026-10-03. It must show an error and still show 7 in stock. Company income
includes Central plus East. Product range 2026-10-01 to 2026-10-31 shows 3 T-Shirts
at Central. Exit/reopen to verify the screen shows the same saved records.

## Files and course techniques

`app.py` uses Tkinter Label, Entry, Button, Radiobutton, Listbox, Frame, Scrollbar,
callbacks, and global values following the provided examples. Functions, loops,
conditionals, f-strings, exception handling, and imported modules follow the notes.
`entries.py`, `storage.py`, and `reports.py` align with the upcoming Report 2
responsibilities, without attributing generated work to teammates.

Beyond-notes techniques are kept small: dictionaries/lists hold catalogs and entry
lines; pathlib locates files; datetime validates dates; sqlite3 stores records.
Parameterized SQL separates values from SQL commands. Transactions commit all
lines together or roll back all lines. The monthly table's composite primary key
prevents duplicate expenses. Money is stored/calculated in integer cents, extending
ordinary class integer arithmetic without floating-point rounding. Text is used
for scrollable report output. TemporaryDirectory and assert support verification.
No frameworks, inheritance hierarchy, ORM, or third-party application dependency.

Clothing purchases are expensed on their purchase date, per assignment; statements
do not substitute cost of goods sold. Reports do not write financial records.
Fixed charges are explicit and uncharged locations are identified on statements.

See ASSUMPTIONS.md for unresolved decisions and limitations, DEMO_OUTLINE.md for
the 10-15 minute presentation, and MANUAL.md for the editable manual source.
The PDF can be rebuilt with `py -3 build_manual.py` after installing the optional
documentation-only package: `py -3 -m pip install reportlab`. PDF reading/rendering
tools used for development are not application dependencies.
