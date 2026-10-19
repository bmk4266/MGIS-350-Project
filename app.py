# Libraries, global values, functions, then main program, as in class notes.
from tkinter import *
from tkinter import messagebox
from datetime import date
from pathlib import Path
import sqlite3
import sys
import catalog
import entries
import storage
import reports

ROOT = Path(__file__).resolve().parent
database = None
location_rows = []


def selected_location():
    selection = lst_locations.curselection()
    if not selection:
        raise ValueError('Select a location first.')
    return location_rows[selection[0]][0]


def refresh_locations():
    global location_rows
    location_rows = storage.locations(database)
    lst_locations.delete(0, END)
    for place, name in location_rows:
        lst_locations.insert(END, name)
    if location_rows:
        lst_locations.selection_set(0)


def show(text):
    txt_output.config(state=NORMAL)
    txt_output.delete('1.0', END)
    txt_output.insert(END, text)
    txt_output.config(state=DISABLED)


def cmd_add_location():
    try:
        storage.add_location(database, ent_location.get())
        refresh_locations()
        ent_location.delete(0, END)
        lbl_status['text'] = 'Location added. Select it before entering activity.'
    except (ValueError, sqlite3.Error) as error:
        messagebox.showerror('Location not saved', str(error))


def cmd_save():
    try:
        location = selected_location()
        kind = var_action.get()
        quantities = {}
        for item in quantity_fields:
            value = quantity_fields[item].get().strip()
            if value and value != '0':
                quantities[item] = value
        # All filled item lines form one entry: any invalid line rejects all.
        entries.record(database, location, ent_day.get().strip(), kind, quantities)
        for field in quantity_fields.values():
            field.delete(0, END)
        lbl_status['text'] = 'Saved. Quantities cleared to prevent an accidental repeat.'
        cmd_stock()
    except (ValueError, sqlite3.Error, OverflowError) as error:
        messagebox.showerror('Entry not saved', str(error))


def cmd_stock():
    try:
        location = selected_location()
        text = 'CURRENT INVENTORY (all recorded dates)\n\n'
        for place, name in location_rows:
            if place == location:
                text += name + '\n\n'
        for item in quantity_fields:
            units = 'units'
            if item == 'Receipt paper':
                units = 'cases'
            text += f'{item}: {storage.stock(database, location, item)} {units}\n'
        show(text)
    except ValueError as error:
        messagebox.showerror('Inventory', str(error))


def cmd_fixed():
    try:
        location = selected_location()
        month = ent_month.get().strip()
        entries.check_month(month)
        if messagebox.askyesno('Apply monthly expenses',
                f'Apply {catalog.money(sum(catalog.FIXED.values()))} for {month}\n'
                f'to {lst_locations.get(lst_locations.curselection()[0])}?'):
            entries.apply_monthly(database, location, month)
            lbl_status['text'] = 'Monthly fixed expenses saved.'
            cmd_income()
    except (ValueError, sqlite3.Error) as error:
        messagebox.showerror('Monthly expenses not saved', str(error))


def cmd_income(company=False):
    try:
        location = None
        if not company:
            location = selected_location()
        show(reports.income_text(database, ent_month.get().strip(), location))
    except (ValueError, sqlite3.Error) as error:
        messagebox.showerror('Income statement', str(error))


def cmd_company():
    cmd_income(True)


def cmd_products():
    try:
        show(reports.product_text(database, ent_start.get().strip(), ent_end.get().strip()))
    except (ValueError, sqlite3.Error) as error:
        messagebox.showerror('Product report', str(error))


def cmd_close():
    database.close()
    root_window.destroy()


