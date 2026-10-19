# Remaining customer decisions

These defaults allow implementation; they are not customer-approved answers.

1. Initial location names and starting clothing/supply balances remain unknown.
   Live storage starts empty. Opening entries add explicitly entered stock without
   purchase expenses. Enter each starting balance once; repeated entries add again.
2. Supply usage is manual, independent of clothing sales. Bags and boxes are
   consumed as individual units; receipt paper is counted in whole cases until
   rolls per case and finer usage units are confirmed.
3. Fixed expenses are applied explicitly per location/month, once only. Confirm
   automatic timing, opening/closing location months, and any prorating policy.
   Statements warn about locations with no fixed charge in the selected month.
4. Product reports use a selectable inclusive date range. Confirm the customer's
   preferred default reporting period.

Additional implementation choices: transactions may use any valid calendar date,
including future or backdated dates. Stock is current stock across all entries,
not reconstructed historical stock. Thus backdating does not enforce a historical
daily stock balance. Confirm whether historical stock controls are needed.
Daily sales are incremental entries: multiple saves on one date add together,
rather than replacing that day's totals. Weekly purchases have no weekday lock.
No sales tax, returns, discounts, payroll calculation, or transaction correction
workflow is included. Assigned prices and fixed expenses are in catalog.py; changes
apply to future entries only, since saved entries retain their original amounts.
Each submitted quantity is limited to 1,000,000 units/packages for practical input
validation. Opening entries are additive and must not be used as corrections.

Report 2 remains the latest recorded progress status. Needs assessment and proposal
are completed according to that report. Modules follow upcoming responsibilities:
Bret - entries.py; Sai - storage.py; Addas - reports.py. Generated implementation
does not establish individual teammate contributions, customer approval, or course
submission. Existing report documents are preserved.
