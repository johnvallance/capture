from tkinter import *
import tkinter.ttk as ttk
from tkinter.messagebox import showerror, askquestion
import sqlite3
#import openpyxl
import pandas as pd
from pandas import DataFrame
import csv


conn = sqlite3.connect(r"c:\PYTHON PROGRAMS\CAPTURE\Mydatabase.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS takeon 
                   (acc_id INTEGER PRIMARY KEY AUTOINCREMENT,               
                    month TEXT,
                    year TEXT, 
                    account TEXT,
                    desc TEXT,
                    amount INTEGER,                       
                    recon TEXT)''')

root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 1200
height = 600
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.resizable(0, 0)


# =============== Adding combobox data FROM combo.csv ============================

df = pd.read_excel(r"c:\PYTHON PROGRAMS\CAPTURE\budget.xlsx")
df.drop_duplicates(subset="bud_account", keep='first', inplace=True)
df.pop('bud_desc'), df.pop('bud_amount'),df.pop('bud_recon')
df = df.sort_values("bud_account") #, inplace=True
df.to_csv(r"c:\PYTHON PROGRAMS\CAPTURE\combo.csv", index=False, header=False)
with open(r'C:\PYTHON PROGRAMS\CAPTURE\combo.csv') as inFile:
    combo_list = [line for line in inFile]
#--------------------------------------------------------------------------------------
def space():
    pass
#  ============================== EXIT FUNCTION ============================================================
def goodbye():
    result = askquestion('Python - Update SQLite Data', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()


# ==================== INSERTING DATA INTO DATABASE ===========================
def insert_data(month, year, account, desc, amount, recon):
    account = account.replace('\r', '').replace('\n', '')
    account = ''.join(account.split())
    if account == "Bank":
        recon = "NO"

    cursor.execute("insert into takeon values(NULL,?,?,?,?,?,?)",
                   (month, year, account, desc, amount, recon))
    conn.commit()


# ================================== CLEAR ENTRIES ========================================================
def clear_entries():
    description.delete(0, "end")
    amt.delete(0, "end")
    combo1.delete(0, "end")
    combo2.delete(0, "end")


# ====================== RETRIEVING INPUT FOR WRITING ===========================
def retrieve():
    month = e1.get()
    year = e2.get()
    desc = description.get()
    recon = ""
    amount = amt.get()
    try:  # testing test numeric def
        val = int(amount)
    except ValueError:
        showerror(" NOT NUMERIC")
        return

    account = combo1.get()
    account1 = combo2.get()
    amount = int(amount)
    amount = (amount * -1)

    if not desc.strip() or not account.strip() or not account1.strip() or not month.strip():
        showerror(" BLANK FIELDS")
        return

    insert_data(month, year, account, desc, amount, recon)  # CALLING INSERT DEF

    account = combo2.get()
    amount = abs(amount)
    insert_data(month, year, account, desc, amount, recon)  # CALLING INSERT DEF

    clear_entries()


# ==================================FRAME==============================================
Top = Frame(root, width=50, height=30, bd=8, relief="ridge")
Top.pack(side=TOP, fill=BOTH, expand=False)

Left = Frame(root, width=500, height=1500, bd=8, relief="ridge")
Left.pack(side=LEFT, fill=BOTH, expand=False)
Left.pack_propagate(0)

Middle = Frame(root, width=400, height=1500, bd=8, relief="ridge")
Middle.pack(side=LEFT, fill=BOTH, expand=True)
Left.pack_propagate(0)

Right = Frame(root, width=50, height=1500, bd=8, relief="flat")
Right.pack(side=RIGHT, fill=BOTH, expand=False)

Forms = Frame(Right, width=50, height=450)
Forms.pack(side=TOP)

Buttons = Frame(Right, width=50, height=100, bd=8, relief="flat")
Buttons.pack(side=BOTTOM)

# ==========================LABEL & COMBOS on right ====================

txt_from_account = Label(Forms, text="From Account", font=('arial', 16), bd=15)
txt_from_account.grid(row=1, column=0, stick="e")
combo1 = ttk.Combobox(Forms, font=("Times New Roman", 16), width=8, height=30)
combo1.grid(column=1, row=1)
combo1['values'] = tuple(combo_list)

txt_to_account = Label(Forms, text="To Account", font=('arial', 16), bd=15)
txt_to_account.grid(row=2, column=0, stick="e")
combo2 = ttk.Combobox(Forms, font=("Times New Roman", 16), width=8, height=30)
combo2.grid(column=1, row=2)
combo2['values'] = tuple(combo_list)

txt_description = Label(Forms, text="Description", font=('arial', 16), bd=15)
txt_description.grid(row=3, column=0, stick="e")
description = Entry(Forms, width=20, font=("Times New Roman", 16), )
description.grid(column=1, row=3, ipadx=1, pady=10)
txt_amount = Label(Forms, text="Amount in Rand", font=('arial', 16), bd=15)
txt_amount.grid(row=4, column=0, stick="e")
amt = Entry(Forms, font=("Times New Roman", 16))
amt.grid(column=1, row=4, ipadx=0, pady=10)

txt_blank = Label(Forms, text="", font=('arial', 16), bd=15)
txt_blank.grid(row=5, column=0, stick="e")


# ============================= DATES ================================
from datetime import datetime
now = datetime.now()  # current date and time
mth = now.strftime("%m")  # PROCESSING MONTH
v = IntVar()
e1 = Entry(Forms, text=v)
e1.grid(row=0, column=0)
v.set(mth)
e1.get()
yr = now.strftime("%Y")  # PROCESSING YEAR

w = IntVar()
e2 = Entry(Forms, text=w)
e2.grid(row=0, column=1)
w.set(yr)

# ========================== SUMMARY ACTUAL  =============================
def summary():
    tree.delete(*tree.get_children())    # CLEARING ENTRIES FROM BUDGET TREE
    tree1.delete(*tree1.get_children())  # CLEARING ENTRIES FROM BUDGET TREE1

    sum_tot = 0
    period = e1.get()
    period = period.replace('\r', '').replace('\n', '')
    period = ''.join(period.split())
    act_tot = ""
    with open('combo.csv') as f:

        for pointer in f:
            pointer = pointer.replace('\r', '').replace('\n', '')
            pointer = ''.join(pointer.split())

            cursor.execute('SELECT amount FROM takeon WHERE account = ? AND month = ?',
                    [pointer, period])
            result = cursor.fetchall()
            result = [amount[0] for amount in result]

            c = 0
            for x in result:
                c += x
                v = IntVar()
                v.set(c)

            month = period
            year = "2023"
            #desc = ""
            account = pointer
            #desc = ""
            amount = c
            #recon =""
            tree.insert("", END, values=("", month, year, account, "  ", amount))
            sum_tot = sum_tot + amount
            c = sum_tot
    sum_tot = Entry(Top, text=c, font=("Times New Roman", 16), width=30)
    sum_tot.grid(column=0, row=0, ipadx=30)

# ============================== DISPLAYING ACTUAL DATA =================================
def actuals():
    tree.delete(*tree.get_children())
    lookup = combo1.get()
    if not lookup.strip():
        showerror(" BLANK FIELDS")  # FAULT DETECTED
        return

    lookup = lookup.replace('\r', '').replace('\n', '')
    lookup = ''.join(lookup.split())

    period = e1.get()
    period = period.replace('\r', '').replace('\n', '')
    period = ''.join(period.split())

    cursor.execute('SELECT * FROM takeon WHERE account = ? AND month =?',
                   [lookup, period])
    fetch = cursor.fetchall()

    for row in fetch:
        tree.insert("", END, values=row)
    result = 0

    cursor.execute('SELECT * FROM takeon WHERE account = ? AND month =?',
                   [lookup, period])

    result = cursor.fetchall()

    result = [amount[5] for amount in result]

    c = 0
    for x in result:
        c += x

    v = IntVar()
    v.set(c)
    act_tot = Entry(Top, text=v, font=("Times New Roman", 16), width=30)
    act_tot.grid(column=0, row=0, ipadx=30)
    budget()


# ==================== DISPLAYING BUDGET ===============================
def budget():
    tree1.delete(*tree1.get_children())
    df = pd.read_excel(r"c:\PYTHON PROGRAMS\CAPTURE\budget.xlsx")  # reading excel
    df.to_csv(r"c:\PYTHON PROGRAMS\CAPTURE\budget.csv", index=True)  # converting to csv

    lookup = combo1.get()
    if not lookup.strip():
        showerror(" BLANK FIELDS")  # FAULT DETECTED
        return
    lookup = lookup.replace('\r', '').replace('\n', '')
    lookup = ''.join(lookup.split())

    with open(r"c:\PYTHON PROGRAMS\CAPTURE\budget.csv") as f:
        reader = csv.DictReader(f, delimiter=',')
        sumcol = 0
        c = 0
        for row in reader:
            bud_account = row['bud_account']
            if bud_account == lookup:
                bud_desct = row['bud_desc']
                bud_amount = row['bud_amount']
                tree1.insert("", 0, values=(bud_account, bud_desct, bud_amount))
                sumcol = sumcol + int(bud_amount)

            c = sumcol
            v = IntVar()
            v.set(c)
            bud_amt = Entry(Top, text=v, font=("Times New Roman", 16), width=10)
            bud_amt.grid(column=1, row=0, ipadx=30)
        f.close()


# ==================DELETING RECORD =====================

def selectedrow(event):
    # connection.Mydatabase.db()
    global acc_id
    curitem = tree.focus()
    contents = (tree.item(curitem))
    selecteditem: object = contents['values']
    acc_id = selecteditem[0]

    result = askquestion('Python - deleting Data', 'Are you sure you want to remove record',
                         icon="warning")
    if result == 'yes':
        cursor.execute('DELETE FROM takeon WHERE acc_id=?', [acc_id])
        conn.commit()


# ==================================BUTTONS WIDGET=====================================

button1 = Button(Buttons, text="CAPTURE", font=("Times New Roman", 16), relief="ridge", command=retrieve)
button1.grid(row=2, column=0)

button2 = Button(Buttons, text="", font=("Times New Roman", 16), relief="flat", command=space)
button2.grid(row=6, column=0)

button3 = Button(Buttons, text="DISPLAY", font=("Times New Roman", 16), relief="ridge", command=actuals)
button3.grid(row=9, column=0)

button4 = Button(Buttons, text="SUMMARY", font=("Times New Roman", 16), relief="ridge", command=summary)
button4.grid(row=9, column=1)

button5 = Button(Buttons, text="Exit", font=("Times New Roman", 16), relief="ridge", command=goodbye)
button5.grid(row=0, column=0)

# ==================================TREE FOR ACTUAL ========================================

scrollbary = Scrollbar(Left, orient=VERTICAL)
scrollbarx = Scrollbar(Left, orient=HORIZONTAL)
tree = ttk.Treeview(Left, columns=("id", "month", "year", "account", "desc", "amount", "recon"),
                    height=500, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading("#0", text="id",anchor='w')
tree.heading('month', text="Month", anchor=W)
tree.heading('year', text="Year", anchor=W)
tree.heading('account', text="Account", anchor=W)
tree.heading('desc', text="Description", anchor=W)
tree.heading('amount', text="Amount", anchor=W)
tree.heading('recon', text="Recon", anchor=W)

tree.column('#0', stretch=NO, minwidth=0, width=20)
tree.column('#1', stretch=NO, minwidth=0, width=40)
tree.column('#2', stretch=NO, minwidth=0, width=40)
tree.column('#3', stretch=NO, minwidth=0, width=40)
tree.column('#4', stretch=NO, minwidth=0, width=80)
tree.column('#5', stretch=NO, minwidth=0, width=80)
tree.column('#6', stretch=NO, minwidth=0, width=60)
tree.pack(fill=BOTH, expand=True)
tree.bind('<Double-Button-1>', selectedrow)

# =====================TREE FOR BUDGET ================================================

scrollbarx = Scrollbar(Middle, orient=HORIZONTAL)
scrollbary = Scrollbar(Middle, orient=VERTICAL)
tree1 = ttk.Treeview(Middle, columns=("bud_account", "bud_desct", "bud_amount"), height=400,
                     selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree1.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree1.xview)
scrollbarx.pack(side=BOTTOM, fill=X)

tree1.heading('bud_account', text="Account", anchor=W)
tree1.heading('bud_desct', text="Description", anchor=W)
tree1.heading('bud_amount', text="Amount", anchor=W)

tree1.column('#0', stretch=NO, minwidth=0, width=0)
tree1.column('#1', stretch=NO, minwidth=0, width=40)
tree1.column('#2', stretch=NO, minwidth=0, width=100)
tree1.column('#3', stretch=NO, minwidth=0, width=50)
tree1.pack(fill=BOTH, expand=True)
# double_click()

if __name__ == '__main__':
    root.mainloop()
