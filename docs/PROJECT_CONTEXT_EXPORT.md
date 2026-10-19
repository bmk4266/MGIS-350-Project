# MGIS 350 Team 13 — Threads & Trends Project Context

Compiled October 19, 2026 from the referenced ChatGPT conversation, the attached needs-assessment proposal and 2×2 template, Team 13 Reports 1 and 2, and the current project files.

## 1. Project identity

- Course: MGIS 350 — Developing Business Applications
- Team: Team 13 Software Solutions
- Team members: Bret Kiefer, Sai Bhuyan, and Addas Ahmad
- Client: Threads & Trends, a fictional clothing retailer
- Project goal: Build a simple, reliable Python application for inventory, sales revenue, expenses, and management reporting across multiple store locations.
- Team mission from the proposal: Provide simple, reliable software that helps businesses maintain accurate records and make informed decisions.
- Stated values: Accuracy, ease of use, and clear communication.

## 2. Source and confidence labels

This export uses the following labels to avoid mixing requirements with assumptions:

- **Confirmed requirement** — stated in the needs-assessment proposal as confirmed by the customer or required by the assignment.
- **Team decision / implementation choice** — selected by Team 13 or used in the current implementation, but not necessarily required by the customer.
- **Unresolved** — still needs customer or instructor confirmation.
- **Historical status** — what Report 1 or Report 2 said at the time; it is not necessarily the current development status.

## 3. Assignment overview and deliverables

### Confirmed requirements

- Act as a software company creating a custom business application for Threads & Trends.
- Build the application in Python.
- Run it locally on the customer’s single laptop.
- Keep entered data after the program closes by using a local file or database.
- Support multiple store locations with separate inventory and financial records.
- Allow new locations to be added.
- Manage clothing inventory, clothing purchases, daily sales totals, supplies, and fixed expenses.
- Display reports on screen.
- Provide regular 2×2 project status reports.
- Deliver the complete Python application and its required data storage.
- Deliver a PDF setup/user manual that explains setup, use, any additional libraries, and how stored data is created and maintained.
- Give a final demonstration showing daily entries, inventory changes, expense and revenue calculations, individual-location reports, and company-wide reports.

### Optional or out-of-scope items

- Exporting reports is optional and is not required.
- Transaction correction features are outside the required scope because the customer confirmed the assignment assumption that staff do not make entry mistakes.

## 4. Confirmed customer requirements

### Locations and data separation

- Maintain separate inventory for each location.
- Maintain separate revenue and expense records for each location.
- Allow users to add new store locations.
- Support reports for one location and for the entire company.
- The customer hopes to open another location within one year.

### Clothing purchases and inventory

- Clothing purchases are expected weekly.
- A clothing purchase increases the selected location’s inventory.
- A clothing purchase increases expenses.
- Store the purchase date, location, item, quantity, and calculated purchase cost.

### Daily sales

- Staff enter daily totals by clothing item, not individual customer transactions.
- A sale decreases inventory at the selected location.
- A sale increases sales revenue using the assigned sale price.
- Store the sale date, location, item, quantity, and calculated revenue.
- Do not allow a recorded sale to exceed available inventory.

### Supplies

- Track shopping bags, gift boxes, and receipt paper as inventory.
- Show the quantity of each supply on hand.
- Include supply purchase expenses in financial reporting.

### Fixed monthly expenses

- Include rent, utilities, labor, and equipment leases for each location.
- Include fixed expenses in monthly income statements.

### Data persistence

- Save all entered data locally.
- Preserve records after the application closes and reopens.
- The application is intended for one laptop, not a networked multi-user environment.

### Reports

#### Monthly income statement

The user must be able to select a month and either one location or the whole company. The report must show:

- Sales revenue
- Clothing purchase expenses
- Supply expenses
- Fixed expenses
- Total expenses
- Net income

Formula: `Net income = Sales revenue - Total expenses`.

#### Product sales report

- Show the quantity of each clothing item sold.
- Break results out by location.
- Help the customer identify sales trends.

## 5. Data and pricing tables

### Clothing catalog

