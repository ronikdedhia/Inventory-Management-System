#Imports
from tkinter import *
from tkinter.font import BOLD
from datetime import datetime
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
from PIL import ImageTk
import sqlite3

#global variables
global nusername, npassword
global count, text
global yIndex
global nameList, qtyList, priceList, idList, stockList, costPriceList

nameList, qtyList, priceList, idList, stockList, costPriceList = [], [], [], [], [], []
yIndex = 75
text = ''
count = 0

#root window 
root = Tk()
root.title('Inventory Management System')
root.geometry("1366x728+75+50")
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH,expand=20)
    
        # ===========Background Image===========
        self.frame = ImageTk.PhotoImage(file='images\login.png')
        self.image_panel = Label(master, image=self.frame)
        self.image_panel.pack(fill='both', expand='yes')
app = Window(root)

# =========Variables=========
USERNAME = StringVar()
PASSWORD = StringVar()
CONFIRMPASSWORD = StringVar()
SEARCH = StringVar()
PRODUCT_NAME = StringVar()
PRODUCT_QTY = IntVar()
PRODUCT_PRICE = IntVar()
PRODUCT_SELL_PRICE = IntVar()
PRODUCT_ID = IntVar()
TOTAL = IntVar()
AMOUNT_GIVEN = IntVar()
BALANCE = IntVar()
QUANTITY = IntVar()

#to animate heading of login page
def Slider():
    global count
    global text
    if count >= len(titleTxt):
        heading.config(text=titleTxt)

    else:
        text = text + titleTxt[count]
        heading.config(text=text)
    count += 1

    heading.after(60, Slider)

#to connect database
def Database():
    global nusername
    global npassword
    global conn, cursor
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `product` (product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, product_name TEXT, product_qty TEXT, product_price TEXT)")
    cursor.execute("SELECT * FROM `admin` WHERE `username` = 'sakshi' AND `password` = 'sakshi'")
    conn.commit()   

#to exit application
def Exit():
    result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

#to check credentials 
def Login():
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        warnTxt.config(text="Please complete the required field!")
    else:
        cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
            data = cursor.fetchone()
            admin_id = data[0]
            USERNAME.set("")
            PASSWORD.set("")
            warnTxt.config(text="")
            cursor.close()
            conn.close()
            ShowHome()
        else:
            warnTxt.config(text="Invalid username or password")
            USERNAME.set("")
            PASSWORD.set("")

