import os
from tkinter import *
from tkinter import ttk
from fpdf import FPDF
import datetime

from PIL import ImageTk, Image


root = Tk()

import sqlite3

global token_number_container
token_number_container = []

variable1 = StringVar(root)


class App(object):

    def __init__(self, master, path):
        self.nodes = dict()
        frame = Frame(master)

        scrollbary1 = Scrollbar(frame, orient=VERTICAL)
        scrollbarx1 = Scrollbar(frame, orient=HORIZONTAL)
        self.tree1 = ttk.Treeview(frame,height = 300,yscrollcommand=scrollbary1.set, xscrollcommand=scrollbarx1.set)
        # ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree1.yview)
        # xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree1.xview)
        # self.tree1.configure(yscroll=scrollbary1.set, xscroll=scrollbarx1.set)
        scrollbary1.config(command=self.tree1.yview)
        scrollbary1.pack(side=RIGHT, fill=Y)
        scrollbarx1.config(command=self.tree1.xview)
        scrollbarx1.pack(side=BOTTOM, fill=X)



        self.tree1.heading('#0', text='PDF Locations', anchor='w')

        self.tree1.pack()
        # ysb.grid(row=0, column=1, sticky='ns')
        # xsb.grid(row=1, column=0, sticky='ew')
        frame.grid()

        abspath = os.path.abspath(path)
        self.insert_node('', abspath, abspath)
        self.tree1.bind('<<TreeviewOpen>>', self.open_node)

    def insert_node(self, parent, text, abspath):
        node = self.tree1.insert(parent, 'end', text=text, open=False)
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree1.insert(node, 'end')

    def open_node(self, event):
        node = self.tree1.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree1.delete(self.tree1.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))














def publish_pdf(pdf, token_number_container):

    time = datetime.datetime.now().date()
    print(time)
    time = str(time) + str(f"-[{datetime.datetime.now().time()}]")
    print(time)
    time = datetime.datetime.now().strftime('%d-%m-%Y--[%H-%M-%S]')
    pdf_folder_date = datetime.datetime.now().strftime('%d-%m-%Y')

    try:
        os.mkdir(f"pdfs")
    except OSError as error:
        print(error)

    try:
        os.mkdir(f"pdfs/{pdf_folder_date}")
    except OSError as error:
        print(error)
    last = len(token_number_container)-1
    pdf.output(f"pdfs/{pdf_folder_date}/(({token_number_container[0]}-{token_number_container[last]}))---{time}.pdf")
    tree2.insert('', 'end', values=(f"(({token_number_container[0]}-{token_number_container[last]}))---{time}.pdf"))



def generate_pdf(token_number_container):
    global pdf


    pdf = FPDF()
    pdf.add_page()

    for items in token_number_container:
        pdf.set_font("Arial", size=15)

        pdf.cell(200, 10, txt="PRABHAT ENTERPRISES",
                 ln=1, align='C')

        pdf.set_font("Arial", size=40)
        pdf.cell(200, 10, txt=f"{items}",
                 ln=1, align='C')

        pdf.set_font("Arial", size=12)
        # add another cell
        pdf.cell(200, 10, txt="CSC AADHAR CENTRE PRABHAT ENTERPRISES",
                 ln=1, align='C')

        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="BARDAD CHAURAHAH NAUSAD GORAKHPUR 273401, Mob- 9956509913",
                 ln=1, align='C')

        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10,
                 txt="--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
                     ""
                     ""
                     "",
                 ln=1, align='C')

        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="                                                                                ",
                 ln=1, align='C')


    publish_pdf(pdf, token_number_container)
    token_number_container.clear()