if __name__ == '__main__':
    if sys.argv[1:] not in ([], ['--demo']):
        print('Usage: python app.py [--demo]')
        sys.exit(1)
    mode = 'LIVE'
    filename = ROOT / 'data' / 'threads_trends.sqlite3'
    if '--demo' in sys.argv:
        mode = 'DEMO'
        filename = ROOT / 'demo_data' / 'threads_trends.sqlite3'
    root_window = Tk()
    root_window.title(f'Threads & Trends - {mode}')
    root_window.geometry('1120x800')
    root_window.minsize(1000, 720)
    try:
        database = storage.open_database(filename)
    except (OSError, sqlite3.Error) as error:
        messagebox.showerror('Storage unavailable', str(error))
        root_window.destroy()
        sys.exit(1)
    root_window.protocol('WM_DELETE_WINDOW', cmd_close)
    root_window.columnconfigure(1, weight=1)
    root_window.rowconfigure(1, weight=1)
    Label(root_window, text=f'{mode} storage: {filename}', anchor=W).grid(
        row=0, column=0, columnspan=2, sticky=EW, padx=10, pady=8)
    controls = Frame(root_window, padx=10, pady=5)
    controls.grid(row=1, column=0, sticky=NS)
    Label(controls, text='1. Select or add a location').grid(row=0, column=0, columnspan=2, sticky=W)
    lst_locations = Listbox(controls, height=4, width=34, exportselection=False)
    lst_locations.grid(row=1, column=0, columnspan=2, sticky=EW)
    ent_location = Entry(controls)
    ent_location.grid(row=2, column=0, sticky=EW)
    Button(controls, text='Add location', command=cmd_add_location).grid(row=2, column=1)
    Label(controls, text='2. Entry date (YYYY-MM-DD)').grid(row=3, column=0, sticky=W)
    ent_day = Entry(controls, width=14)
    ent_day.insert(0, date.today().isoformat())
    ent_day.grid(row=3, column=1)
    var_action = StringVar(value='Purchase')
    row = 4
    for action in ('Purchase', 'Sale', 'Supply purchase', 'Supply usage', 'Opening'):
        Radiobutton(controls, text=action, variable=var_action, value=action).grid(
            row=row, column=0, columnspan=2, sticky=W)
        row += 1
    Label(controls, text='3. Quantities (blank/0 = skip)').grid(row=9, column=0, columnspan=2, sticky=W)
    quantity_fields = {}
    row = 10
    for item in list(catalog.CLOTHING) + list(catalog.SUPPLIES):
        Label(controls, text=item).grid(row=row, column=0, sticky=W)
        field = Entry(controls, width=14)
        field.grid(row=row, column=1)
        quantity_fields[item] = field
        row += 1
    Label(controls, text='Supply purchase: packages/cases\nUsage/opening: bags, boxes, cases\nOpening adds stock; no expense.', justify=LEFT).grid(
        row=18, column=0, columnspan=2, sticky=W, pady=5)
    Button(controls, text='Save entry', command=cmd_save).grid(row=19, column=0, sticky=EW)
    Button(controls, text='View inventory', command=cmd_stock).grid(row=19, column=1)
    Label(controls, text='Month (YYYY-MM)').grid(row=20, column=0, sticky=W, pady=5)
    ent_month = Entry(controls, width=14)
    ent_month.insert(0, date.today().strftime('%Y-%m'))
    ent_month.grid(row=20, column=1)
    Button(controls, text='Apply monthly fixed expenses', command=cmd_fixed).grid(row=21, column=0, columnspan=2, sticky=EW)
    Button(controls, text='Location income', command=cmd_income).grid(row=22, column=0, sticky=EW)
    Button(controls, text='Company income', command=cmd_company).grid(row=22, column=1)
    Label(controls, text='Sales range start / end').grid(row=23, column=0, columnspan=2, sticky=W)
    ent_start = Entry(controls, width=14)
    ent_start.insert(0, date.today().strftime('%Y-%m-01'))
    ent_start.grid(row=24, column=0)
    ent_end = Entry(controls, width=14)
    ent_end.insert(0, date.today().isoformat())
    ent_end.grid(row=24, column=1)
    Button(controls, text='Product sales by location', command=cmd_products).grid(row=25, column=0, columnspan=2, sticky=EW)
    output_frame = Frame(root_window)
    output_frame.grid(row=1, column=1, sticky=NSEW, padx=10, pady=5)
    scrollbar = Scrollbar(output_frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    txt_output = Text(output_frame, width=65, wrap=WORD, font=('Consolas', 11), yscrollcommand=scrollbar.set)
    txt_output.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=txt_output.yview)
    lbl_status = Label(root_window, text='Ready. Blank locations mean no locations have been added.', anchor=W)
    lbl_status.grid(row=2, column=0, columnspan=2, sticky=EW, padx=10, pady=8)
    refresh_locations()
    show('Threads & Trends\nTeam 13 Software Solutions\n\nSelect or add a location to begin.\n\nPurchases: clothing units at wholesale prices.\nSales: daily clothing quantities at sale prices.\nSupply purchases: whole packages or cases.\nSupply usage: individual bags, boxes, or cases.\nOpening: additional starting stock without expense.\n\nReports never create financial entries.\nApply fixed expenses explicitly for each month/location.\n\nAll filled lines are saved together or rejected together.\nReview entries carefully; corrections are outside this version.')
    root_window.mainloop()