#to display products in list in inventory management    
def DisplayData():
    Database()
    cursor.execute("SELECT * FROM `product`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

#to display sales Data in list
def DisplaySalesData():
    Database()
    cursor.execute("SELECT * FROM `sales`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree3.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

#to display products in list in bill generator
def DisplayProductList():
    Database()
    cursor.execute("SELECT * FROM `product`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree1.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

#to display transactions in list
def DisplayTransactionData():
    Database()
    cursor.execute("SELECT * FROM `transactions`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree2.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

#to search products
def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT * FROM `product` WHERE `product_name` LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

#to search transactions
def SearchTransaction():
    if SEARCH.get() != "":
        tree2.delete(*tree2.get_children())
        Database()
        cursor.execute("SELECT * FROM `transactions` WHERE `transaction_id` LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree2.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

#window for adding products
def ShowAddNew():
    global addNewProduct
    addNewProduct = Toplevel()
    addNewProduct.title("ADD NEW PRODUCT")
    addNewProduct.geometry("600x720+75+50")
    addNewProduct.resizable(0, 0)
    addNewProduct.iconbitmap("images\\ucoe.ico")

    PRODUCT_NAME.set("")
    PRODUCT_PRICE.set("")
    PRODUCT_SELL_PRICE.set("")
    PRODUCT_QTY.set("")

    # ==========background Image===========
    image = ImageTk.PhotoImage(file="images\\addNewProduct.png")
    background = Label(addNewProduct, image=image)
    background.image = image
    background.pack(fill="both", expand="yes")

    # ===========Labels And Inputs============
    heading = Label(addNewProduct,text = "ADD PRODUCT DETAILS",font=("yu gothic ui", 18, "bold"), bg= "white", fg = "black" )
    heading.place(x=150, y=60, width = 300)

    productName_label = Label(addNewProduct,text = "PRODUCT NAME",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
    productName_label.place(x=115, y=105, width = 200)
    name = Entry(addNewProduct, textvariable=PRODUCT_NAME,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
    name.place(x=150, y=140, width=300)

    productQt_label = Label(addNewProduct,text = "PRODUCT QUANTITY",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
    productQt_label.place(x=130, y=230, width = 200)
    qty = Entry(addNewProduct, textvariable=PRODUCT_QTY,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
    qty.place(x=150, y=260, width=200)

    productPrice_label = Label(addNewProduct,text = "COST PRICE",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
    productPrice_label.place(x=90, y=350, width = 200)
    price = Entry(addNewProduct, textvariable=PRODUCT_PRICE,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
    price.place(x=150, y=385, width=200)

    sellPrice_label = Label(addNewProduct,text = "SELL PRICE",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
    sellPrice_label.place(x=90, y=470, width = 200)
    sellprice = Entry(addNewProduct, textvariable=PRODUCT_SELL_PRICE,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
    sellprice.place(x=150, y=505, width=200)

    # ============Button==================
    saveBtnImage = ImageTk.PhotoImage(file='images\\save.png')
    saveBtn = Button(addNewProduct,image=saveBtnImage, command=AddNew, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
    saveBtn.image = saveBtnImage
    saveBtn.place(x=170, y=550)

#adding products to database
def AddNew():
    Database()
    cursor.execute("INSERT INTO `product` (product_name, product_qty, product_price, product_selling_price) VALUES(?, ?, ?, ?)", (str(PRODUCT_NAME.get()), int(PRODUCT_QTY.get()), int(PRODUCT_PRICE.get()), int(PRODUCT_SELL_PRICE.get())))
    conn.commit()
    PRODUCT_NAME.set("")
    PRODUCT_PRICE.set("")
    PRODUCT_SELL_PRICE.set("")
    PRODUCT_QTY.set("")
    cursor.close()
    conn.close()
    Reset()

#updating product list in inventory management
def Reset():
    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("Search")

#updating product list in bill generator
def Reset1():
    tree1.delete(*tree1.get_children())
    DisplayProductList()

#updating transaction list 
def Reset2():
    tree2.delete(*tree2.get_children())
    DisplayTransactionData()

#deleting products from database
def Delete():
    if not tree.selection():
       tkMessageBox.showinfo("Inventory System","Please Select A Product From List", icon="warning")
    else:
        result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `product` WHERE `product_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()

#deleting transactions from database
def DeleteTransaction():
    if not tree2.selection():
       tkMessageBox.showinfo("Inventory System","Please Select A Transaction From List", icon="warning")
    else:
        result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to delete this Transaction?', icon="warning")
        if result == 'yes':
            curItem = tree2.focus()
            contents =(tree2.item(curItem))
            selecteditem = contents['values']
            tree2.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `transactions` WHERE `transaction_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()

#window for changing password
def changePassword():
    global passwordPage
    global nusername
    global npassword
    passwordPage=Toplevel()
    passwordPage.title("Change Password")
    passwordPage.geometry("500x600")
    passwordPage.resizable(0,0)
    passwordPage.iconbitmap("images\\ucoe.ico")

    # ===========background Image============
    image = ImageTk.PhotoImage(file="images\\changePasswordBG.png")
    background = Label(passwordPage, image=image)
    background.image = image
    background.pack(fill="both", expand="yes")

    # ==========Labels and Inputs==========
    heading = Label(passwordPage,text = "CHANGE PASSWORD",font=("yu gothic ui", 18, "bold"), bg= "white", fg = "black" )
    heading.place(x=120, y=30, width = 250)

    passwordLabel = Label(passwordPage,text = "NEW PASSWORD",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
    passwordLabel.place(x=40, y=95, width = 200)
    password = Entry(passwordPage, textvariable=PASSWORD,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15, show="*")
    password.place(x=65, y=130, width=200)

    cpassLabel = Label(passwordPage,text = "CONFIRM PASSWORD",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
    cpassLabel.place(x=60, y=220, width = 200)
    cpass = Entry(passwordPage, textvariable=CONFIRMPASSWORD,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15, show="*")
    cpass.place(x=65, y=255, width=200)

    # ==========Button=============
    saveBtnImage = ImageTk.PhotoImage(file='images\\save.png')
    saveBtn = Button(passwordPage,image=saveBtnImage, command=updatePassword, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
    saveBtn.image = saveBtnImage
    saveBtn.place(x=120, y=430)
    saveBtn.bind('<Return>', Login)

#to update password
def updatePassword():
    global nusername
    global npassword
    Database()
    cursor.execute("UPDATE admin SET password='{}' WHERE username='admin' ".format(str(PASSWORD.get())))
    PASSWORD.set("")
    conn.commit()
    cursor.close()
    conn.close()
    tkMessageBox.showinfo("Username/Password","Password has been changed")
    tkMessageBox.showinfo("Username/Password","Please Open the File again")
    passwordPage.destroy()
    Home1.destroy()

#to add item to the Cart list
def addToCart():
    global yIndex, nameList, qtyList, priceList, idList, stockList,costPriceList, productName, Quantity, Price
    Database()

    if (QUANTITY.get() != 0):
        cursor.execute("SELECT * FROM `product` WHERE `product_id` LIKE ?",('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall() #fetching the data
        if fetch != []:
            name = fetch[0][1]
            qty = QUANTITY.get()
            costPrice = qty*int(fetch[0][3])
            price = qty*int(fetch[0][4])
            stock = fetch[0][2]
            id = fetch[0][0]

            if int(fetch[0][2]) >= qty:
                productName = Label(bill, text=name, font=("yu gothic ui", 10), bg="white", width=50, anchor=W)
                productName.place(x=953, y=yIndex, width=130)

                Quantity = Label(bill, text=qty, bg="white", font=("yu gothic ui", 10), width=100, anchor=W)
                Quantity.place(x=1153, y=yIndex, width=50)

                Price = Label(bill, text=price, bg="white", font=("yu gothic ui", 10), width=100, anchor=W)
                Price.place(x=1253, y=yIndex, width=50)

                nameList.append(name)
                qtyList.append(qty)
                costPriceList.append(costPrice)
                priceList.append(price)
                idList.append(id)
                stockList.append(stock)

                TOTAL.set(TOTAL.get()+price)
                totalLabel.configure(text="Total = %i"%TOTAL.get())
                BALANCE.set(TOTAL.get()-AMOUNT_GIVEN.get())
                QUANTITY.set(0)
                SEARCH.set("")
                search1.focus()
                fetch = []
                cursor.close()
                conn.close()

                yIndex += 20
                Reset1()
            else:
                tkMessageBox.showinfo("LOW STOCK",("We Have Only "+fetch[0][2]+" "+name+" In Stock"))
        else:
            tkMessageBox.showinfo("OUT OF STOCK","Item Not Found!!!!")
    else:
        tkMessageBox.showinfo("Warning", "Quantity Cannot Be 0")

#making pdf invoice and updating database
def GenerateBill():
    global nameList, qtyList, priceList, idList, stockList,costPriceList, yIndex
    Database()

    yIndex = 75
    now = datetime.now()  
    transaction_id=str(now.strftime("%d%m%Y%H%M%S"))
    date = str(now.strftime("Date : %d/%m/%Y"))
    time = str(now.strftime("Time : %H:%M:%S"))
    vertical = 10.55

    canvas = Canvas("invoices\\"+transaction_id+".pdf")
    canvas.drawString(0.25 * inch, vertical * inch, "Product Name")
    canvas.drawString(5.25 * inch, vertical * inch, "Quantity")
    canvas.drawString(7.25 * inch, vertical * inch, "Price")
    canvas.drawString(2.65 * inch, 11.25 * inch, "INVENTORY MANAGEMENT SYSTEM")
    canvas.drawString(0 * inch, 10.95 * inch, "______________________________________________________________________________________________")
    canvas.drawString(0 * inch, 10.25 * inch, "______________________________________________________________________________________________")

    counter = 0
    vertical-=0.2
    for n in nameList:
        vertical-=0.5
        canvas.drawString(0.25 * inch, vertical * inch, n)
        canvas.drawString(5.25 * inch, vertical * inch, str(qtyList[counter]))
        canvas.drawString(7.25 * inch, vertical * inch, str(priceList[counter]))
        counter+=1
        if counter == len(nameList):
            vertical-=0.2
            canvas.drawString(0 * inch, vertical * inch, "______________________________________________________________________________________________")
            vertical-=0.5
            canvas.drawString(5.25 * inch, vertical * inch, "Total")
            canvas.drawString(7.25 * inch, vertical * inch, str(TOTAL.get()))
            vertical-=0.2
            canvas.drawString(0 * inch, vertical * inch, "______________________________________________________________________________________________")
            vertical-=0.8
            canvas.drawString(5.25 * inch, vertical * inch, "Invoice ID : "+str(transaction_id))
            canvas.drawString(0.25 * inch, vertical * inch, date)
            canvas.drawString(1.85 * inch, vertical * inch, time)

    canvas.save()

    counter1 = 0
    for n in nameList:
        profit = priceList[counter1] - costPriceList[counter1]
        cursor.execute("SELECT * FROM `sales` WHERE `product_id` LIKE ?",('%'+str(idList[counter1])+'%',))
        fetch = cursor.fetchall()
        if fetch == []:
            cursor.execute("INSERT INTO `sales` (product_id, product_name, product_qty, product_profit) VALUES(?, ?, ?, ?)",(int(idList[counter1]), nameList[counter1], str(qtyList[counter1]), str(profit)))
            conn.commit()
        else:
            cursor.execute("UPDATE `sales` SET `product_qty`='{}', `product_profit`='{}' WHERE `product_id`='{}'".format(str(int(fetch[0][2])+qtyList[counter1]), str(int(fetch[0][3])+profit), int(idList[counter1])))
            conn.commit()

        cursor.execute("INSERT INTO `transactions` (transaction_id, product_name, product_qty, product_price, total_amount) VALUES(?, ?, ?, ?, ?)",(int(transaction_id), n, str(qtyList[counter1]), str(priceList[counter1]), str(TOTAL.get())))
        conn.commit()

        cursor.execute("UPDATE `product` SET `product_qty`='{}' WHERE `product_id`={}".format(str(int(stockList[counter1])-int(qtyList[counter1])), int(idList[counter1])))
        conn.commit()
        profit = 0
        counter1+=1

    tkMessageBox.showinfo("GENERATED", "Your Bill Is Generated Check Invoice Section")
    
    for i in range(counter1):
        tempName = Label(bill,text="", bg = "white")
        tempName.place(x=953, y=yIndex, width=130)

        tempQty = Label(bill,text="", bg = "white")
        tempQty.place(x=1153, y=yIndex, width=50)

        tempName = Label(bill,text="", bg = "white")
        tempName.place(x=1253, y=yIndex, width=50)
        yIndex+=20
        i+=1

    nameList, qtyList, priceList, idList, stockList, costPriceList = [], [], [], [], [], []

    TOTAL.set(0)
    QUANTITY.set(0)
    BALANCE.set(0)
    SEARCH.set("")
    AMOUNT_GIVEN.set(0)
    totalLabel.configure(text=("Total = %s"%str(TOTAL.get())))
    profit = 0
    yIndex = 75
    Reset1()
    conn.close()

#to display change
def calculateChange():
    BALANCE.set(int(AMOUNT_GIVEN.get())-int(TOTAL.get()))
    balance.configure(textvariable=BALANCE)

#window for list of activities
def Home1():
    global Home1
    Home1 = Toplevel()
    Home1.title("Home")
    Home1.geometry("600x720+75+50")
    Home1.resizable(False, False)
    Home1.iconbitmap("images\\ucoe.ico")

    # ============background Image============
    image = ImageTk.PhotoImage(file="Images\\home1.png")
    background = Label(Home1, image=image)
    background.image = image
    background.pack(fill="both", expand="yes")

    # ============Buttons===================
    manageINBtnImage = ImageTk.PhotoImage(file= "Images\\manageIN.png") 
    manageINBtn = Button(Home1, image = manageINBtnImage, bg="white", activebackground="white", borderwidth=0, cursor="hand2", command=Home)
    manageINBtn.image = manageINBtnImage
    manageINBtn.place(x=150, y=60)

    billBtnImage = ImageTk.PhotoImage(file= "Images\\bill.png") 
    billBtn = Button(Home1, image = billBtnImage, bg="white", activebackground="white", borderwidth=0, cursor="hand2", command=bill)
    billBtn.image = billBtnImage
    billBtn.place(x=150, y=160)

    salesBtnImage = ImageTk.PhotoImage(file= "Images\\viewSales.png") 
    salesBtn = Button(Home1, image = salesBtnImage, bg="white", activebackground="white", borderwidth=0, cursor="hand2", command=sales)
    salesBtn.image = salesBtnImage
    salesBtn.place(x=150, y=260)

    transactionBtnImage = ImageTk.PhotoImage(file= "Images\\transactions.png") 
    transactionBtn = Button(Home1, image = transactionBtnImage, bg="white", activebackground="white", borderwidth=0, cursor="hand2", command=transactions)
    transactionBtn.image = transactionBtnImage
    transactionBtn.place(x=150, y=360)

    changePassBtnImage = ImageTk.PhotoImage(file='images\\changePassword.png')
    changePassBtn = Button(Home1,image=changePassBtnImage, command=changePassword, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
    changePassBtn.image = changePassBtnImage
    changePassBtn.place(x=150, y=460)

    logoutBtnImage = ImageTk.PhotoImage(file='images\logout.png')
    logoutBtn = Button(Home1,image=logoutBtnImage, command=Logout, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
    logoutBtn.image = logoutBtnImage
    logoutBtn.place(x=150, y=560)

#destroy login page and displaying list of activities page
def ShowHome():
    root.withdraw()
    Home1()

#window for bill generator
def bill():
    global totalLabel, amountGiven, balance, search1, bill, tree1, balance
    PRODUCT_ID.set("")
    TOTAL.set(0)
    AMOUNT_GIVEN.set(0)
    BALANCE.set(0)
    SEARCH.set("")
    QUANTITY.set(0)
    bill = Toplevel()
    bill.title("Bill Generator")
    bill.geometry("1366x720+75+50")
    bill.resizable(False, False)
    bill.iconbitmap("images\\ucoe.ico")
    Title = Frame(bill, bd=0, relief=SOLID)
    Title.pack(pady=0)

    productListFrame = Frame(bill, width=100, height=100, bg="black")
    productListFrame.place(x=427, y=50)

    whiteFrame = Frame(bill, width=477, height=100, bg="white")
    whiteFrame.place(x=940, y=645)

    whiteFrame2 = Frame(bill, width=990, height=50, bg="white")
    whiteFrame2.place(x=427, y=0)

    whiteFrame3 = Frame(bill, width=100, height=644, bg="white")
    whiteFrame3.place(x=1317, y=51)

    border = Frame(bill, width=1, height=50, bg="black")
    border.place(x=939, y=0)

    border1 = Frame(bill, width=1, height=50, bg="black")
    border1.place(x=427, y=0)

    border2 = Frame(bill, width=937, height=1, bg="black")
    border2.place(x=427, y=0)

    border2 = Frame(bill, width=500, height=1, bg="black")
    border2.place(x=940, y=645)

    border3 = Frame(bill, width=500, height=1, bg="black")
    border3.place(x=940, y=50)

    # ===========Background Image===========
    image = ImageTk.PhotoImage(file='images\\billPage.png')
    background = Label(Title, image=image)
    background.image = image
    background.pack(fill='both', expand='yes')

    # ============Labels===================
    productListLabel = Label(bill, text="PRODUCTS LIST",fg="black", bg="white", font=("yu gothic ui", 15, "bold"), width=100)
    productListLabel.place(x=590, y=10, width=200)

    dateLabel = Label(bill, text="Date:12/12/12      Time:12:12:12", fg="black", bg="white", font=("yu gothic ui", 15, "bold"),width=100)
    dateLabel.place(x=960, y=10, width=400)

    productNameLabel = Label(bill, text="Product Name", font=("yu gothic ui", 10), bg="white", width=50, anchor=W)
    productNameLabel.place(x=953, y=55, width=100)

    QuantityLabel = Label(bill, text="Quanity", bg="white", font=("yu gothic ui", 10), width=100, anchor=W)
    QuantityLabel.place(x=1153, y=55, width=50)

    PriceLabel = Label(bill, text="Price", bg="white", font=("yu gothic ui", 10), width=100, anchor=W)
    PriceLabel.place(x=1253, y=55, width=50)

    totalLabel = Label(bill, text=("Total = %s"%str(TOTAL.get())), fg="black", bg="white", font=("yu gothic ui", 15, "bold"),width=100)
    totalLabel.place(x=947, y=665, width=150)

    QuantityLabel1 = Label(bill, text="QUANTITY",fg = "#9d9d9d", bg="white", font=("yu gothic ui", 15, "bold"),width=100)
    QuantityLabel1.place(x=80, y=108, width=100)

    totalLabel1 = Label(bill, text="TOTAL", fg = "#9d9d9d", bg="white", font=("yu gothic ui", 15, "bold"),width=100)
    totalLabel1.place(x=75, y=256, width=80)

    AmountGivenLabel = Label(bill, text="AMOUNT GIVEN", fg = "#9d9d9d", bg="white", font=("yu gothic ui", 15, "bold"),width=100)
    AmountGivenLabel.place(x=85, y=345, width=150)

    balanceLabel = Label(bill, text="BALANCE", fg = "#9d9d9d", bg="white", font=("yu gothic ui", 15, "bold"),width=100)
    balanceLabel.place(x=75, y=434, width=100)

    # ============Inputs==================
    search1 = Entry(Title, textvariable=SEARCH,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 15, "bold"), width=15)
    search1.insert(0, 'Enter Product ID')
    search1.bind("<FocusIn>", lambda args: search1.delete('0', 'end'))
    search1.place(x=99, y=62, width=200)

    quantity = Entry(Title, textvariable=QUANTITY,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
    quantity.bind("<FocusIn>", lambda args: quantity.delete('0', 'end'))
    quantity.place(x=90, y=138, width=200)

    total = Entry(Title, textvariable=TOTAL,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
    total.place(x=90, y=285, width=200)

    amountGiven = Entry(Title, textvariable=AMOUNT_GIVEN,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
    amountGiven.bind("<FocusIn>", lambda args: amountGiven.delete('0', 'end'))
    amountGiven.place(x=90, y=380, width=200)

    balance = Entry(Title, textvariable=BALANCE,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
    balance.place(x=90, y=469, width=200)

    # ============Buttons==================
    addToCartBtnImage = ImageTk.PhotoImage(file='images\\addToCart.png')
    addToCartBtn = Button(Title,image=addToCartBtnImage, command=addToCart, relief=FLAT, bg="white", activebackground="white", borderwidth=0, cursor="hand2")
    addToCartBtn.image = addToCartBtnImage
    addToCartBtn.place(x=90, y=177)

    calculateBtnImage = ImageTk.PhotoImage(file='images\\calculate.png')
    calculateBtn = Button(Title,image=calculateBtnImage, command=calculateChange, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
    calculateBtn.image = calculateBtnImage
    calculateBtn.place(x=305, y=335)

    generateBtnImage = ImageTk.PhotoImage(file='images\\generateBill.png')
    generateBtn = Button(Title,image=generateBtnImage, command=GenerateBill, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
    generateBtn.image = generateBtnImage
    generateBtn.place(x=90, y=520)

    # ============Product List==============
    scrollbarx = Scrollbar(productListFrame, orient=HORIZONTAL)
    scrollbary = Scrollbar(productListFrame, orient=VERTICAL)
    tree1 = ttk.Treeview(productListFrame, columns=("ProductID", "Product Name", "Product Qty","hide", "Selling Price"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    tree1.heading('ProductID', text="ProductID",anchor=W)
    tree1.heading('Product Name', text="Name",anchor=W)
    tree1.heading('Product Qty', text="Quantity",anchor=W)
    tree1.heading('hide', text="hide",anchor=W)
    tree1.heading('Selling Price', text="Price",anchor=W)

    tree1.column('#0', stretch=NO, minwidth=0, width=0)
    tree1.column('#1', stretch=NO, minwidth=0, width=100)
    tree1.column('#2', stretch=NO, minwidth=0, width=250)
    tree1.column('#3', stretch=NO, minwidth=0, width=80)
    tree1.column("#4", stretch=NO, minwidth=0, width=0)
    tree1.column('#5', stretch=NO, minwidth=0, width=80)
    tree1.pack()
    DisplayProductList()

     # ===========getting date and time=============
    now = datetime.now()  
    dateLabel.configure(text=now.strftime("Date:%d-%m-%Y \t Time:%H:%M:%S"))

#window for transaction window
def transactions():
    global transactions
    global tree2
    PRODUCT_NAME.set("")
    PRODUCT_PRICE.set("")
    PRODUCT_QTY.set("")
    TOTAL.set("")
    transactions = Toplevel()
    transactions.title("TRANSACTIONS")
    transactions.geometry("1336x720+75+50")
    transactions.resizable(False, False)
    transactions.iconbitmap("images\\ucoe.ico")
    Title = Frame(transactions, bd=0, relief=SOLID)
    Title.pack(pady=0)

    transactionFrame = Frame(transactions, width=850, height=620)
    transactionFrame.place(x=410, y=0)

    # ===========Background Image===========
    image = ImageTk.PhotoImage(file='images\home.png')
    background = Label(Title, image=image)
    background.image = image
    background.pack(fill='both', expand='yes')

    #===========Buttons====================
    searchBtnImage = ImageTk.PhotoImage(file='images\search.png')
    searchBtn = Button(Title,image=searchBtnImage, command=SearchTransaction, relief=FLAT, bg="white", activebackground="white", borderwidth=0, cursor="hand2")
    searchBtn.image = searchBtnImage
    searchBtn.place(x=110, y=108)

    deleteBtnImage = ImageTk.PhotoImage(file='images\delete.png')
    deleteBtn = Button(Title,image=deleteBtnImage, command=DeleteTransaction, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
    deleteBtn.image = deleteBtnImage
    deleteBtn.place(x=110, y=178)

    updateBtnImage = ImageTk.PhotoImage(file='images\\update.png')
    updateBtn = Button(Title,image=updateBtnImage, command=updateTransactionPage, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
    updateBtn.image = updateBtnImage
    updateBtn.place(x=110, y=248)

    resetBtnImage = ImageTk.PhotoImage(file='images\\reset.png')
    resetBtn = Button(Title,image=resetBtnImage, command=Reset2, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
    resetBtn.image = resetBtnImage
    resetBtn.place(x=110, y=388)

    # =============Inputs=================
    search = Entry(Title, textvariable=SEARCH,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 15, "bold"), width=15)
    search.insert(0, 'Search')
    search.bind("<FocusIn>", lambda args: search.delete('0', 'end'))
    search.place(x=99, y=62, width=200)

    # ============Displaying Transaction ID=========
    scrollbarx = Scrollbar(transactionFrame, orient=HORIZONTAL)
    scrollbary = Scrollbar(transactions, orient=VERTICAL)
    scrollbary.pack(side="right", fill='x')
    tree2 = ttk.Treeview(transactionFrame, columns=("Transaction ID", "Product Name", "Product Qty", "Price", "Total", "space"), selectmode="browse", height=100, yscrollcommand=scrollbarx.set, xscrollcommand=scrollbary.set)
    tree2.heading('Transaction ID', text="Transaction ID",anchor=W)
    tree2.heading('Product Name', text="Product Name",anchor=W)
    tree2.heading('Product Qty', text="Quantity",anchor=W)
    tree2.heading('Price', text="Price", anchor=W)
    tree2.heading('Total', text="Total",anchor=W)
    tree2.heading('space', text="",anchor=W)

    tree2.column('#0', stretch=NO, minwidth=0, width=0)
    tree2.column('#1', stretch=NO, minwidth=0, width=100)
    tree2.column('#2', stretch=NO, minwidth=0, width=200)
    tree2.column('#3', stretch=NO, minwidth=0, width=120)
    tree2.column('#4', stretch=NO, minwidth=0, width=120)
    tree2.column('#5', stretch=NO, minwidth=0, width=120)
    tree2.column('#6', stretch=NO, minwidth=0, width=600)

    tree2.pack()
    DisplayTransactionData()

#window for sales window
def sales():
    global sales
    global tree3
    sales = Toplevel()
    sales.title("SALES")
    sales.geometry("500x720+75+50")
    sales.resizable(False, False)
    sales.iconbitmap("images\\ucoe.ico")

    scrollbarx = Scrollbar(sales, orient=HORIZONTAL)
    scrollbary = Scrollbar(sales, orient=VERTICAL)
    tree3 = ttk.Treeview(sales, columns=("ProductID", "Product Name", "Product Qty", "Total Profit"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    tree3.heading('ProductID', text="ProductID",anchor=W)
    tree3.heading('Product Name', text="Product Name",anchor=W)
    tree3.heading('Product Qty', text="Quantity",anchor=W)
    tree3.heading('Total Profit', text="Total Profit",anchor=W)

    tree3.column('#0', stretch=NO, minwidth=0, width=0)
    tree3.column('#1', stretch=NO, minwidth=0, width=100)
    tree3.column('#2', stretch=NO, minwidth=0, width=200)
    tree3.column('#3', stretch=NO, minwidth=0, width=120)
    tree3.column('#4', stretch=NO, minwidth=0, width=120)
    tree3.pack()
    DisplaySalesData()

#window for Inventory Management
def Home():
    global Home
    global tree
    global productQty
    SEARCH.set("")
    Home = Toplevel()
    Home.title("MANAGE INVENTORY")
    Home.geometry("1366x720+75+50")
    Home.resizable(False, False)
    Home.iconbitmap("images\\ucoe.ico")
    Title = Frame(Home, bd=0, relief=SOLID)
    Title.pack(pady=0)

    productFrame = Frame(Home, width=850, height=620)
    productFrame.place(x=427, y=0)

    # ===========Background Image===========
    frame1 = ImageTk.PhotoImage(file='images\home.png')
    image_panel = Label(Title, image=frame1)
    image_panel.image = frame1
    image_panel.pack(fill='both', expand='yes')

    #===========Buttons====================
    searchBtnImage = ImageTk.PhotoImage(file='images\search.png')
    searchBtn = Button(Title,image=searchBtnImage, command=Search, relief=FLAT, bg="white", activebackground="white", borderwidth=0, cursor="hand2")
    searchBtn.image = searchBtnImage
    searchBtn.place(x=110, y=108)

    deleteBtnImage = ImageTk.PhotoImage(file='images\delete.png')
    deleteBtn = Button(Title,image=deleteBtnImage, command=Delete, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
    deleteBtn.image = deleteBtnImage
    deleteBtn.place(x=110, y=198)

    updateBtnImage = ImageTk.PhotoImage(file='images\\update.png')
    updateBtn = Button(Title,image=updateBtnImage, command=updateProductPage, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
    updateBtn.image = updateBtnImage
    updateBtn.place(x=110, y=288)

    newProductBtnImage = ImageTk.PhotoImage(file='images\\addProduct.png')
    newProductBtn = Button(Title,image=newProductBtnImage, command=ShowAddNew, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
    newProductBtn.image = newProductBtnImage
    newProductBtn.place(x=110, y=378)

    resetBtnImage = ImageTk.PhotoImage(file='images\\reset.png')
    resetBtn = Button(Title,image=resetBtnImage, command=Reset, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
    resetBtn.image = resetBtnImage
    resetBtn.place(x=110, y=468)

    # =============Inputs=================
    search = Entry(Title, textvariable=SEARCH,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 15, "bold"), width=15)
    search.insert(0, 'Search')
    search.bind("<FocusIn>", lambda args: search.delete('0', 'end'))
    search.place(x=99, y=62, width=200)

    #==============Display Inventory===============
    scrollbarx = Scrollbar(productFrame, orient=HORIZONTAL)
    scrollbary = Scrollbar(productFrame, orient=VERTICAL)
    tree = ttk.Treeview(productFrame, columns=("ProductID", "Product Name", "Product Qty", "Product Price", "Selling Price"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    tree.heading('ProductID', text="ProductID",anchor=W)
    tree.heading('Product Name', text="Product Name",anchor=W)
    tree.heading('Product Qty', text="Quantity",anchor=W)
    tree.heading('Product Price', text="Cost Price",anchor=W)
    tree.heading('Selling Price', text="Sell Price",anchor=W)

    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=100)
    tree.column('#2', stretch=NO, minwidth=0, width=200)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=120)
    tree.column('#5', stretch=NO, minwidth=0, width=450)
    tree.pack()
    DisplayData()

#window for updating product window
def updateProductPage():
    if not tree.selection():
       tkMessageBox.showinfo("Inventory System","Please Select A Product From List", icon="warning")
    else:
        global updatePage
        updatePage = Toplevel()
        updatePage.title("Update Product Details")
        updatePage.geometry("600x720+75+50")
        updatePage.resizable(0, 0)
        updatePage.iconbitmap("images\\ucoe.ico")

        
        
        # ===========Background Image===========
        frame = ImageTk.PhotoImage(file='images\\updatePage.png')
        image_panel = Label(updatePage, image=frame)
        image_panel.image = frame
        image_panel.pack(fill='both', expand='yes')

        # ===========Labels And Inputs============
        heading = Label(updatePage,text = "PRODUCT DETAILS",font=("yu gothic ui", 18, "bold"), bg= "white", fg = "black" )
        heading.place(x=200, y=60, width = 210)

        productName_label = Label(updatePage,text = "PRODUCT NAME",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
        productName_label.place(x=115, y=105, width = 200)
        name = Entry(updatePage, textvariable=PRODUCT_NAME,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
        name.place(x=150, y=140, width=300)

        productQt_label = Label(updatePage,text = "PRODUCT QUANTITY",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
        productQt_label.place(x=130, y=230, width = 200)
        qty = Entry(updatePage, textvariable=PRODUCT_QTY,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
        qty.place(x=150, y=263, width=200)

        productPrice_label = Label(updatePage,text = "COST PRICE",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
        productPrice_label.place(x=90, y=350, width = 200)
        price = Entry(updatePage, textvariable=PRODUCT_PRICE,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
        price.place(x=150, y=385, width=200)

        sellPrice_label = Label(updatePage,text = "SELL PRICE",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
        sellPrice_label.place(x=90, y=475, width = 200)
        sellprice = Entry(updatePage, textvariable=PRODUCT_SELL_PRICE,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
        sellprice.place(x=150, y=505, width=200)
        
        # ==========placing the data into input fields============
        Database()
        curItem = tree.focus()
        contents =(tree.item(curItem))
        selecteditem = contents['values']
        PRODUCT_NAME.set(selecteditem[1])
        PRODUCT_QTY.set(selecteditem[2])
        PRODUCT_PRICE.set(selecteditem[3])
        PRODUCT_SELL_PRICE.set(selecteditem[4])

        # ============Button==================
        saveBtnImage = ImageTk.PhotoImage(file='images\\save.png')
        saveBtn = Button(updatePage,image=saveBtnImage, command=update, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
        saveBtn.image = saveBtnImage
        saveBtn.place(x=170, y=550)

#window for updating transaction window
def updateTransactionPage():
    if not tree2.selection():
        tkMessageBox.showinfo("Inventory System","Please Select A Transaction From The List", icon="warning")
    else:
        global transactionPage
        transactionPage = Toplevel()
        transactionPage.title("Update Transaction Details")
        transactionPage.geometry("600x720+75+50")
        transactionPage.resizable(0, 0)
        transactionPage.iconbitmap("images\\ucoe.ico")

        
        # ===========Background Image===========
        frame = ImageTk.PhotoImage(file='images\\updatePage.png')
        image_panel = Label(transactionPage, image=frame)
        image_panel.image = frame
        image_panel.pack(fill='both', expand='yes')

        # ===========Labels And Inputs============
        heading = Label(transactionPage,text = "TRANSACTION DETAILS",font=("yu gothic ui", 18, "bold"), bg= "white", fg = "black" )
        heading.place(x=150, y=60, width = 310)

        productName_label = Label(transactionPage,text = "PRODUCT NAME",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
        productName_label.place(x=115, y=105, width = 200)
        name = Entry(transactionPage, textvariable=PRODUCT_NAME,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
        name.place(x=150, y=140, width=300)

        productQt_label = Label(transactionPage,text = "PRODUCT QUANTITY",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
        productQt_label.place(x=130, y=230, width = 200)
        qty = Entry(transactionPage, textvariable=PRODUCT_QTY,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
        qty.place(x=150, y=263, width=200)

        productPrice_label = Label(transactionPage,text = "PRICE",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
        productPrice_label.place(x=120, y=350, width = 100)
        price = Entry(transactionPage, textvariable=PRODUCT_PRICE,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
        price.place(x=150, y=385, width=200)

        sellPrice_label = Label(transactionPage,text = "TOTAL AMOUNT",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
        sellPrice_label.place(x=110, y=475, width = 200)
        sellprice = Entry(transactionPage, textvariable=TOTAL,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 12, "bold"), width=15)
        sellprice.place(x=150, y=505, width=200)
        
        # ==========placing the data into input fields============
        Database()
        curItem = tree2.focus()
        contents =(tree2.item(curItem))
        selecteditem = contents['values']
        PRODUCT_NAME.set(selecteditem[1])
        PRODUCT_QTY.set(selecteditem[2])
        PRODUCT_PRICE.set(selecteditem[3])
        TOTAL.set(selecteditem[4])

        # ============Button==================
        saveBtnImage = ImageTk.PhotoImage(file='images\\save.png')
        saveBtn = Button(transactionPage,image=saveBtnImage, command=updateTransaction, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
        saveBtn.image = saveBtnImage
        saveBtn.place(x=170, y=550)

#updating Products Details on DataBase
def update():
    if not tree.selection():
       tkMessageBox.showinfo("Inventory System","Please Select A Product From List", icon="warning")
    else:
        Database()
        curItem = tree.focus()
        contents =(tree.item(curItem))
        selecteditem = contents['values']
        cursor.execute("UPDATE `product` SET `product_name`='{}' WHERE `product_id`={}".format(str(PRODUCT_NAME.get()), selecteditem[0]))
        cursor.execute("UPDATE `product` SET `product_qty`='{}' WHERE `product_id`={}".format(int(PRODUCT_QTY.get()), selecteditem[0]))
        cursor.execute("UPDATE `product` SET `product_price`='{}' WHERE `product_id`={}".format(int(PRODUCT_PRICE.get()), selecteditem[0]))
        cursor.execute("UPDATE `product` SET `product_selling_price`='{}' WHERE `product_id`={}".format(int(PRODUCT_SELL_PRICE.get()), selecteditem[0]))
        conn.commit()
        cursor.close()
        updatePage.destroy()
        Reset()

#updating transaction Details on DataBase
def updateTransaction():
    if not tree2.selection():
       tkMessageBox.showinfo("Inventory System","Please Select A Transaction From List", icon="warning")
    else:
        Database()
        curItem = tree2.focus()
        contents =(tree2.item(curItem))
        selecteditem = contents['values']
        cursor.execute("UPDATE `transactions` SET `product_name`='{}' WHERE `transaction_id`={}".format(str(PRODUCT_NAME.get()), selecteditem[0]))
        cursor.execute("UPDATE `transactions` SET `product_qty`='{}' WHERE `transaction_id`={}".format(int(PRODUCT_QTY.get()), selecteditem[0]))
        cursor.execute("UPDATE `transactions` SET `product_price`='{}' WHERE `transaction_id`={}".format(int(PRODUCT_PRICE.get()), selecteditem[0]))
        cursor.execute("UPDATE `transactions` SET `total_amount`='{}' WHERE `transaction_id`={}".format(int(TOTAL.get()), selecteditem[0]))
        conn.commit()
        cursor.close()
        transactionPage.destroy()
        Reset2()

#for logout
def Logout():
    result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to logout?', icon="warning") #messageBox to confirm logout
    if result == 'yes': 
        admin_id = ""
        root.deiconify()
        Home1.destroy()
 
# ===============LOGO======================
root.iconbitmap("images\\ucoe.ico")

titleTxt = "INVENTORY MANAGEMENT" #text for heading
heading = Label(root, text=titleTxt,font=("yu gothic ui", 25, BOLD),bg= "white", fg = "orange",bd = 5,relief = FLAT)
heading.place(x = 458, y =58, width = 458)
Slider() #Writing Animation

# ===========Labels And Input============
username_label = Label(root,text = "Username",font=("yu gothic ui", 14, "bold"), bg= "white", fg = "#9d9d9d" )
username_label.place(x=467, y=180, width = 100)
username = Entry(root, textvariable=USERNAME,relief=FLAT, bg="white",fg= "black",  font=("yu gothic ui", 15, "bold"), width=15)
username.place(x=515, y=215, width=200)

password_label = Label(root,text = "Password",font=("yu gothic ui", 14, "bold"), bg= "white",  fg = "#9d9d9d" )
password_label.place(x=467, y=310, width=100)
password = Entry(root, textvariable=PASSWORD,relief=FLAT, bg="white",fg= "black",   font=("yu gothic ui", 15, "bold"), width=15, show="*")
password.place(x=515, y=340, width=200)

# ============Buttons===================
loginBtnImage = ImageTk.PhotoImage(file='images\loginBtn.png') #Login 
loginBtn = Button(root,command=Login, image=loginBtnImage, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
loginBtn.place(x=600, y=450)

exitBtnImage = ImageTk.PhotoImage(file='images\exit.png') #Exit Application
exitBtn = Button(root,command=Exit, image=exitBtnImage, relief=FLAT,bg="white",activebackground="white", borderwidth=0, cursor="hand2")
exitBtn.place(x=600, y=510)

warnTxt = Label(root, text="",font=("yu gothic ui", 14, "bold"), bg= "white",  fg = "red", relief=FLAT) #Shows Warings if user enters wrong info
warnTxt.place(x = 458, y =390, width = 458)
 




if __name__ == "__main__":   #MainLoop
    root.mainloop()