def create_pdf(conn, token_number_container):


    connn = sqlite3.connect('pdf.db')



    c = connn.cursor()

    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='pdf_record' ''')

    if c.fetchone()[0] == 1:

        qry = "insert into pdf_record (print) values(?);"
        try:
            cur = connn.cursor()
            connn.execute('INSERT INTO pdf_record(NAME, TIME) values (?,?)', ("Rahul ", "4:23 AM "))
            connn.commit()
            print("records added successfully")
        except:
            print("error in operation")
            # connn.rollback()

        sql = "SELECT * from pdf_record;"
        cur = connn.cursor()
        cur.execute(sql)
        while True:
            record = cur.fetchone()
            if record == None:
                break
            else:
                if record[0] == 5:
                    connn.execute("DROP TABLE pdf_record")
                    print("creating Table...")
                    connn.execute('''CREATE TABLE pdf_record
                                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                  NAME           TEXT    NOT NULL,
                                 TIME          TEXT    NOT NULL)''')
                    print("Table created successfully")

                    connn.execute('INSERT INTO pdf_record(NAME, TIME) values (?,?)', ("NULL", f"{datetime.datetime.now().strftime('%d-%m-%Y--[%H-%M-%S]')}"))

                    connn.commit()
                    pass
                else:
                    cursor = conn.execute("SELECT ID, NAME, TIME from BOOKS")
                    for data in cursor:
                        data = data

                    # generate_pdf(int(record[0]))
                    print(f"pdf written {record[0]}")
            print(record)
        hold_label.config(text=f"Tokens on Hold: {len(token_number_container)}")
        if len(token_number_container) == 4:
            generate_pdf(token_number_container)
            hold_label.config(text=f"Tokens on Hold: 0")

    else:
        print("creating Table...")
        connn.execute('''CREATE TABLE pdf_record
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
              NAME           TEXT    NOT NULL,
             TIME          TEXT    NOT NULL)''')
        print("Table created successfully")

        connn.execute('INSERT INTO pdf_record(NAME, TIME) values (?,?)', ("NULL", f"{datetime.datetime.now().strftime('%d-%m-%Y--[%H-%M-%S]')}"))

        connn.commit()

        sql = "SELECT * from pdf_record;"
        cur = connn.cursor()
        cur.execute(sql)
        while True:
            record = cur.fetchone()
            if record == None:
                break
            else:
                if record[0] == 5:
                    connn.execute("DROP TABLE pdf_record")
                    pass
                else:
                    # generate_pdf(int(record[0]))
                    print(f"pdf written {record[0]}")
            print(record)

        hold_label.config(text=f"Tokens on Hold: {len(token_number_container)}")
        if len(token_number_container) == 4:
            generate_pdf(token_number_container)
            hold_label.config(text=f"Tokens on Hold: 0")









def previous_data():
    conn = sqlite3.connect('ddio_ember.db')
    c = conn.cursor()
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='BOOKS' ''')

    if c.fetchone()[0] == 1:
        print("table Exists..")

        cursor = conn.execute("SELECT ID, NAME, TIME from BOOKS")
        print(cursor)
        for data in cursor:
            print(data)
            tree.insert('', 'end', values=(data[0], data[1], data[2]))

        conn.close()