| Item | Wholesale cost | Sale price |
|---|---:|---:|
| T-Shirt | $8.00 | $18.00 |
| Jeans | $22.00 | $48.00 |
| Hoodie | $18.00 | $40.00 |
| Jacket | $35.00 | $75.00 |
| Dress | $28.00 | $60.00 |

### Supply catalog

| Supply | Purchase price | Package quantity / current unit treatment |
|---|---:|---:|
| Shopping bags | $25.00 | 500 bags per package |
| Gift boxes | $40.00 | 100 boxes per package |
| Receipt paper | $18.00 | 1 case; rolls per case are unresolved |

### Fixed monthly expenses per location

| Expense | Monthly amount |
|---|---:|
| Rent | $1,500.00 |
| Utilities | $350.00 |
| Labor | $18,000.00 |
| Equipment leases | $2,500.00 |
| **Total** | **$22,350.00** |

## 6. Needs-assessment findings

The needs assessment established that accurate inventory updates and financial calculations are the customer’s highest priorities. Daily entry should stay simple: employees enter item totals for the day instead of recording each customer purchase. Inventory and financial activity must stay associated with a location, while management reports must also support a company-wide view.

The proposed workflow is:

1. Add or select a store location.
2. Record starting inventory when it becomes known.
3. Record clothing and supply purchases.
4. Enter daily clothing quantities sold.
5. Prevent any entry that would make stock negative.
6. Account for fixed monthly expenses.
7. Display monthly income statements and product-sales reports.
8. Close and reopen the program without losing data.

## 7. Unresolved customer questions

These items were explicitly left unresolved in the proposal and Report 2:

1. What are the initial store locations?
2. What is the starting clothing inventory for each location?
3. What is the starting supply inventory for each location?
4. How should supply usage be entered or calculated?
5. How many rolls are in a case of receipt paper, and should paper usage be tracked by roll or case?
6. Should fixed monthly expenses be created automatically, entered manually, or calculated only while reports are generated?
7. If fixed expenses are automatic, when should they be applied and should partial months be prorated?
8. What date-range behavior should the product-sales report use by default?
9. Is historical, date-specific inventory validation required for backdated entries, or is checking current stock sufficient?

These questions should not be silently converted into permanent business rules.

## 8. Provisional team decisions in the current implementation

The following choices make the current application usable but are not recorded as customer-approved answers:

- Live storage starts with no invented locations or inventory.
- An explicit opening-inventory entry adds starting stock without recording a purchase expense.
- Supply usage is entered manually and is independent of clothing sales.
- Bags and boxes are consumed as individual units.
- Receipt paper is temporarily counted in whole cases.
- Fixed monthly expenses are applied explicitly for each location and month.
- Applying fixed expenses twice for the same location/month is blocked.
- Reports warn when a location has no fixed charge for the selected month.
- Product sales use a user-selected inclusive start and end date.
- Valid future and backdated dates are accepted.
- Inventory validation checks current recorded stock, not reconstructed historical stock on the entered date.
- Multiple sales entries on the same date add together; they do not replace earlier totals.
- Clothing purchase costs are expensed on the purchase date rather than treated as cost of goods sold when items sell.
- Prices are centralized and stored in integer cents to avoid floating-point rounding errors.
- No sales tax, returns, discounts, payroll calculation, user login, or correction workflow is included in the first version.

## 9. Report 1 status context

**Historical status — Report 1**

Completed tasks:

- Reviewed the project requirements — Bret Kiefer
- Prepared questions for the customer meeting — Sai Bhuyan
- Discussed team roles and workflow — Addas Ahmad

Upcoming tasks at that time:

- Attend the customer meeting and record answers — Bret Kiefer
- Draft the team proposal — Sai Bhuyan
- Plan the Python program and data storage — Addas Ahmad

Decisions/action items at that time:

- Choose the company name and mission statement.
- Confirm team roles and data storage.

Issues/concerns at that time:

- Some project details still needed customer clarification.
- Team schedules needed coordination.

The final Report 1 copy was simplified to reduce repeated wording and unnecessary bullet points. Team members were corrected to Bret Kiefer, Sai Bhuyan, and Addas Ahmad.

## 10. Report 2 status context

**Historical status — Report 2**

Completed tasks:

