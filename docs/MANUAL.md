# Threads & Trends
## Setup and user manual

Team 13 Software Solutions | MGIS 350
Bret Kiefer, Sai Bhuyan, Addas Ahmad

## 1. Install and start

Use Python 3.10 or later with Tcl/Tk (Tkinter) and the Python launcher installed.
The application needs no additional packages. Keep app.py, catalog.py, entries.py,
storage.py, and reports.py in the same folder. Open PowerShell in that folder and
run: py -3 app.py. If using a python command installation, run python app.py.
The title says LIVE and the top line shows the full database path. If Tkinter
is missing, repair Python's installation to include Tcl/Tk. A storage error is
displayed if the folder/database is inaccessible; correct permissions or restore
a known good backup before retrying. Do not replace an unreadable database with
an empty one without first preserving the original.

## 2. Storage, maintenance, and backups

The program creates data/threads_trends.sqlite3 beside app.py automatically.
CREATE TABLE IF NOT EXISTS preserves existing data. All locations and dated
activity share this database, with a location ID on each record. Each accepted
entry is committed immediately; rejected entries roll back. Closing the window
closes the connection. No Save All action is needed. Reports do not change data.

Close every application window before backing up. Copy the entire data folder
to a dated backup folder or external drive. Back up before major data entry and
keep multiple dated copies. To restore, close the app, preserve the current data
folder under another name, and copy the backup data folder beside app.py. Reopen
and check locations, stock, and reports. Restoring replaces later entries with
the backed-up state. Never copy demo storage over live storage. Keep databases
private and protect the laptop/account and backups; no login system is included.
Use one running window on the one laptop; do not edit or synchronize an open
database from another device. Pause cloud syncing while using the database if
the project folder is inside OneDrive; closed database backups may be synced.

## 3. Add and select locations

Enter a name beside Add location and click the button. Names must be nonblank,
unique ignoring case, and at most 80 characters. Select the location in the list
before every entry or location report. New locations have zero inventory and no
financial entries. No actual customer location names are supplied or invented.

## 4. Opening inventory and weekly purchases

Select a location and enter a real date as YYYY-MM-DD. Choose Opening, fill in
the known starting quantities, and click Save entry. Opening adds stock without
creating a purchase expense. It does not replace balances; enter starting stock
once only. Opening supplies use individual bags, boxes, and whole paper cases.

For weekly purchases choose Purchase, enter clothing quantities, and save. You
may enter several clothing items together. Prices are assigned automatically:
T-Shirt $8 cost/$18 sale; Jeans $22/$48; Hoodie $18/$40; Jacket $35/$75; Dress
$28/$60. A purchase increases stock and expenses on the entered date. No weekly
schedule restriction is imposed. View inventory shows current stock for the
selected location across all recorded dates.

## 5. Enter daily sales

Choose Sale, enter the sales date and total units sold for each clothing item,
then Save entry. Enter daily quantities, not customer transactions or dollar
amounts. Revenue uses the assigned sale prices and stock decreases. All filled
lines form one entry. If any line exceeds available stock, nothing in that entry
is saved. Quantities clear after success; an error retains them for correction.
Multiple saved sales for the same day add together. Do not resubmit the same
daily totals. Inspect entries before saving: transaction corrections are outside
the first version. Enter blank or 0 to skip a line; other submitted quantities
must be positive whole numbers up to 1,000,000.

## 6. Buy and use supplies

Choose Supply purchase and fill only supply rows. Shopping bags cost $25 for
one package of 500; gift boxes cost $40 for one package of 100; receipt paper
costs $18 for one case. Enter the number of packages/cases purchased, not loose
bags/boxes. Saving increases inventory by package contents and records expense.

Choose Supply usage to reduce stock manually. Enter individual bags or boxes,
or whole receipt-paper cases. Usage has no new expense because the purchase was
already expensed. Usage exceeding stock is rejected in full. Clothing sales do
not automatically consume supplies. Rolls per paper case remain unspecified.

## 7. Apply monthly expenses

Select a location, enter a month as YYYY-MM, and click Apply monthly fixed
expenses. Check the confirmation's location, month, and amount before accepting.
The action saves rent $1,500, utilities $350, labor $18,000, and equipment leases
$2,500: total $22,350. Charges are dated on that month's first day. The same
location/month cannot be charged twice, even after reopening. Other locations
and months are independent. Generating an income statement never applies charges.

## 8. Display reports

For Location income select a location and month. For Company income only the
month is needed. Statements show revenue, clothing purchase expenses, supply
expenses, fixed expenses with detail, and net income. Clothing purchases are
expenses when purchased; unsold stock does not defer their expense. Net income
is revenue minus these expenses. Company figures equal the sum of location
figures for the month. Locations without recorded monthly fixed charges are
listed so incomplete expense entry is visible; the report does not add estimates.

For Product sales by location enter start and end as YYYY-MM-DD. Both dates are
included; start must not follow end. The report shows all clothing items at every
location, including zero sales. Scroll the output area to read long reports.
Reports are displayed on screen. Export is not included in this version.

## 9. Demonstration and checks

Run py -3 verify.py for repeatable checks using temporary databases. Run
py -3 demo_setup.py, then py -3 app.py --demo for safe separate demo storage in
demo_data/threads_trends.sqlite3. The title and path say DEMO. Existing demo
records are preserved, and live storage is untouched. Choose October 2026 and
Central: buying 10 T-Shirts costs $80, selling 3 yields $54, stock is 7, and net
income after one fixed month is -$22,376. Trying to sell 8 more must fail. Close
and reopen to check persistence. See `docs/DEMO_OUTLINE.md` for the presentation plan.

## 10. Defaults, limitations, and editable source

Customer decisions still needed: initial locations/balances, supply usage rules,
paper units, monthly expense automation, and preferred report dates. Current
defaults are provisional: manual usage, paper cases, explicit monthly charges,
and selectable report ranges. Opening stock creates no purchase expense. Valid
backdated/future dates are accepted; inventory checks use current recorded stock,
not historical stock as of the entered date. There is no correction, returns,
tax, discount, user-login, or automatic monthly charging workflow.

`docs/MANUAL.md` is the editable source. To rebuild the PDF, install the optional
documentation package with py -3 -m pip install reportlab and run
py -3 build_manual.py. This package is not needed to run or verify the application.
See `README.md` for the module map and `docs/ASSUMPTIONS.md` for all pending decisions.