def Database():
    if variable1.get() == "" or variable1.get() == " ":
        from tkinter import messagebox
        messagebox.showerror("No entry", "Please enter a Name")
        pass

    else:
        conn = sqlite3.connect('ddio_ember.db')
        c = conn.cursor()
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='BOOKS' ''')



        if c.fetchone()[0] == 1:
            print("table Exists..")

            qry = "insert into BOOKS (NAME, TIME) values(?,?);"
            try:
                cur = conn.cursor()
                cur.execute(qry, (f"{variable1.get()}", f"{datetime.datetime.now().strftime('%H:%M:%S')}"))
                conn.commit()
                print("records added successfully")
            except:
                print("error in operation")
                conn.rollback()

            sql = "SELECT * from BOOKS;"
            cur = conn.cursor()
            cur.execute(sql)
            while True:
                record = cur.fetchone()
                if record == None:
                    break
            c= conn.cursor()
            cursor = c.execute("SELECT * from BOOKS")
            cursor = cursor.fetchall()
            # print(len(cursor))
            # for row in cursor:
            #     print ("ID = ", row[0])
            #     print ("NAME = ", row[1])
            #     print ("TIME = ", row[2], "\n")

            cursor = conn.execute("SELECT ID, NAME, TIME from BOOKS")
            # print(len(cursor.fetchall()))
            cursor= conn.execute("SELECT ID, NAME, TIME from BOOKS")
            for data in cursor:
                data = data
            tree.insert('', 'end', values=(data[0], data[1], data[2]))
            token_number_container.append(int(data[0]))
            create_pdf(conn, token_number_container)

            conn.close()


        else:
            print("creating Table...")
            conn.execute('''CREATE TABLE BOOKS
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                  NAME           TEXT    NOT NULL,
                 TIME          TEXT    NOT NULL)''')
            print("Table created successfully")


            conn.execute('INSERT INTO BOOKS(NAME, TIME) values (?,?)', (f"{variable1.get()}", f"{datetime.datetime.now().strftime('%H:%M:%S')}"))
            conn.commit()

            cursor = conn.execute("SELECT ID, NAME, TIME from BOOKS")
            print(cursor)
            for data in cursor:
                data = data
            tree.insert('', 'end', values=(data[0], data[1], data[2]))
            token_number_container.append(int(data[0]))
            create_pdf(conn, token_number_container)

            conn.close()


def on_close():

    connect = sqlite3.connect('chache.db')
    c = connect.cursor()
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='HOLD' ''')



    if c.fetchone()[0] == 1:
        print("storing chache")
        if True:
            for i in token_number_container:
                connect.execute('INSERT INTO HOLD(TOKEN, TIME) values (?,?)', (i, f"{i}"))
                connect.commit()
            connect.close()

    else:
        print("creating chache table ")
        connect.execute('''CREATE TABLE HOLD
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                  TOKEN           INTEGER    NOT NULL,
                 TIME          TEXT    NOT NULL)''')
        if True:
            for i in token_number_container:
                connect.execute('INSERT INTO HOLD(TOKEN, TIME) values (?,?)', (i, f"{i}"))
                connect.commit()
            connect.close()

    root.destroy()



def print_on_hold_tokens():

    if len(token_number_container) == 0:
        from tkinter import messagebox
        messagebox.showerror("Please Enter Data", "No Tokens on Hold")
        pass

    elif len(token_number_container) == 1 or len(token_number_container) == 2 or len(token_number_container) == 3:
        generate_pdf(token_number_container)
        hold_label.config(text=f"Tokens on Hold: {len(token_number_container)}")