- Completed the needs assessment and confirmed project requirements — Bret Kiefer
- Completed the customer proposal and project scope — Sai Bhuyan
- Reviewed reports, inventory tracking, and data storage needs — Addas Ahmad

Upcoming tasks at that time:

- Build inventory and sales entry functions in Python — Bret Kiefer
- Set up data storage for locations, inventory, revenue, and expenses — Sai Bhuyan
- Create the income statement and product sales reports — Addas Ahmad

Decision/action item:

- Confirm starting inventory, supply usage, fixed-expense handling, and the product-sales report date range.

Issue/concern:

- Remaining customer details needed confirmation before all application logic could be finalized.

The module responsibility labels used in the current project follow this plan, but generated code does not prove that a named teammate personally completed that work.

## 11. Current implementation status as of this export

This section reflects the files now present in the project folder, not the older Report 2 milestone.

The project currently includes:

- A local Tkinter desktop application in `app.py`.
- An optional local browser interface in `web_app.py`.
- SQLite persistence in `data/threads_trends.sqlite3`.
- Location creation and selection.
- Opening inventory, clothing purchases, daily sales, supply purchases, and manual supply usage.
- Validation for dates, required values, positive whole-number quantities, known locations/items, and insufficient inventory.
- Transactional all-or-nothing entry saving.
- Explicit monthly fixed-expense application with duplicate prevention.
- Monthly location and company income statements.
- Product-sales reporting by inclusive date range and location.
- A verification suite in `verify.py` using temporary databases.
- Separate fictional demonstration storage and setup.
- `README.md`, `docs/MANUAL.md`, a generated PDF manual, assumptions, and a presentation outline.

Current SQLite model:

- `locations(id, name)` stores unique location names.
- `activity(id, location, day, kind, item, quantity, cents)` stores inventory and financial activity.
- `monthly(location, month)` records which location/month combinations received fixed expenses and prevents duplicates.

This compact activity-ledger design replaces the larger preliminary list of possible tables while still supporting the required workflows.

## 12. Recommended architecture

The original recommendation remains appropriate: use a small standard-library Python application with clear separation of responsibilities.

### Recommended components

- `app.py` — Tkinter user interface and event handlers
- `catalog.py` — clothing prices, supply package data, and fixed-expense values
- `storage.py` — SQLite connection, schema, location operations, and stock queries
- `entries.py` — validation and transactional purchase/sale/supply/monthly-expense entry rules
- `reports.py` — read-only income-statement and product-sales calculations
- `verify.py` — automated workflow and rule checks
- `README.md` — setup and developer overview
- `docs/MANUAL.md` and PDF — end-user setup, use, storage, backup, and limitations
- `data/` — live SQLite database
- `demo_data/` — separate fictional demonstration database

### Architecture principles

- Prefer Python standard-library tools.
- Keep code understandable for students learning Python.
- Use SQLite for persistence and Tkinter for the required desktop interface.
- Keep business constants centralized and easy to change.
- Validate a complete multi-line entry before writing any part of it.
- Use database transactions so an entry fully succeeds or fully rolls back.
- Keep reports read-only.
- Keep live and demo data separate.
- Record unresolved requirements in documentation and configurable logic instead of inventing hidden rules.

## 13. Recommended implementation and validation plan

The most important end-to-end milestone is:

`Open app → add location → add opening stock or purchase inventory → record sales → view reports → close/reopen → verify records remain.`

Suggested sequence:

1. Confirm requirements and record unresolved customer questions.
2. Centralize product, supply, and fixed-expense values.
3. Create the SQLite schema automatically without deleting existing data.
4. Implement location creation and selection.
5. Implement opening inventory and purchases.
6. Implement daily sales with overselling prevention.
7. Implement supply purchases and provisional manual usage.
8. Implement explicit monthly fixed expenses with duplicate prevention.
9. Implement location and company income statements.
10. Implement product-sales reporting by location and date range.
11. Add clear validation and user-facing error messages.
12. Test persistence, separate locations, report totals, rollback behavior, boundaries, and duplicate protection.
13. Prepare a separate fictional demo database.
14. Finish the setup/user manual and final presentation.
15. Ask the customer/instructor to resolve remaining business-rule questions before declaring those rules final.

## 14. Suggested demonstration plan

The current presentation outline targets about 12 minutes:

- Bret: explain the purpose and interface; show clothing inventory, purchase, sale, and overselling rejection; discuss entry logic.
- Sai: show separate location records, adding a location, supply purchase/usage, close/reopen persistence, database storage, and backups.
- Addas: show location and company income statements, duplicate fixed-expense protection, product-sales date ranges, report calculations, and unresolved decisions.

All team members should understand and be able to explain the full workflow, even when one module is assigned to one person.

## 15. Codex starter prompt from the referenced conversation

The following preserves the starter prompt that was drafted before the current implementation existed. Because the project has now been built substantially, a new Codex session should first inspect the existing files and avoid replacing working features.

```text
I need you to help me build a college group project for MGIS-350 Developing Business Applications at RIT.

PROJECT TEAM
Team 13:
- Bret Kiefer
- Sai Bhuyan
- Addas Ahmad

PROJECT
We are acting as a software company creating an inventory and financial management application for a fictional clothing retailer called Threads & Trends.

IMPORTANT
This is a student project. Keep the code understandable for students who are still learning Python. Do not make the architecture unnecessarily complex. Use clear variable names, comments where useful, and simple functions/classes.

The program needs to run locally on a single Windows laptop with Python.

Prefer Python standard-library tools whenever possible. I would like to use:
- tkinter for the GUI
- sqlite3 for persistent data storage
- datetime for dates

Avoid third-party packages unless they are clearly necessary.

CORE REQUIREMENTS

1. STORE LOCATIONS
The company has multiple store locations.

The program must:
- maintain separate inventory for each location
- maintain separate financial data for each location
- allow new store locations to be added
- also allow company-wide reports across every location

2. PRODUCTS

Clothing products:

T-Shirt
Wholesale cost: $8
Sale price: $18

Jeans
Wholesale cost: $22
Sale price: $48

Hoodie
Wholesale cost: $18
Sale price: $40

Jacket
Wholesale cost: $35
Sale price: $75

Dress
Wholesale cost: $28
Sale price: $60

3. SUPPLIES

Also track these supplies as inventory:

Shopping Bags
$25 per package of 500

Gift Boxes
$40 per package of 100

Receipt Paper
$18 per case

4. INVENTORY PURCHASES

Stores purchase clothing to restock inventory.

When clothing is purchased:
- inventory quantity increases
- expenses increase
- save the date
- save the location
- save the product
- save quantity purchased
- calculate and save the purchase cost

5. DAILY SALES

The customer does NOT want individual customer transactions.

Employees enter daily sales totals for each clothing item.

For example:

Date: 10/19/2026
Location: Rochester
T-Shirts Sold: 6
Jeans Sold: 3
Hoodies Sold: 4
Jackets Sold: 1
Dresses Sold: 2

When sales are recorded:
- decrease inventory
- increase sales revenue
- calculate revenue using the predetermined sale price
- store the sale date and location

IMPORTANT:
Do not allow the user to record a sale quantity greater than the inventory currently available.

6. SUPPLY INVENTORY

Shopping bags, gift boxes, and receipt paper must also be tracked.

Create the data model so supply purchases and supply quantities can be recorded.

The exact method for recording supply usage has not yet been confirmed by the customer, so structure the program so supply usage can easily be added later.

Do not invent complicated supply-consumption rules yet.

7. FIXED MONTHLY EXPENSES

Each store has these fixed monthly expenses:

Rent: $1,500
Utilities: $350
Labor: $18,000
Equipment leases: $2,500

Design the system so these values are centralized and easy to change.

The customer has not yet confirmed whether fixed monthly expenses should automatically be generated each month or calculated only when reports are generated.

For now, design this as a configurable behavior instead of hard-coding an irreversible assumption.

8. DATA STORAGE

All data must remain after the program closes.

Use SQLite.

Create the database automatically if it does not exist.

Possible tables could include:

locations
products
inventory
inventory_purchases
sales
supplies
supply_inventory
supply_purchases

Add other tables only if they clearly improve the application.

9. REPORTS

MONTHLY INCOME STATEMENT

The user should:
- choose a month
- choose either one store or the whole company

Display:

Sales Revenue
Clothing Purchase Expenses
Supply Expenses
Fixed Expenses
Total Expenses
Net Income

Net Income =
Sales Revenue - Total Expenses

PRODUCT SALES REPORT

Show how many of each clothing item were sold.

Allow reporting by location.

Structure the code so a date range can be added easily because the exact date-range requirement has not yet been confirmed.

Reports only need to display on screen. Exporting reports is optional.

10. GUI

Create a simple professional tkinter GUI.

Suggested main navigation:

Dashboard
Locations
Inventory
Purchases
Daily Sales
Supplies
Reports

It does not need to look like a commercial SaaS product.

Prioritize:
- clarity
- ease of use
- preventing invalid data
- understandable Python code

11. VALIDATION

Include basic error checking such as:

- quantities must be numbers
- quantities cannot be negative
- required fields cannot be blank
- users cannot sell more inventory than exists
- location must exist
- dates should be valid

Show understandable GUI error messages.

12. PROJECT DELIVERABLES

Eventually we need:

- Complete Python application
- Persistent data storage
- PDF setup/user manual
- Final class demonstration

For now create a Markdown manual that we can later convert into the required PDF.

CREATE THIS PROJECT STRUCTURE

threads_and_trends/
    app.py
    database.py
    models.py
    inventory.py
    sales.py
    reports.py
    config.py
    manual.md
    README.md
    data/
        threads_and_trends.db

You may modify this structure if there is a clear reason, but keep the project relatively small.

IMPORTANT DEVELOPMENT INSTRUCTIONS

Do NOT try to build everything at once.

First:

1. Review these requirements.
2. Create a short implementation plan.
3. Identify anything that is still ambiguous.
4. Create the folder/file structure.
5. Build the SQLite database schema.
6. Build a minimal working tkinter application.
7. Implement adding/viewing store locations.
8. Implement inventory.
9. Implement inventory purchases.
10. Implement daily sales.
11. Implement reports.
12. Add validation.
13. Test the complete workflow.
14. Write README.md and manual.md.

Do not silently make major business-rule assumptions.

For unresolved customer questions, add clear TODO comments or configurable options.

Before doing major architecture changes, explain why.

START NOW

Begin by:
- inspecting the current repository
- giving me your implementation plan
- showing me the proposed SQLite schema
- creating the initial project structure
- then implementing the database initialization and basic GUI shell

After that, tell me what was created and what you recommend building next.
```