def on_start_getTokens():
    connect = sqlite3.connect('chache.db')
    c = connect.cursor()
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='HOLD' ''')

    if c.fetchone()[0] == 1:
        print("chache Exists...")
        cursor = connect.execute("SELECT TOKEN, TIME from HOLD")

        for data in cursor:
            token_number_container.append(int(data[1]))
            print(data[1])

        hold_label.config(text = f"Tokens on Hold: {len(token_number_container)}")
        connect.execute("DROP TABLE HOLD")

    else:
        print("no chache available")


def new():
    for i in tree.get_children():
        tree.delete(i)

    for i in tree2.get_children():
        tree2.delete(i)

    token_number_container.clear()
    hold_label.config( text = f"Tokens on Hold: {len(token_number_container)}")
    name_field.delete(0, 'end')
    import os
    os.remove("ddio_ember.db")
    os.remove("chache.db")
    os.remove("pdf.db")



if __name__ == "__main__":



    root.geometry("1000x500")

    root.title("PRABHAT ENTERPRISES")
    root.configure(background='white')
    # root.bind('<Escape>', lambda e: root.destroy())

    root.protocol("WM_DELETE_WINDOW",on_close)


    Top = Frame(root, width=700, height=50, bd=8, bg = "white")
    Top.pack(side=TOP, fill =X)


    img = ImageTk.PhotoImage(Image.open("logo.jpeg").resize((110,130)))
    panel = Label(Top, image=img, bg='white')
    panel.grid(row = 1, column = 1, ipadx ="25")

    developer = Label(Top,text = "Developed By: Rahul Ranjan Singh (8318807980)\n                       Aman Sharma      (9369438757)",bg="white",font = "sans-serif 7 bold")
    developer.grid(row = 0, column = 3, ipadx = "20")

    headlabel = Label(Top, text='PRABHAT ENTERPRISES', fg='black', bg="white",font = "sans-serif 24 bold")
    headlabel.grid(row=1, column=2)
    Top.columnconfigure(2, weight=1)

    global name_field

    name_field = Entry(Top, border = 5, textvariable = variable1, width =30 , font = "sans-serif 15" )
    name_field.grid(ipadx = "20",row= 10, column = 2)

    add_to_database_butoon = Button(Top, text = "Add Recipient", bg = "sky blue", fg = "white",font = "sans-serif 15 bold", command=Database)
    add_to_database_butoon.grid(row = 20, column = 2, ipadx = "20", pady = 23)

    global hold_label
    hold_label = Label(Top, text = f"Tokens on Hold: {len(token_number_container)}", fg= 'black', bg = 'white', font="sans-serif 10" )
    hold_label.grid(row = 25, column = 3, ipadx = "20", pady = 5)

    on_start_getTokens()
    print_buttonn = Button(Top, text = "Print hold Tokens", bg = "red", fg = "white",font = "sans-serif 9 bold", command=print_on_hold_tokens)
    print_buttonn.grid(row = 25, column = 4, ipadx = "20", pady = 5)

    Body2 = Frame(root, width=50, height=300, bd=8, relief="sunken")
    Body2.pack(side=LEFT, fill=X)
    scrollbary0 = Scrollbar(Body2, orient=VERTICAL)
    scrollbarx0 = Scrollbar(Body2, orient=HORIZONTAL)

    global tree2

    tree2 = ttk.Treeview(Body2, columns=("Firstname"), selectmode="extended", height=200,
                         yscrollcommand=scrollbary0.set, xscrollcommand=scrollbarx0.set)
    scrollbary0.config(command=tree2.yview)
    scrollbary0.pack(side=RIGHT, fill=Y)
    scrollbarx0.config(command=tree2.xview)
    scrollbarx0.pack(side=BOTTOM, fill=X)
    tree2.heading('Firstname', text="Generated PDF's", anchor=W)
    tree2.column('#0', stretch=NO, minwidth=0, width=70)



    tree2.pack(fill=X)

    middle = Frame(root, width=700, height=300, bd=8, relief="sunken")
    middle.pack(side=RIGHT, fill=X)


    Body = Frame(root, width=700, height=300, bd=8, relief="sunken")
    Body.pack(side=BOTTOM, fill = X)


    scrollbary = Scrollbar(Body, orient=VERTICAL)
    scrollbarx = Scrollbar(Body, orient=HORIZONTAL)
    global tree
    tree = ttk.Treeview(Body, columns=("Firstname", "Lastname", "Address"), selectmode="extended", height=300,
                        yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Firstname', text="Token No", anchor=W)
    tree.heading('Lastname', text="Name of Recepient", anchor=W)
    tree.heading('Address', text="Time of Entry", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=200)
    tree.column('#2', stretch=NO, minwidth=0, width=200)
    tree.column('#3', stretch=NO, minwidth=0, width=200)
    tree.pack(fill=X)

    menubar = Menu(root)

    # Adding File Menu and commands
    file = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=file)
    file.add_command(label='New File', command=new)
    file.add_command(label='Open...', command=None)
    file.add_command(label='Save', command=None)
    file.add_separator()
    file.add_command(label='Exit', command=on_close)

    # Adding Edit Menu and commands
    edit = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Edit', menu=edit)
    edit.add_command(label='Cut', command=None)
    edit.add_command(label='Copy', command=None)
    edit.add_command(label='Paste', command=None)
    edit.add_command(label='Select All', command=None)
    edit.add_separator()
    edit.add_command(label='Find...', command=None)
    edit.add_command(label='Find again', command=None)

    # Adding Help Menu
    help_ = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Help', menu=help_)
    help_.add_command(label='Tk Help', command=None)
    help_.add_command(label='Demo', command=None)
    help_.add_separator()
    help_.add_command(label='About Tk', command=None)

    # display Menu
    root.config(menu=menubar)

    app = App(middle, path='pdfs')

    previous_data()
    root.mainloop()