## 16. Updated continuation prompt for the current project

This shorter prompt is more appropriate now that the project already contains a working implementation:

```text
Continue the existing MGIS 350 Team 13 Threads & Trends project in this folder. Team members are Bret Kiefer, Sai Bhuyan, and Addas Ahmad.

First read docs/PROJECT_CONTEXT_EXPORT.md, README.md, docs/ASSUMPTIONS.md, docs/MANUAL.md, and the existing Python files. Do not replace the working architecture or erase any live/demo data. Treat confirmed requirements, provisional implementation choices, and unresolved customer questions as separate categories.

Inspect the current implementation and verification results before changing code. Keep the project understandable for students, prefer the Python standard library, preserve SQLite data, and make only focused changes. Do not claim that generated work was personally completed by a specific teammate.

Then:
1. Summarize what is already complete.
2. Identify any gaps between confirmed requirements and the implementation.
3. Identify unresolved questions that need customer/instructor input.
4. Recommend the safest next milestone.
5. Implement only the next requested change, verify it, and update the manual if behavior changes.
```

## 17. Source files represented in this export

- Referenced ChatGPT conversation: “Write Report 1”
- Attached `Team_13_Needs_Assessment_Proposal(1).docx`
- Attached `2x2 Template(2).docx`
- `docs/Team_13_Report_1_Simplified.docx`
- `docs/Team_13_Report_2.docx`
- `docs/Team_13_Report_3.docx`
- Current `README.md`
- Current `docs/ASSUMPTIONS.md`
- Current `docs/MANUAL.md`
- Current `docs/DEMO_OUTLINE.md`
- Current application modules and data model
