from tkinter import *
from tkinter import font
import tkinter as tk
from tkinter import messagebox
import psycopg2
from datetime import *
from datetime import date 
import math
from tkinter import ttk
from PIL import ImageTk,Image
from tkcalendar import *
import sys
import babel.numbers
import traceback
from fpdf import FPDF,HTMLMixin
from ttkwidgets.autocomplete import AutocompleteEntry
import os.path
import os
from dotenv import load_dotenv 


product_list=[]
product_price=[]
product_part=[]
product_quantity=[]
product_unit=[]
product_sales=[]
product_cost_sale=[]
product_capital=[]
product_profit=[]
product_Tprofit=[]
stocks =[]
product_mode=[]

class index:
    def database(self, *args, **kwargs):
        conn=psycopg2.connect(database="shop_inventory",user="postgres",password="M",host="localhost",)
        cur = conn.cursor()
        return conn, cur

    def __init__(self,master,*args, **kwargs):
        
        self.master =master
        self.up =Frame(master,width=1400,height=360,bg='#bdbdbd')
        self.up.pack(side=TOP)
        self.up2 =Frame(self.up,width=1400,height=360,bg='#bdbdbd')
        self.up2.pack(side=TOP)

        self.w1=LabelFrame(master,bg='steelblue')
        
        self.mcanvas=Canvas(self.w1,bg='steelblue',width=1386)
        self.mcanvas.place(rely=0.25)

        self.bottom=Frame(self.mcanvas,width=1386,height=100000,bg='steelblue')
    
        self.sc=ttk.Scrollbar(self.w1,orient="vertical",command=self.mcanvas.yview)
        self.sc.place(relx=1,rely=0,relheight=1, anchor='ne')
        self.mcanvas.configure(yscrollcommand=self.sc.set)
        self.mcanvas.bind('<Configure>',lambda e:self.mcanvas.configure(scrollregion = self.mcanvas.bbox("all")))
        self.mcanvas.bind_all('<MouseWheel>',self.OnWheel)
        self.mcanvas.create_window((0,0),window=self.bottom,anchor="nw")
        self.w1.pack(fill="both",expand="yes",padx=1,side=BOTTOM)
        self.heading1=Label(self.up2,text="Shop Management System",font=('Mochiy Pop P One' ,20 ,'bold'),bg='#bdbdbd' )
        self.heading1.place(x=500,y=0)
        self.Sbt= Button(self.up2,text="close Todays sales" ,height=1,width=25,font=('arial',10,'bold'),bg='steelblue', fg="white" ,command=self.close_sale).place(x=1060,y=40)
        today =date.today()
        self.date_home=Label(self.w1,text="Date: " + str(today),font=('arial' ,18 ,'bold'),bg='steelblue',fg='black')
        self.date_home.place(x=0,y=20)
        self.tcomodity=Label(self.w1,text='Commodity',font=('arial' ,15 ,'bold'),bg='steelblue',fg='white')
        self.tcomodity.place(x=15,y=50)
        self.tparticular=Label(self.w1,text='Particulars',font=('arial' ,15 ,'bold'),bg='steelblue',fg='white')
        self.tparticular.place(x=180,y=50)
        self.tQuantity=Label(self.w1,text='Quantity',font=('arial' ,15 ,'bold'),bg='steelblue',fg='white')
        self.tQuantity.place(x=300,y=50)
        self.tUnitPrice=Label(self.w1,text='Unit Price',font=('arial' ,15 ,'bold'),bg='steelblue',fg='white')
        self.tUnitPrice.place(x=400,y=50)
        self.tSales=Label(self.w1,text='Amount',font=('arial' ,15 ,'bold'),bg='steelblue',fg='white')
        self.tSales.place(x=520,y=50)
        self.tCostOfsale=Label(self.w1,text='Cost of sales',font=('arial' ,15 ,'bold'),bg='steelblue',fg='white')
        self.tCostOfsale.place(x=625,y=50)
        self.tCapital=Label(self.w1,text='Capital',font=('arial' ,15 ,'bold'),bg='steelblue',fg='white')
        self.tCapital.place(x=790,y=50)
        self.Profit=Label(self.w1,text='Profit',font=('arial' ,15 ,'bold'),bg='steelblue',fg='white')
        self.Profit.place(x=910,y=50)
        self.tProfit=Label(self.w1,text='Total Profit',font=('arial' ,15 ,'bold'),bg='steelblue',fg='white')
        self.tProfit.place(x=1000,y=50)
        self.tProfit=Label(self.w1,text='Mode',font=('arial' ,15 ,'bold'),bg='steelblue',fg='white')
        self.tProfit.place(x=1150,y=50)
        # self.img1= ImageTk.PhotoImage(Image.open("image/open.png"))
        # self.bt2 =Button(master,image=self.img1,command=self.menuM,border=0,bg='#262626', activebackground='#262626').place(x=5,y=5)
        # particulars
        # self.sele = Label(self.up,text="Select Particulars: ",font=('arial',13,'bold'),bg="#bdbdbd")
        # self.sele.place(x=600,y=50)
        
       
        # self.purchaseChoosen=ttk.Combobox(self.up,width=35,textvariable=self.n)
        # self.purchaseChoosen['values'] =('sales','purchase','withdrawal','Additional')
        # self.purchaseChoosen.place(x=600,y=50)
        # self.purchaseChoosen['state']='readonly'
        # self.chos=self.purchaseChoosen.current()
        # self.purchaseChoosen.bind('<<ComboboxSelected>>',self.select_part)

        self.salebtn=Button(self.up2,width=20,height=1,text="Sale",font=('arial',10,'bold'),bg='steelblue',fg='white',command=self.selectsale)
        self.salebtn.place(x=190,y=40)
        self.purbtn=Button(self.up2,width=20,height=1,text="Purchase",font=('arial',10,'bold'),bg='steelblue',fg='white',command=self.selectpur)
        self.purbtn.place(x=410,y=40)
        self.withbtn=Button(self.up2,width=20,height=1,text="Withdrawal",font=('arial',10,'bold'),bg='steelblue',fg='white',command=self.selectwid)
        self.withbtn.place(x=630,y=40)
        self.addbtn=Button(self.up2,width=20,height=1,text="Additional",font=('arial',10,'bold'),bg='steelblue',fg='white',command=self.selectadd)
        self.addbtn.place(x=850,y=40)
        self.n=StringVar()

        self.f1=Frame(self.up2,width=180,height=360,bg="#bdbdbd")
        self.f1.place(x=0,y=0)
        # self.img_1 = ImageTk.PhotoImage(Image.open("image/shop.ico"))
        
        # self.l.place(x=0,y=0)
        # self.canvas1= Canvas(self.f1, width= 10, height= 10)
        # self.canvas1.place(x=0,y=10)
        # self.img= (Image.open("image/shop.ico"))
        # self.resized_image= self.img.resize((100,80), Image.ANTIALIAS)
        # self.new_image= ImageTk.PhotoImage(self.resized_image)
        # self.l=Label(self.f1,image=self.new_image)
        # self.l.place(x=37,y=2)
        self.btn4=Button(self.f1,width=20,height=2,text="Home",font=('arial',10,'bold'),bg='steelblue',fg='white',command=self.dishome)
        self.btn4.place(x=0,y=100)
        self.btn5=Button(self.f1,width=20,height=2,text="Inventory",font=('arial',10,'bold'),bg='steelblue',fg='white',command=self.display_update)
        self.btn5.place(x=0,y=150)
        self.btn6=Button(self.f1,width=20,height=2,text="Report",font=('arial',10,'bold'),bg='steelblue',fg='white',command=self.reports_done)
        self.btn6.place(x=0,y=200)
    def OnWheel(self, event):
        self.mcanvas.yview("scroll",event.delta,"units")
        return "break"
    def selectsale(self, *args, **kwargs):
        try:
            self.n='sales'
        finally:
            self.select_part()
    def selectpur(self, *args, **kwargs):
        try:
            self.n='purchase'
        finally:
            self.select_part()
    def selectadd(self, *args, **kwargs):
        try:
            self.n='Additional'
        finally:
            self.select_part()
    def selectwid(self, *args, **kwargs):
        try:
            self.n='withdrawal'
        finally:
            self.select_part()

    def select_part(self, *args, **kwargs):
        self.particular=self.n
        if self.n == "sales":
            conn,cur = self.database()
            autocom=[]
            cur.execute('SELECT * FROM testinventory')  
            result = cur.fetchall()
            conn.commit()
            for self.r in result:
                autocom.append(self.r[1])
        
            self.FrameComodity=Frame(self.up2,width=1100,height=360,bg='#bdbdbd')
            self.FrameComodity.place(x=180,y=75)
            # search
            self.name_search = Label(self.FrameComodity,text="Search :",font=('arial',13 ,'bold'),bg='#bdbdbd')
            self.name_search.place(x=14,y=10)
            self.input_search =AutocompleteEntry(self.FrameComodity,font=('arial',13,'bold'),width=29,completevalues=autocom)
            self.input_search.place(x=110,y=10)

            self.Sbt= Button(self.FrameComodity,text="Search" ,width=32,font=('arial',10,'bold'),bg='steelblue', fg="white" ,command=self.search)
            self.Sbt.place(x=110,y=40) 

            self.salesHeading=Label(self.FrameComodity,text="Commodity:",font=('arial' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.salesHeading.place(x=14,y=80)
            self.displaycom=Label(self.FrameComodity,text=" ",font=('arial' ,12,'bold') ,fg='black',bg='#bdbdbd')
            self.displaycom.place(x=110,y=80)
            
            self.add_cart = Button(self.FrameComodity,text="Sale" ,width=32,bg='steelblue',font=('arial',10,'bold'), fg="white" ,command=self.sale_btn)
            self.add_cart.place(x=110,y=215)

            self.quantityL = Label(self.FrameComodity,text="Quantity  :",font=('arial',12,'bold'),fg='black',bg='#bdbdbd')
            self.quantityL.place(x=14,y=180)
            self.input_quantity =Entry(self.FrameComodity,width=29,font=('arial',12,'bold'))
            self.input_quantity.place(x=110,y=180)
            self.input_quantity.focus()
            self.input_quantity.insert(END,'')

            self.h7=Label(self.FrameComodity,text="in_stock:",font=('arial' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.h7.place(x=365,y=80)
            self.dk=Label(self.FrameComodity,text="",font=('Mochiy Pop P One' ,12 ,'bold') ,fg='black',bg='#bdbdbd')            
            self.dk.place(x=440,y=80) 

            self.heading7=Label(self.FrameComodity,text="price:",font=('arial' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.heading7.place(x=250,y=80)
            self.displayUprice=Label(self.FrameComodity,text="",font=('arial' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.displayUprice.place(x=300,y=80)

            window.bind('<Return>',self.search)
            window.bind('<space>',self.sale_btn)
    
            
            try:
                self.destroy_pur()
                self.destroy_with()
            except:
                pass
        elif self.n =="purchase":

            conn,cur = self.database()
            autocom=[]
            cur.execute('SELECT * FROM testinventory')  
            result = cur.fetchall()
            conn.commit()
            for self.r in result:
                autocom.append(self.r[1])
            # search
            self.FramePur=Frame(self.up2,width=1100,height=360,bg='#bdbdbd')
            self.FramePur.place(x=180,y=75)

            self.name_searchP= Label(self.FramePur,text="Search:",font=('arial',13 ,'bold'),bg='#bdbdbd')
            self.name_searchP.place(x=30,y=10)
            self.input_searchP = AutocompleteEntry(self.FramePur,font=('arial',13,'bold'),width=29,completevalues=autocom)
            self.input_searchP.place(x=150,y=10)
            self.btP=Button(self.FramePur,text="Search" ,font=('arial',10,'bold'),width=32,bg='steelblue', fg="white" ,command=self.searchupdate)
            self.btP.place(x=150,y=40) 
            self.heading7=Label(self.FramePur,text="Commodity:",font=('arial' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.heading7.place(x=30,y=80)
            self.heading8=Label(self.FramePur,text="stock:",font=('arial' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.heading8.place(x=30,y=110)
            self.heading9=Label(self.FramePur,text="cost of sale:",font=('arial' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.heading9.place(x=30,y=140) 
            self.heading2=Label(self.FramePur,text="Retail price :",font=('arial' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.heading2.place(x=30,y=170) #
            self.wh_1 = Label(self.FramePur,text="Wholesale:",font=('arial ',12,' bold'),bg='#bdbdbd').place(x=30,y=200)
            self.dispcom=Label(self.FramePur,text="",font=('Mochiy Pop P One' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.dispcom.place(x=150,y=80)
            self.heading7=Label(self.FramePur,text="in_stock:",font=('arial' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.heading7.place(x=340,y=80)
            self.dispstock=Label(self.FramePur,text=" ",font=('Mochiy Pop P One' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.dispstock.place(x=420,y=80) 
            
            self.input_stock = Entry(self.FramePur,font=('arial',12,'bold'),width=30)
            self.input_stock.place(x=150,y=110)
            self.input_wh = Entry(self.FramePur,font=('arial',12,'bold'),width=30)
            self.input_wh.place(x=150,y=200)
            self.input_cost = Entry(self.FramePur,font=('arial',12,'bold'),width=30)
            self.input_cost.place(x=150,y=140) 
            self.input_sp= Entry(self.FramePur,font=('arial',12,'bold'),width=30)
            self.input_sp.place(x=150,y=170)#

            self.purbtn = Button(self.FramePur,text="purchase" ,width=33,bg='steelblue',font=('arial',10,'bold'), fg="white" ,command=self.sale_btn)
            self.purbtn.place(x=150,y=230)
            try:
                self.destroy_sa()
                self.destroy_with()
            except:
                pass
            window.bind('<Return>',self.searchupdate)
            window.bind('<space>',self.sale_btn)
        elif self.n== "withdrawal":
            self.Framewith=Frame(self.up2,width=1100,height=360,bg='#bdbdbd')
            self.Framewith.place(x=180,y=75)
            self.enterAmount=Label(self.Framewith,text="Enter Amount :",font=('arial' ,12,'bold') ,fg='black',bg='#bdbdbd')
            self.enterAmount.place(x=320,y=10)
            self.input_enterAmount = Entry(self.Framewith,font=('arial',12,'bold'),width=25)
            self.input_enterAmount.place(x=450,y=10)
            self.withbtn = Button(self.Framewith,text="withdraw" ,width=28,bg='steelblue',font=('arial',10,'bold'), fg="white" ,command=self.sale_btn)
            self.withbtn.place(x=450,y=50)
            
            try:
                self.destroy_sa()
                self.destroy_pur()
            except:
                pass
            window.bind('<Return>',self.sale_btn)
        elif self.n=='Additional':
            self.upown=Frame(self.up2,width=1100,height=360,bg='#bdbdbd')
            self.upown.place(x=180,y=75)
            self.enterAmount=Label(self.upown,text="Enter Amount :",font=('arial' ,12,'bold') ,fg='black',bg='#bdbdbd')
            self.enterAmount.place(x=320,y=10)
            self.inputenterAmount = Entry(self.upown,font=('arial',12,'bold'),width=25)
            self.inputenterAmount.place(x=450,y=10)
            self.add_btn = Button(self.upown,text="Add Capital" ,width=28,bg='steelblue',font=('arial',10,'bold'), fg="white" ,command=self.sale_btn)
            self.add_btn.place(x=450,y=50)
            window.bind('<Return>',self.sale_btn)
        elif self.n=='sale_own':
            conn,cur = self.database()
            autocom=[]
            cur.execute('SELECT * FROM testinventory')  
            result = cur.fetchall()
            conn.commit()
            for self.r in result:
                autocom.append(self.r[1])
            self.upown=Frame(self.up2,width=1100,height=360,bg='#bdbdbd')
            self.upown.place(x=180,y=75)
            self.nasearch = Label(self.upown,text="Search :",font=('arial',13 ,'bold'),bg='#bdbdbd')
            self.nasearch.place(x=500,y=10) 
            self.input_search = AutocompleteEntry(self.upown,font=('arial',13,'bold'),width=25,completevalues=autocom)
            self.input_search.place(x=570,y=10)
            self.Sbt= Button(self.upown,text="Search" ,width=30,bg='steelblue', fg="black" ,command=self.search)
            self.Sbt.place(x=610,y=50) 
            self.salesHeading=Label(self.upown,text="Commodity:",font=('arial' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.salesHeading.place(x=15,y=5)
            self.displaycom=Label(self.upown,text=" ",font=('arial' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.displaycom.place(x=110,y=5)
            self.heading7=Label(self.upown,text="price:",font=('arial' ,12,'bold') ,fg='black',bg='#bdbdbd')
            self.heading7.place(x=300,y=5)
            self.displayUprice=Label(self.upown,text=" ",font=('arial' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.displayUprice.place(x=350,y=5)
            self.add_cart = Button(self.upown,text="Sale" ,width=40,bg='yellow',font=('arial',10,'bold'), fg="black" ,command=self.sale_btn)
            self.add_cart.place(x=300,y=180)
            self.quantityL = Label(self.upown,text="Quantity:",font=('arial',12,'bold'),fg='black',bg='#bdbdbd')
            self.quantityL.place(x=15,y=95)
            self.input_quantity =Entry(self.upown,width=15,font=('arial',12,'bold'))
            self.input_quantity.place(x=150,y=95)
            self.input_quantity.focus()
            self.input_quantity.insert(END,'')
            self.h7=Label(self.upown,text="in_stock:",font=('arial' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.h7.place(x=400,y=95)
            self.dk=Label(self.upown,text=" ",font=('Mochiy Pop P One' ,12 ,'bold') ,fg='black',bg='#bdbdbd')
            self.dk.place(x=475,y=95) 
            

    def destroy_with(self,*args, **kwargs):
        self.Framewith.destroy()
    def destroy_pur(self,*args, **kwargs):
        self.FramePur.destroy()
    def destroy_sa(self,*args, **kwargs):
        self.FrameComodity.destroy()
    def searchupdate(self,*args, **kwargs):
        conn,cur = self.database()
        self.seach_name= str(self.input_searchP.get()).lower()
        cur.execute('SELECT * FROM testinventory where comodity = %s',(self.seach_name,))
        result = cur.fetchall()
        conn.commit()
        if cur.rowcount ==0:
            messagebox.showinfo('error',"commodity not in the inventory")
            self.input_searchP.delete(0,END)  
        else:
            try:
                for r in result:
                    self.n0=r[0]
                    self.n1=r[1]
                    self.n2=r[2]
                    self.n3=r[3]
                    self.n4=r[4]
                    self.n5=r[5]
                    self.n6=r[8]
                    self.n7=r[9]
                
                self.pId=self.n0
                self.dispcom.configure(text=str(self.n1))
                self.dispstock.configure(text=str(self.n2))
                self.input_stock.delete(0,END)
                self.input_stock.insert(END,0)
                self.input_cost.delete(0,END)
                self.input_cost.insert(0,str(self.n3))
                self.input_sp.delete(0,END)
                self.input_sp.insert(0,str(self.n4))
                self.input_wh.delete(0,END)
                self.input_wh.insert(0,str(self.n7))
            except Exception as error:   
                conn.rollback()
                print(traceback.format_exc())
    
    def search(self,*args, **kwargs):
        conn,cur = self.database()
        try:
            self.comodity = self.input_search.get().lower()
            cur.execute('SELECT * FROM testinventory where comodity = %s',(self.comodity,))
            result = cur.fetchall()
            conn.commit()
            if cur.rowcount ==0:
                messagebox.showinfo('error',"commodity not in the inventory")
                self.input_search.delete(0,END)  
            else:
                for self.r in result:
                    self.id=self.r[0]
                    self.comodity_get=self.r[1]
                    self.Csales=self.r[3]
                    self.retail=self.r[4] 
                    self.stock=self.r[2]
                    self.wholesale=self.r[9]
    
            self.displayUprice.configure(text=str(self.retail))
            self.displaycom.configure(text=str(self.comodity_get))
            self.dk.configure(text=str(self.stock))
            self.pay_mode = "cash"
            
        except Exception as e:
            print(e)
            conn.rollback()
            print(traceback.format_exc())
        finally:
            if self.n=='sales':
                self.sele2 = Label(self.FrameComodity,text="price: ",font=('arial',12,'bold'),bg="#bdbdbd")
                self.sele2.place(x=14,y=110)
                self.p=StringVar()
                self.priceChoosen=ttk.Combobox(self.FrameComodity,width=27,textvariable=self.p,font=('arial',12,'bold'))
                self.priceChoosen['values'] =('retail','wholesale')
                self.priceChoosen.place(x=110,y=110)
                self.priceChoosen['state']='readonly'
                self.priceChoosen.current(0)
                self.priceChoosen.bind('<<ComboboxSelected>>',self.select_work)
                
                self.sele2 = Label(self.FrameComodity,text="Mode: ",font=('arial',12,'bold'),bg="#bdbdbd")
                self.sele2.place(x=14,y=145)
                self.c=StringVar()
                self.modeChoosen=ttk.Combobox(self.FrameComodity,width=27,textvariable=self.c,font=('arial',12,'bold'))
                self.modeChoosen['values'] =('Cash','Mpesa')
                self.modeChoosen.place(x=110,y=145)
                self.modeChoosen['state']='readonly'
                self.modeChoosen.current(0)
                self.modeChoosen.bind('<<ComboboxSelected>>',self.select_mode)
            elif self.n=='sale_own':
                self.sele3 = Label(self.upown,text="Price: ",font=('arial',12,'bold'),bg="#bdbdbd")
                self.sele3.place(x=20,y=50)
                self.p=StringVar()
                self.priceChoosen=ttk.Combobox(self.upown,width=35,textvariable=self.p,font=('arial',10,'bold'))
                self.priceChoosen['values'] =('retail','wholesale')
                self.priceChoosen.place(x=150,y=50)
                self.priceChoosen['state']='readonly'
                self.priceChoosen.current()
                self.priceChoosen.bind('<<ComboboxSelected>>',self.select_work)

                self.sele6 = Label(self.upown,text="Mode: ",font=('arial',12,'bold'),bg="#bdbdbd")
                self.sele6.place(x=20,y=145)
                self.c=StringVar()
                self.modeChoosen=ttk.Combobox(self.upown,width=35,textvariable=self.c,font=('arial',10,'bold'))
                self.modeChoosen['values'] =('Cash','Mpesa')
                self.modeChoosen.place(x=150,y=145)
                self.modeChoosen['state']='readonly'
                self.modeChoosen.current()
                self.modeChoosen.bind('<<ComboboxSelected>>',self.select_mode)
    def select_mode(self,*args, **kwargs):
        self.mode =self.c.get()
        if self.mode == 'Cash':
            self.pay_mode = "cash"
        elif self.mode == 'Mpesa':
            self.pay_mode ='mpesa'
                
    def select_work(self,*args, **kwargs):
        try:
            self.prices=self.p.get()
            if self.prices=='retail':
                conn,cur = self.database()
                cur.execute('SELECT * FROM testinventory where comodity = %s',(self.comodity,))
                result = cur.fetchall()
                conn.commit()
                for self.r in result:
                    self.id=self.r[0]
                    self.retail=self.r[4]
                    self.wholesale=self.r[9]
                self.displayUprice.configure(text=str(self.retail))
            elif self.prices=='wholesale':
                conn,cur = self.database()
                cur.execute('SELECT * FROM testinventory where comodity = %s',(self.comodity,))
                result = cur.fetchall()
                conn.commit()
                for self.r in result:
                    self.id=self.r[0]
                    self.retail=self.r[4]
                    self.wholesale=self.r[9]
                self.displayUprice.configure(text=str(self.wholesale)) 
        except Exception as e :
            messagebox.showinfo('error', 'search before selecting price !!!')
            print(e)
            print(traceback.format_exc())
         
        
#sp ndio unit ndio retail
# cos ndio Cos
    def sale_btn(self,*args, **kwargs):
        try:
            self.particulars=self.n
            if self.particulars == "sales":
                try:
                    conn,cur = self.database()
                    self.prices=self.p.get()
                    self.quantity_value = float(self.input_quantity.get())
                    if self.quantity_value > float(self.stock):
                        messagebox.showinfo('error',"stock is empty")
                        try:
                            cur.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 1')  
                            conn.commit()
                            result = cur.fetchall()
                            self.pay_mode =0
                            for self.r in result:
                                self.fcapital=self.r[7]
                                self.tprofit=self.r[9]
                            self.Tcapital = float(self.fcapital)
                            self.comodity_get='-'
                            self.quantity_value=0
                            self.price=0
                            self.sales=0
                            self.Csales=0
                            self.profit=0
                            self.Tprofit=float(self.tprofit)
                            self.particular=0
                        except Exception as e:
                            print(e)
                        self.priceChoosen.destroy()
                        self.modeChoosen.destroy()
                        self.input_search.delete(0,END)
                        self.input_quantity.delete(0,END)
                        self.displayUprice.configure(text='0')
                        self.dk.configure(text='0')
                    else:
                        if self.prices == 'retail':
                            self.final_price = float(self.quantity_value)*float(self.retail)
                            self.price=self.retail
                            self.sales=float(self.quantity_value)*float(self.retail)
                            self.original=float(self.Csales)*float(self.quantity_value)
                            self.profit=float(self.sales)-float(self.original)
                            self.Capital=float( self.sales)-float(self.profit)
                            self.stocks = float(self.stock) -float(self.quantity_value)
                            self.Tcapital=self.Capital
                            self.Csales=float(self.Csales)*float(self.quantity_value)
                            cur.execute("UPDATE testinventory SET stock=%s WHERE id=%s",(self.stocks,self.id))
                            conn.commit()
                            cur.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 1')  
                            result = cur.fetchall()
                            conn.commit()
                            self.tprofit=0
                            self.fcapital=0
                            for self.r in result:
                                self.fcapital=self.r[7]
                                self.tprofit=self.r[9]
                            self.Tprofit=float(self.profit)+float(self.tprofit)
                            self.Tcapital = float(self.Capital) + float(self.fcapital)
                        elif self.prices=='wholesale':
                            conn,cur = self.database()
                            self.final_price = float(self.quantity_value)*float(self.wholesale)
                            self.price=self.wholesale
                            self.sales=float(self.quantity_value)*float(self.wholesale)
                            self.original=float(self.Csales)*float(self.quantity_value)
                            self.profit=float(self.sales)-float(self.original)
                            self.Csales=float(self.Csales)*float(self.quantity_value)
                            self.Capital=float( self.sales)-float(self.profit)
                            self.stocks = float(self.stock) -float(self.quantity_value)
                            self.Tcapital=self.Capital
                            cur.execute("UPDATE testinventory SET stock=%s WHERE id=%s",(self.stocks,self.id))
                            conn.commit() 
                            cur.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 1')  
                            result = cur.fetchall()
                            conn.commit()
                            self.tprofit=0
                            self.fcapital=0
                            for self.r in result:
                                self.fcapital=self.r[7]
                                self.tprofit=self.r[9]
                            self.Tprofit=float(self.profit)+float(self.tprofit)
                            self.Tcapital = float(self.Capital) + float(self.fcapital)
                        self.particular='sales'
                        self.priceChoosen.destroy()
                        self.modeChoosen.destroy()
                        self.input_search.delete(0,END)
                        self.input_quantity.delete(0,END)
                        self.displayUprice.configure(text='0')
                        self.dk.configure(text='0')
                except:
                    pass
            elif self.particulars == "withdrawal":
                try: 
                    conn,cur = self.database()
                    cur.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 1')  
                    conn.commit()
                    result = cur.fetchall()
                    self.tprofit=0
                    self.pay_mode =0
                    self.fcapital=0
                    for self.r in result:
                        self.fcapital=self.r[7]
                        self.tprofit=self.r[9]
                    self.amount =self.input_enterAmount.get()
                    self.Tcapital = float(self.fcapital)-float(self.amount)
                    self.comodity_get='-'
                    self.quantity_value =0
                    self.particular ="withdrawal"
                    self.price=0
                    self.sales=float(self.amount)
                    self.Csales=0
                    self.profit=0
                    self.Tprofit=self.tprofit
                except:
                    pass
                self.input_enterAmount.delete(0,END)
            elif self.particulars == "purchase":
                conn,cur = self.database()
                try:
                    self.id=self.pId
                    self.stock=self.input_stock.get()
                    self.cost=self.input_cost.get()
                    self.whP=self.input_wh.get()
                    self.sp=self.input_sp.get()
                    self.pay_mode =0
                    
                    self.totalcost=float(self.cost)*float(self.stock)
                    self.totalsp=float(self.sp)*float(self.stock)
                    self.capital=float(self.totalcost)
                    self.profit=float(self.totalsp)-float(self.capital) 
                    
                    try:
                        cur.execute('SELECT * FROM testinventory where id=%s',(self.id,))  
                        result = cur.fetchall()
                        for self.r in result:
                            self.fstock=self.r[2]
                        self.stockdb =float(self.stock)+float(self.fstock)
                        cur.execute("UPDATE testinventory SET stock=%s,cost=%s,sp=%s,capital=%s,profit=%s,wholesale=%s WHERE id=%s",(self.stockdb,self.cost,self.sp,self.capital,self.profit,self.whP,self.id))
                        conn.commit()
                    except Exception as e:
                        print(traceback.format_exc())
                    
                    cur.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 1')
                    conn.commit()  
                    result = cur.fetchall()
                    self.tprofit=0
                    self.fcapital=0
                    for self.r in result:
                        self.fcapital=self.r[7]
                        self.tprofit=self.r[9]
                        
                    self.Tcapital = float(self.fcapital)-float(self.capital)
                    self.comodity_get=self.seach_name
                    self.quantity_value =self.stock
                    self.price=self.sp
                    self.sales=self.totalcost
                    self.Csales=self.cost
                    self.particular='purchase'
                    self.profit=0
                    self.Tprofit=self.tprofit
                except:
                    pass
                self.input_stock.delete(0,END)
                self.input_searchP.delete(0,END)
                
            elif self.particulars =="Additional":
                try:
                    conn,cur = self.database()
                    cur.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 1')  
                    conn.commit()
                    result = cur.fetchall()
                    self.tprofit=0
                    self.pay_mode =0
                    self.fcapital=0
                    for self.r in result:
                        self.fcapital=self.r[7]
                        self.tprofit=self.r[9]
                    self.amount =self.inputenterAmount.get()
                    self.Tcapital = float(self.fcapital)+float(self.amount)
                    self.comodity_get='-'
                    self.quantity_value =0
                    self.price=0
                    self.sales=float(self.amount)
                    self.Csales=0
                    self.profit=0
                    self.Tprofit=self.tprofit
                    self.particular='Additional'
                    
                except :
                    pass
                self.inputenterAmount.delete(0,END)
    
            # elif self.particulars =="sale_own":
            #     conn,cur = self.database()
            #     self.prices=self.p.get()
            #     self.quantity_value = float(self.input_quantity.get())
            #     if self.quantity_value > float(self.stock):
            #         messagebox.showinfo('error',"stock is  not enough or empty")
            #         try:
            #             cur.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 1')  
            #             result = cur.fetchall()
            #             conn.commit()
            #             self.pay_mode =0
            #             for self.r in result:
            #                 self.fcapital=self.r[7]
            #                 self.tprofit=self.r[9]
            #             self.Tcapital = float(self.fcapital)
            #             self.comodity_get='-'
            #             self.quantity_value=0
            #             self.price=0
            #             self.sales=0
            #             self.Csales=0
            #             self.profit=0
            #             self.Tprofit=self.tprofit
            #         except Exception as e:
            #             print(e)

            #     else:
            #         if self.prices == 'retail':
            #             self.final_price = float(self.quantity_value)*float(self.retail)
            #             self.price=self.retail
            #             self.sales=float(self.quantity_value)*float(self.retail)
            #             self.original=float(self.Csales)*float(self.quantity_value)
            #             self.profit=float(self.sales)
            #             self.Capital=float( self.sales)-float(self.profit)
            #             self.stocks = float(self.stock) -float(self.quantity_value)
            #             self.Tcapital=self.Capital
            #             cur.execute("UPDATE testinventory SET stock=%s WHERE id=%s",(self.stocks,self.id))
            #             conn.commit() 
            #             cur.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 1 ')  
            #             result = cur.fetchall()
            #             conn.commit()
            #             self.tprofit=0
            #             self.fcapital=0
            #             for self.r in result:
            #                 self.fcapital=self.r[7]
            #                 self.tprofit=self.r[9]
            #             self.Tprofit=float(self.profit)+float(self.tprofit)
            #             self.Tcapital = float(self.fcapital)
            #             self.particular ='sales'
            #         elif self.prices=='wholesale':
            #             self.final_price = float(self.quantity_value)*float(self.wholesale)
            #             self.price=self.wholesale
            #             self.sales=float(self.quantity_value)*float(self.wholesale)
            #             self.original=float(self.Csales)*float(self.quantity_value)
            #             self.profit=float(self.sales)
            #             self.stocks = float(self.stock) -float(self.quantity_value)
            #             cur.execute("UPDATE testinventory SET stock=%s WHERE id=%s",(self.stocks,self.id))
            #             conn.commit() 
            #             cur.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 1 ')  
            #             result = cur.fetchall()
            #             conn.commit()

            #             self.tprofit=0
            #             self.fcapital=0
            #             for self.r in result:
            #                 self.fcapital=self.r[7]
            #                 self.tprofit=self.r[9]
            #             self.Tprofit=float(self.profit)+float(self.tprofit)
            #             self.Tcapital =  float(self.fcapital)
            #             self.particular ='sales'
            #         self.priceChoosen.destroy()
            #         self.modeChoosen.destroy()
            #         self.input_search.delete(0,END)
                    
            else:
                print("error")              
        except Exception as e:
            print(traceback.format_exc())
            print("error"   ,e)

        finally:
            if self.particular != 0:
                try:
                    product_list.append(self.comodity_get)
                    product_quantity.append(self.quantity_value)
                    product_unit.append(self.price)
                    product_sales.append(self.sales)
                    product_cost_sale.append(self.Csales)
                    product_capital.append(self.Tcapital) 
                    product_profit.append(self.profit)
                    product_Tprofit.append(self.Tprofit)
                    product_part.append(self.particular)
                    product_mode.append(self.pay_mode)
                    self.y_index=0
                    self.counter=0
                    
                    for self.p in product_list:    
                        self.tempname= Label(self.bottom, text=str(product_list[self.counter]),font=('arial',15,'bold'),bg='steelblue')
                        self.tempname.place(x=10,y= self.y_index)
                        self.tempcomodity =product_list[self.counter]
                        self.temppart= Label(self.bottom, text=str(product_part[self.counter]),font=('arial',15,'bold'),bg='steelblue')
                        self.temppart.place(x=180,y= self.y_index)
                        self.tempparts= product_part[self.counter]
                        self.tempqua= Label(self.bottom, text=str(product_quantity[self.counter]),font=('arial',18,'bold'),bg='steelblue')
                        self.tempqua.place(x=310,y= self.y_index)
                        self.tempquat =product_quantity[self.counter]
                        self.tempunit= Label(self.bottom, text=str(product_unit[self.counter]),font=('arial',18,'bold'),bg='steelblue')
                        self.tempunit.place(x=410,y= self.y_index)
                        self.tempunitp =product_unit[self.counter]
                        self.tempsales= Label(self.bottom, text=str(product_sales[self.counter]),font=('arial',18,'bold'),bg='steelblue')
                        self.tempsales.place(x=525,y= self.y_index)
                        self.tempsale=product_sales[self.counter]
                        self.tempCostsales= Label(self.bottom, text=str(product_cost_sale[self.counter]),font=('arial',18,'bold'),bg='steelblue')
                        self.tempCostsales.place(x=650,y= self.y_index)
                        self.tempCostsale=product_cost_sale[self.counter]
                        self.tempcapital= Label(self.bottom, text=str(product_capital[self.counter]),font=('arial',18,'bold'),bg='steelblue')
                        self.tempcapital.place(x=790,y= self.y_index)
                        self.tempcapitals=product_capital[self.counter]

                        self.tempCprofit= Label(self.bottom, text=str(product_profit[self.counter]),font=('arial',18,'bold'),bg='steelblue')
                        self.tempCprofit.place(x=910,y= self.y_index)
                        self.tempCprofits=product_profit[self.counter]
                        self.tempTprofit= Label(self.bottom, text=str(product_Tprofit[self.counter]),font=('arial',18,'bold'),bg='steelblue')
                        self.tempTprofit.place(x=1010,y= self.y_index)
                        self.tempTprofits=product_Tprofit[self.counter]

                        self.tempmode= Label(self.bottom, text=str(product_mode[self.counter]),font=('arial',18,'bold'),bg='steelblue')
                        self.tempmode.place(x=1140,y= self.y_index)
                        self.tempmodes=str(product_mode[self.counter])

                        self.y_index +=40
                        self.counter +=1
                    today =date.today()  
                    self.monthlpy=0
                    cur.execute("INSERT INTO transactions (comodity,particulars,quantity,unitprice,sales,costofsales,capital,cprofit,tprofit,date,year,month,mode,monthlyp) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.comodity_get ,self.particular,self.quantity_value,self.price,self.sales,self.Csales,self.Tcapital, self.profit,self.Tprofit,today,today.year,today.month,self.pay_mode,self.monthlpy,))
                    conn.commit() 
                    self.particular=0
                except Exception as e :
                    conn.rollback()
                    print(e)
                    print(traceback.format_exc())
            else:
                pass
            conn.close()
            self.particular=0
    def close_sale(self,*args, **kwargs):
        conn,cur = self.database()
        try:
            cur.execute('SELECT * FROM transactions ')  
            result = cur.fetchall()
            conn.commit()
            self.tprofit=0
            for self.r in result:
                self.fcapital=self.r[7]
                self.T_profit=self.r[9]
            self.Tcapital = self.fcapital
            self.prof=self.T_profit
            self.comodity='close'
            self.quantity ='-'
            self.particulars='-'
            self.unitprice='-'
            self.sales='-'
            self.Csales='-'
            self.profit=0
            self.Tprofit=0
            self.mode=0
            today =date.today()  
            cur.execute("INSERT INTO transactions (comodity,particulars,quantity,unitprice,sales,costofsales,capital,cprofit,tprofit,date,year,month,mode,monthlyp) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.comodity ,self.particulars,self.quantity,self.unitprice,self.sales,self.Csales,self.Tcapital,self.profit, self.Tprofit,today,today.year,today.month,self.mode,self.prof,))
            conn.commit()
        except Exception as e :
            conn.rollback()
            print(traceback.format_exc())
            print(e)
        finally:
            self.mss=messagebox.askquestion('close sales',"Do you really want to close sales ",icon="warning")
            if self.mss =='yes':
              window.destroy()
            else:
                print("Not closed")
        conn.close()
                
                    
                    
    
    # def menuM(self,*args,**kwargs):
        
    def dele(self,*args,**kwargs):
        # self.f1.destroy()
        try:
            self.updat_e.destroy()
            self.upAdd.destroy()  
        except:
            pass
    def destroy_report(self,*args,**kwargs):
        self.upAdd.destroy()
    def destroy_stock (self,*args,**kwargs):
            self.top.destroy()
    def  destroy_update(self,*args,**kwargs):
        self.updat_e.destroy()
    def destroy_add_own(self,*args, **kwargs):
        self.Addown.destroy()
    def destroy_addd_own(self,*args, **kwargs):
        self.upAdd.destroy()
    def destroy_update_own(self,*args, **kwargs):
        self.updel.destroy()
    def destroy_most_own(self,*args,**kwargs):
        self.mostS.destroy()
    def destroy_repo(self,*args,**kwargs):
        self.report.destroy()

    def reports_done(self,*args,**kwargs):
        self.upAdd=Frame(self.up,width=1100,height=360,bg='#bdbdbd')
        self.upAdd.place(x=180,y=34)
        self.img3= ImageTk.PhotoImage(Image.open("image/back.png"))
        self.bt26 =Button(self.upAdd,image=self.img3,border=0,command=self.destroy_report,bg='steelblue',activebackground='#12c4c0')
        self.bt26.place(x=10,y=0)
        self.btn8=Button(self.upAdd,width=42,height=2,font=('arial',10,'bold'),text="Best selling commodity",bg='steelblue',fg='white',command=self.diplay_most_Selling)
        self.btn8.place(x=700,y=100)
        self.btn6=Button(self.upAdd,width=42,height=2,font=('arial',10,'bold'),text="shop records",bg='steelblue',fg='white',command=self.display_report)
        self.btn6.place(x=200,y=100)
        # self.f1.destroy()

    def selected_stock(self,*args, **kwargs):
        # self.tree.selection_set(self.tree.tag_has(self.inputS.get()))
        conn,cur = self.database()
        if self.inputS.get() !="":
            self.tree.delete(*self.tree.get_children())
            cur.execute('SELECT comodity,stock,cost,sp,wholesale FROM testinventory WHERE comodity=%s',(self.inputS.get(),))
            self.result = cur.fetchall()
            conn.commit
            self.couns=1
            for r in self.result:
                self.tree.insert('',END,iid=r[0],values=(self.couns,r[0],r[1],r[2],r[3],r[4]),tags=r[0])
                self.couns +=1    
            cur.close()
    def stock_display(self,*args,**kwargs):
        conn,cur = self.database()
        autocom=[]
        cur.execute('SELECT * FROM testinventory')  
        result = cur.fetchall()
        conn.commit()
        for self.r in result:
            autocom.append(self.r[1])

        self.top=Frame(self.up,width=1100,height=360,bg='#bdbdbd')
        self.top.place(x=180,y=34)

        self.img4 = ImageTk.PhotoImage(Image.open("image/back.png"))
        self.bt20 =Button(self.top,image=self.img4,border=0,command=self.destroy_stock,bg='steelblue',activebackground='#12c4c0')
        self.bt20.place(x=10,y=0)
        self.y=Label(self.top, text= "Items in the Inventory", font=('arial', 15,' bold'),bg='#bdbdbd')
        self.y.place(x=50,y=50)
        self.print_stock = Button(self.top,text="Get pdf of Items" ,width=20,bg='steelblue',font=('arial',10,'bold'), fg="white" ,command=self.print_stock_F)
        self.print_stock.place(x=900,y=50)
        self.lbd =Label(self.top,text="Search :",font=('arial',10,'bold'))
        self.lbd.place(x=300,y=50)
        self.inputS=AutocompleteEntry(self.top,font=('arial',10,'bold'),width=20,completevalues=autocom)
        self.inputS.place(x=370,y=50)
        self.search_stock = Button(self.top,text="search",width=20,bg='steelblue',font=('arial',9,'bold'), fg="white" ,command=self.selected_stock)
        self.search_stock.place(x=520,y=50)
        self.columns = ('rank','comodity','stock','cost','sp','wholesale') 
        self.tree = ttk.Treeview(self.top,height=11, columns=self.columns, show='headings')
        self.tree.heading('rank',text='No.')
        self.tree.column('rank',stretch=NO,width=30)
        self.tree.heading('comodity',text='commodity')
        self.tree.heading('stock',text='stock')
        self.tree.heading('cost' ,text='costofsale')
        self.tree.heading('sp',text='retail')
        self.tree.heading('wholesale',text='wholesale')
        window.bind('<Return>',self.selected_stock)
        try:
            cur.execute('SELECT comodity,stock,cost,sp,wholesale FROM testinventory ')
            self.results = cur.fetchall()
            conn.commit()
            self.counter=1
            
            for r in self.results:
                self.tree.insert('',END,values=(self.counter,r[0],r[1],r[2],r[3],r[4]),tags=r[0]) 
                self.counter +=1 
        except Exception as e :
            print(e)
        self.tree.place(x=50,y=80)
        self.scrollbar = ttk.Scrollbar(self.top, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.place(x=1100,y=80,relheight=0.68, anchor='ne')
        conn.close()
    
    def  display_update(self,*args,**kwargs):
        self.updat_e=Frame(self.up,width=1100,height=360,bg='#bdbdbd')
        self.updat_e.place(x=180,y=34)

        self.img5 = ImageTk.PhotoImage(Image.open("image/back.png"))
        self.bt25 =Button(self.updat_e,image=self.img5,border=0,command=self.destroy_update,bg='steelblue',activebackground='#12c4c0')
        self.bt25.place(x=10,y=0)

        self.btn7=Button(self.updat_e,width=30,height=2,text="New Commodities ",font=('arial',10,'bold'),bg='steelblue',fg='white',command=self.add_new)
        self.btn7.place(x=20,y=100)
        self.btn3=Button(self.updat_e,width=30,height=2,text="Update stock",font=('arial',10,'bold'),bg='steelblue',fg='white',command=self.add_own)
        self.btn3.place(x=300,y=100)
        self.btn8=Button(self.updat_e,width=30,height=2,text="Delete commodity",font=('arial',10,'bold'),bg='steelblue',fg='white',command=self.diplay_delete)
        self.btn8.place(x=860,y=100)
        self.btn9=Button(self.updat_e,width=30,height=2,text="Stock records",font=('arial',10,'bold'),bg='steelblue',fg='white',command=self.stock_display)
        self.btn9.place(x=580,y=100)
        
    def dishome(self,*args,**kwargs): 
        try:
            # self.f1.destroy()
            # self.updat_e.destroy()
            # self.upAdd.destroy()
            # self.mostS.destroy()
            # self.top.destroy()
            # self.updel.destroy()
            # self.reports_done.destroy()
            # self.display_update.destroy()
            # self.own_comodity.destroy() 
            # self.add_new.destroy()   
            # self.Addown.destroy()   
            self.up2.tkraise()
        except:
            pass   
    def add_new(self,*args,**kwargs):
        # self.f1.destroy()
        try:
            self.upAdd=Frame(self.up,width=1100,height=360,bg='#bdbdbd')
            self.upAdd.place(x=180,y=34)   
            self.img6 = ImageTk.PhotoImage(Image.open("image/back.png"))
            self.bt20 =Button(self.upAdd,image=self.img6,border=0,command=self.destroy_addd_own,bg='steelblue',activebackground='#12c4c0')
            self.bt20.place(x=10,y=0)
            # self.heading=Label(self.upAdd,text="Add New commodity",font=('arial 20 bold'),fg='black',bg='#bdbdbd')
            # self.heading.place(x=350,y=10)
            self.name_1 = Label(self.upAdd,text="Comodity:",font=('arial 12 bold'),bg='#bdbdbd')
            self.name_1.place(x=20,y=70)
            self.stock_1 = Label(self.upAdd,text="stock:",font=('arial 12 bold'),bg='#bdbdbd')
            self.stock_1.place(x=20,y=110)
            self.retail_1= Label(self.upAdd,text="Retail:",font=('arial 12 bold'),bg='#bdbdbd')
            self.retail_1.place(x=20,y=150)
            self.wholesale = Label(self.upAdd,text="wholesale:",font=('arial 12 bold'),bg='#bdbdbd')
            self.wholesale.place(x=20,y=190)  
            self.Cos= Label(self.upAdd,text="Cost of Sale:",font=('arial 12 bold'),bg='#bdbdbd')
            self.Cos.place(x=20,y=230)

            self.input_Cos = Entry(self.upAdd,font=('arial',12,'bold'),width=29)
            self.input_Cos.place(x=120,y=230) 

            self.input_retail = Entry(self.upAdd,font=('arial',12,'bold'),width=29)
            self.input_retail.place(x=120,y=150) 
            self.input_stock = Entry(self.upAdd,font=('arial',12,'bold'),width=29)
            self.input_stock.place(x=120,y=110) 
            self.input_wholesale = Entry(self.upAdd,font=('arial',12,'bold'),width=29)
            self.input_wholesale.place(x=120,y=190) 
            self.input_Comodity = Entry(self.upAdd,font=('arial',12,'bold'),width=29)
            self.input_Comodity.place(x=120,y=70) 
            self.bt=Button(self.upAdd,text="Add new commodity" ,font=('arial',10,'bold'),width=32,bg='steelblue', fg="white" ,command=self.get_input)
            self.bt.place(x=120,y=270)
            # self.bt=Button(self.upAdd,text="Refresh" ,width=25,bg='steelblue', fg="white" ,command=self.clear_all)
            # self.bt.place(x=50,y=290)
            self.tBox=Text(self.upAdd,width=40,height=15)
            self.tBox.place(x=700,y=50)
            self.input_stock.insert(END,0)
        except Exception as e :
             print(traceback.format_exc())
    def get_input(self,*args, **kwargs):
        conn,cur = self.database()
        self.comodity=self.input_Comodity.get().lower()
        self.stock=self.input_stock.get()
        self.cost=self.input_retail.get()
        self.wholesale=self.input_wholesale.get()
        self.Cos=self.input_Cos.get()
      #cost for selling the comodities
        if self.comodity=='':
            messagebox.showinfo("Error","Please Fill in all the fields")
        else:
            try:
                cur.execute("INSERT INTO testinventory (comodity,stock,sp,cost,wholesale) values (%s,%s,%s,%s,%s)",(self.comodity,self.stock,self.cost,self.Cos,self.wholesale))    
                conn.commit()
                self.tBox.insert(END,"\n\n Add commodity:  "+ str(self.comodity))
                
            except Exception as e:
                conn.rollback()
                print(traceback.format_exc())
                messagebox.showinfo("Error","Comodity All ready in store !!")
        conn.close()
    def clear_all(self,*args, **kwargs):
         self.input_Comodity.delete(0,END)
    
    
    def add_own (self,*args,**kwargs):
        conn,cur = self.database()
        autocom=[]
        cur.execute('SELECT * FROM testinventory')  
        result = cur.fetchall()
        conn.commit()
        for self.r in result:
            autocom.append(self.r[1])

        self.Addown=Frame(self.up,width=1100,height=360,bg='#bdbdbd')
        self.Addown.place(x=180,y=34)
        
        self.img7 = ImageTk.PhotoImage(Image.open("image/back.png"))
        self.bt20 =Button(self.Addown,image=self.img7,border=0,command=self.destroy_add_own,bg='steelblue',activebackground='#12c4c0')
        self.bt20.place(x=10,y=0)

        # (if no cost of sale type ' 0 'at cost of sale)

        
        self.name_search = Label(self.Addown,text="Search :",font=('arial',13 ,'bold'),bg='#bdbdbd')
        self.name_search.place(x=20,y=35)
        self.input_search_own = AutocompleteEntry(self.Addown,font=('arial',13,'bold'),width=29,completevalues=autocom)
        self.input_search_own.place(x=120,y=35)
        self.Sbt= Button(self.Addown,text="Search" ,font=('arial',10,'bold'),width=32,bg='steelblue', fg="white" ,command=self.search_own)
        self.Sbt.place(x=120,y=70) 
        self.comU=Label(self.Addown,text="Comidity:",font=('arial ',12,' bold'),bg='#bdbdbd')
        self.comU.place(x=20,y=100)
        self.disownpcom=Label(self.Addown,text=" ",font=('arial ',12,' bold'),bg='#bdbdbd')
        self.disownpcom.place(x=120,y=100)
        self.disto=Label(self.Addown,text="in_stock:",font=('arial ',12,' bold'),bg='#bdbdbd')
        self.disto.place(x=350,y=100)
        self.disownpsto=Label(self.Addown,text=" ",font=('arial ',12,' bold'),bg='#bdbdbd')
        self.disownpsto.place(x=430,y=100)
        self.stock_1 = Label(self.Addown,text="stock:",font=('arial ',12,' bold'),bg='#bdbdbd')
        self.stock_1.place(x=20,y=130)
        self.retail_1= Label(self.Addown,text="Retail:",font=('arial ',12,' bold'),bg='#bdbdbd')
        self.retail_1.place(x=20,y=165)
        self.wholesale = Label(self.Addown,text="wholesale:",font=('arial ',12,' bold'),bg='#bdbdbd')
        self.wholesale.place(x=20,y=200)  
        self.Cos= Label(self.Addown,text="Cost of Sale:",font=('arial ',12,' bold'),bg='#bdbdbd')
        self.Cos.place(x=20,y=235)
        self.input_Cost = Entry(self.Addown,font=('arial ',12,'bold'),width=29)
        self.input_Cost.place(x=120,y=235) 
        self.input_retail = Entry(self.Addown,font=('arial',12,'bold'),width=29)
        self.input_retail.place(x=120,y=165) 
        self.input_stock = Entry(self.Addown,font=('arial',12,'bold'),width=29)
        self.input_stock.place(x=120,y=130) 
        self.input_wholesale = Entry(self.Addown,font=('arial',12,'bold'),width=29)
        self.input_wholesale.place(x=120,y=200) 
        self.bt=Button(self.Addown,text="Update" ,font=('arial',10,'bold'),width=32,bg='steelblue', fg="white" ,command=self.get_own_input)
        self.bt.place(x=120,y=280)
        # self.bt=Button(self.Addown,text="Refresh" ,width=25,bg='steelblue', fg="white" ,command=self.clear_own_all)
        # self.bt.place(x=50,y=280)
        self.tBox=Text(self.Addown,width=40,height=15)
        self.tBox.place(x=700,y=50)
        window.bind('<Return>',self.search_own)
    def get_own_input(self,*args, **kwargs):
        conn,cur = self.database()
        try:
            self.updat_e.destroy()
            self.comodity=self.input_search_own.get().lower()
            self.stock=self.input_stock.get()
            self.wholesale=self.input_wholesale.get()
            self.sp=self.input_retail.get()
            self.cos=self.input_Cost.get()
            
            self.vendor="own"
            self.vendorContact="own"
            cur.execute('SELECT * FROM testinventory where comodity=%s',(self.comodity,))  
            result = cur.fetchall()
            if cur.rowcount ==0:
                messagebox.showinfo('error',"commodity not in the inventory")
                self.input_search.delete(0,END)  
            else:
                for self.r in result:
                    self.fstock=self.r[2]
                self.stockd =float(self.stock)+float(self.fstock)
                cur.execute("UPDATE testinventory SET stock=%s,cost=%s,sp=%s,vendor=%s,vendorphone=%s,wholesale=%s WHERE comodity=%s",(self.stockd,self.cos,self.sp,self.vendor,self.vendorContact,self.wholesale,self.comodity,))
                conn.commit()
                self.tBox.insert(END,"\n\n Updated commodity:  "+ str(self.comodity))
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            messagebox.showinfo("Error","Error durring update of stock")
        self.input_Cost.delete(0,END)
        self.input_retail.delete(0,END)
        self.input_stock.delete(0,END)
        self.input_wholesale.delete(0,END)
        conn.close()
    def search_own(self,*args, **kwargs):
        conn,cur = self.database()
        self.seach_name= str(self.input_search_own.get()).lower()
        cur.execute('SELECT * FROM testinventory where comodity = %s ',(self.seach_name,))
        try:
            result = cur.fetchall()
            for r in result:
                self.n1=r[1]
                self.n2=r[2]
                self.n3=r[3]
                self.n4=r[4]
                self.n7=r[9]
            conn.commit( )
            self.disownpcom.configure(text=str(self.n1))
            self.disownpsto.configure(text=str(self.n2))
            self.input_stock.delete(0,END)
            self.input_stock.insert(END,0)
            self.input_Cost.delete(0,END)
            self.input_Cost.insert(0,str(self.n3))
            self.input_retail.delete(0,END)
            self.input_retail.insert(0,str(self.n4))
            self.input_wholesale.delete(0,END)
            self.input_wholesale.insert(0,str(self.n7) ) 
        except Exception as error:
            messagebox.showwarning('danger',"No such Comodity in Database")
            print(traceback.format_exc())      
    
    def clear_own_all(self,*args, **kwargs):
         self.input_Comodity.delete(0,END)
         self.input_stock.delete(0,END)
         self.input_wholesale.delete(0,END)
         self.input_retail.delete(0,END)
    
    def selected_del(self,*args, **kwargs):
        conn,cur = self.database()
        if self.inputD.get() !="":
            self.trs.delete(*self.trs.get_children())
            cur.execute('SELECT id,comodity,stock,cost,sp,wholesale FROM testinventory WHERE comodity=%s',(self.inputD.get(),))
            self.result = cur.fetchall()
            conn.commit
            self.couns=1
            for r in self.result:
                self.trs.insert('',END,iid=r[0],values=(self.couns,r[1],r[2],r[3],r[4],r[5]),tags=r[1])
                self.couns +=1    
            cur.close()

        # self.trs.selection_set(self.trs.tag_has(self.inputD.get()))
        conn.close()

    def diplay_delete(self,*args,**kwargs):

        conn,cur = self.database()
        autocom=[]
        cur.execute('SELECT * FROM testinventory')  
        result = cur.fetchall()
        conn.commit()
        for self.r in result:
            autocom.append(self.r[1])
        
        self.updel=Frame(self.up,width=1100,height=360,bg='#bdbdbd')
        self.updel.place(x=180,y=34)
        self.img8 = ImageTk.PhotoImage(Image.open("image/back.png"))
        self.bt20 =Button(self.updel,image=self.img8,border=0,command=self.destroy_update_own,bg='steelblue',activebackground='#12c4c0')
        self.bt20.place(x=10,y=0)

        self.inputD=AutocompleteEntry(self.updel,font=('arial',13,'bold'),width=25,completevalues=autocom)
        self.inputD.place(x=420,y=50)
        self.search_del = Button(self.updel,text="search" ,width=20,bg='steelblue',font=('arial',10,'bold'), fg="white" ,command=self.selected_del)
        self.search_del.place(x=680,y=50)
        window.bind('<Return>',self.selected_del)
        self.DEl=Label(self.updel,text="Delete commodity from the Inventory",font=('Mochiy Pop P One' ,15,'bold'),bg='#bdbdbd' ).place(x=50,y=50)
        self.cols = ('rank','comodity','stock','cost','sp','wholesale')
        self.trs = ttk.Treeview(self.updel,height=11, columns=self.cols, show='headings')
        self.trs.heading('comodity',text='commodity')
        self.trs.column('comodity',stretch=NO,width=200)
        self.trs.heading('stock',text='stock')
        self.trs.column('stock',stretch=NO,width=200,anchor=CENTER)
        self.trs.heading('cost' ,text='costofsale')
        self.trs.column('cost',stretch=NO,width=200,anchor=CENTER)
        self.trs.heading('sp',text='retail')
        self.trs.column('sp',stretch=NO,width=200,anchor=CENTER)
        self.trs.heading('wholesale',text='wholesale')
        self.trs.column('wholesale',stretch=NO,width=200,anchor=CENTER)
        self.trs.heading('rank',text='No.')
        self.trs.column('rank',stretch=NO,width=30)
        try:
            cur.execute('SELECT id,comodity,stock,cost,sp,wholesale FROM testinventory ')
            self.result = cur.fetchall()
            conn.commit
            self.couns=1
            for r in self.result:
                self.trs.insert('',END,iid=r[0],values=(self.couns,r[1],r[2],r[3],r[4],r[5]),tags=r[1])
                self.couns +=1  
        except Exception as e :
            print(traceback.format_exc())
            print(e)
        self.trs.bind('<<TreeviewSelect>>', self.delete_selected)
        self.trs.place(x=50,y=80)
        self.scrol = ttk.Scrollbar(self.updel, orient=tk.VERTICAL, command=self.trs.yview)
        self.trs.configure(yscrol=self.scrol.set)
        self.scrol.place(x=1085,y=80,relheight=0.68, anchor='ne')
        
    def authdelete(self,*args,**kwargs):
        self.auth= Toplevel(window,bg="#bdbdbd")
        self.auth.geometry("400x100+500+200") 
        self.auth.title("Authenticate")
        self.ureport=Frame(self.auth,width=500,height=300,bg='#bdbdbd')
        self.ureport.place(x=50,y=0)
        self.bt38 =Button(self.auth,width=24,text="Delete",font=('arial',12,'bold'),command=self.del_sele,bg='steelblue',fg='white')
        self.bt38.place(x=120,y=60)
        self.La=Label(self.auth,font=('arial',12,'bold'),text="Password:",bg="#bdbdbd")
        self.La.place(x=10,y=25)
        self.input_pass = Entry(self.auth,font=('arial',12,'bold'),width=27,show="*")
        self.input_pass.place(x=120,y=25)
    def del_sele(self,*args,**kwargs):
        conn,cur = self.database()
        env_path=os.path.join('image','p.env')
        load_dotenv(env_path)
        cpass=os.getenv('pin')
        password = self.input_pass.get()
        if password == cpass:
            sql="DELETE FROM testinventory WHERE id=%s"
            r=cur.execute(sql,(self.id,))
            conn.commit()
            if(cur.rowcount == 1):
                self.trs.delete(self.id)
            self.auth.destroy()      
        else:
            messagebox.showinfo("error", "Password Mismatch",icon="warning")
        self.auth.destroy()
    def delete_selected(self,*args,**kwargs):
        conn,cur = self.database()
        if self.trs.selection():
            self.iid= self.trs.selection()[0]
            sql1="SELECT * FROM testinventory WHERE id=%s"
            cur.execute(sql1,(self.iid,))
            row= cur.fetchone()
            self.id=row[0]
            if row==None:
                print("error")
            else:
                self.authdelete()
        conn.close()
 
    def diplay_most_Selling(self,*args,**kwargs):
        conn,cur = self.database()
        self.mostS=Frame(self.up,width=1100,height=360,bg='#bdbdbd')
        self.mostS.place(x=180,y=34)
        self.img9 = ImageTk.PhotoImage(Image.open("image/back.png"))
        self.bt20 =Button(self.mostS,image=self.img9,border=0,command=self.destroy_most_own,bg='steelblue',activebackground='#12c4c0')
        self.bt20.place(x=10,y=0)
        self.most=Label(self.mostS,text="Best selling Commodity ",font=('Helvetica' ,15,'bold'),bg='#bdbdbd' )
        self.most.place(x=200,y=20)
        self.bt20 =Button(self.mostS,text="Get pdf Most Selling",font=('arial',10,'bold'),width=25,command=self.print_most,bg='steelblue',fg='white')
        self.bt20.place(x=550,y=20)
        # most selling 
        # print_most
        self.col = ('rank','comodity','quantity','profit')
        self.tres = ttk.Treeview(self.mostS, columns=self.col, show='headings')
        self.tres.heading('rank',text='No.')
        self.tres.column('rank',stretch=NO,width=30)
        self.tres.heading('comodity',text='commodity')
        self.tres.column('comodity',stretch=NO,width=250)
        self.tres.heading('quantity',text='Quantity')
        self.tres.column('quantity',stretch=NO,width=150,anchor=CENTER)
        self.tres.heading('profit',text='Profit')
        self.tres.column('profit',stretch=NO,width=150,anchor=CENTER)
        pat='sales'
        today =date.today()
        self.mon=today
        cur.execute(' SELECT comodity FROM  transactions WHERE particulars=%s AND date=%s GROUP BY comodity ORDER BY COUNT(comodity) DESC',(pat,self.mon,))
        self.result= cur.fetchall()
        conn.commit()
        if not self.result:
            messagebox.showinfo("no data", "Error")
        else:
            self.coun=1
            T=[]
            for self.re in self.result:
                cur.execute(' SELECT quantity FROM  transactions WHERE comodity=%s AND date=%s',(self.re,self.mon,))
                r =[i[0] for i in cur.fetchall()]
                conn.commit()
                for x in range(0,len(r)):  
                    r[x]=float(r[x])
                self.add = sum(r)
                cur.execute(' SELECT cprofit FROM  transactions WHERE comodity=%s AND date=%s',(self.re,self.mon,))
                t =[i[0] for i in cur.fetchall()]
                conn.commit()
                for x in range(0,len(t)):  
                    t[x]=float(t[x])
                self.add2 = sum(t)
                self.tres.insert('',END,values=(self.coun,self.re,self.add,self.add2))
                self.coun +=1
            self.tres.place(x=200,y=50)
            self.scrollbas = ttk.Scrollbar(self.mostS, orient=tk.VERTICAL, command=self.tres.yview)
            self.tres.configure(yscroll=self.scrollbas.set)
            self.scrollbas.place(x=800,y=50,relheight=0.63 ,anchor='ne')
    def select_job(self,*args,**kwargs):
        self.dt=self.t.get()
        if self.dt == "Daily":
            self.cal=Calendar(self.upreport,selectmode="day")
            self.cal.place(x=250,y=0)
            self.b=Button(self.upreport,text="fetch info",font=('arial',10,'bold'),command=self.fetch_day,bg="steelblue",fg="white").place(x=640,y=50)   
        elif self.dt =="Monthly":
            self.calM=Calendar(self.upreport,selectmode="day",date_pattern="mm-dd-y")
            self.calM.place(x=250,y=0)
            self.bu=Button(self.upreport,text="fetch info",font=('arial',10,'bold'),command=self.select_month,bg="steelblue",fg="white").place(x=640,y=50) 
  
    def  display_report(self,*args,**kwargs):
        self.report= Toplevel(window,bg="#bdbdbd")
        self.report.geometry("1280x658+50+30") 
        self.report.title("Report")
        self.upreport=Frame(self.report,width=1386,height=658,bg='#bdbdbd')
        self.upreport.place(x=50,y=40)
        self.img_1 = ImageTk.PhotoImage(Image.open("image/back.png"))
        self.bt20 =Button(self.upreport,image=self.img_1,border=0,command=self.destroy_repo,bg='steelblue',activebackground='#12c4c0')
        self.bt20.place(x=0,y=0)
        self.T_capital =Label(self.report,text="Total Capital: ",font=('Mochiy Pop P One' ,15,'bold'),bg='#bdbdbd' ).place(x=600,y=120)
        self.disT_capital=Label(self.report,text=" ",font=('Mochiy Pop P One' ,15,'bold'),bg='#bdbdbd' ).place(x=730,y=120)
        self.T_Profit =Label(self.report,text="Total Profit: ",font=('Mochiy Pop P One' ,15 ,'bold'),bg='#bdbdbd' ).place(x=900,y=120)
        self.heading1=Label(self.report,text=" Shop Records",font=('Mochiy Pop P One' ,20 ,'bold'),bg="#bdbdbd" )
        self.heading1.place(x=500,y=0)
        self.sele2 = Label(self.upreport,text="Select Day: ",font=('arial',13,'bold'),bg="#bdbdbd")
        self.sele2.place(x=0,y=50)
        self.t=StringVar()
        self.dayChoosen=ttk.Combobox(self.upreport,width=10,textvariable=self.t)
        self.dayChoosen['values'] =('Daily','Monthly')
        self.dayChoosen.place(x=150,y=50)
        self.dayChoosen['state']='readonly'
        self.chosen=self.dayChoosen.current()
        self.dayChoosen.bind('<<ComboboxSelected>>',self.select_job) 
    def fetch_day(self,*args,**kwargs):
        try :
            self.print_month.destroy()
            self.print_m.destroy()
        except:
            pass
        conn,cur = self.database()
        self.day =self.cal.get_date()
        self.Datep=Label(self.upreport,text=self.day,font=('arial',13,'bold'),bg="#bdbdbd").place(x=710,y=50)
        try:
            self.col = ('comodity','particulars','quantity','unitprice','sales','costofsales','capital','cprofit','tprofit','mode')
            self.tre = ttk.Treeview(self.upreport,height=18, columns=self.col, show='headings')
            self.tre.heading('comodity',text='commodity')
            self.tre.column('comodity',stretch=NO,width=130)
            self.tre.heading('particulars',text='particulars')
            self.tre.column('particulars',stretch=NO,width=130)
            self.tre.heading('quantity' ,text='quantity')
            self.tre.column('quantity',anchor=CENTER,stretch=NO,width=70)
            self.tre.heading('unitprice',text='untiprice')
            self.tre.column('unitprice',anchor=CENTER,stretch=NO,width=70)
            self.tre.heading('sales',text='Amount')
            self.tre.column('sales',anchor=CENTER,stretch=NO,width=70)
            self.tre.heading('costofsales',text='costofsale')
            self.tre.column('costofsales',anchor=CENTER,stretch=NO,width=70)
            self.tre.heading('capital',text='capital')
            self.tre.column('capital',anchor=CENTER,stretch=NO,width=150)
            self.tre.heading('cprofit',text='profit')
            self.tre.column('cprofit',anchor=CENTER,stretch=NO,width=100)
            self.tre.heading('tprofit',text='T_profit')
            self.tre.column('tprofit',anchor=CENTER,stretch=NO,width=100)
            self.tre.heading('mode',text='Mode')
            self.tre.column('mode',anchor=CENTER,stretch=NO,width=100)
            cur.execute('SELECT comodity,particulars,quantity,unitprice,sales,costofsales,capital,cprofit,tprofit,mode FROM transactions WHERE date=%s ORDER BY id ASC',(self.day,))
            self.result = cur.fetchall()
            conn.commit()
            if not self.result:
                messagebox.showinfo("no data", "No data for that particular day")
                self.report.destroy()
            else:
                for r in self.result:
                    self.tre.insert('',END,values=r)
                    self.capital = r[6]
                    self.profit=r[8]
                self.disT_capital=Label(self.report,text=str(self.capital),font=('Mochiy Pop P One' ,15,'bold'),bg='#bdbdbd' ).place(x=730,y=120)
                self.disT_profit=Label(self.report,text=str(self.profit),font=('Mochiy Pop P One' ,15 ,'bold'),bg='#bdbdbd' ).place(x=1020,y=120)
                self.tre.place(x=100,y=190)
                self.scrollbarr = ttk.Scrollbar(self.upreport, orient=tk.VERTICAL, command=self.tre.yview)
                self.tre.configure(yscroll=self.scrollbarr.set)
                self.scrollbarr.place(x=1110,y=190,relheight=0.6, anchor='ne')
                self.print_day = Button(self.report,text="Get pdf report" ,width=20,bg='steelblue',font=('arial',10,'bold'), fg="white" ,command=self.print_btn)
                self.print_day.place(x=900,y=50)
        except Exception as e:
            print(traceback.format_exc())
            print(e)
    def select_month(self,*args,**kwargs):
        try:
            self.print_day.destroy()
        except:
            pass
        conn,cur = self.database()
        self.day =self.calM.get_date()
        self.mon =self.day[0] + self.day[1]
        self.month = int(self.mon)
        self.year =self.day[6]+self.day[7]+self.day[8]+self.day[9]
        self.Datep=Label(self.upreport,text=self.day,font=('arial',13,'bold'),bg="#bdbdbd").place(x=710,y=50)
        try:
            self.col = ('comodity','particulars','quantity','unitprice','sales','costofsales','capital','cprofit','tprofit','mode')
            self.tre = ttk.Treeview(self.upreport,height=18,columns=self.col, show='headings')
            self.tre.heading('comodity',text='commodity')
            self.tre.column('comodity',stretch=NO,width=130)
            self.tre.heading('particulars',text='particulars')
            self.tre.column('particulars',stretch=NO,width=130)
            self.tre.heading('quantity' ,text='quantity')
            self.tre.column('quantity',anchor=CENTER,stretch=NO,width=70)
            self.tre.heading('unitprice',text='untiprice')
            self.tre.column('unitprice',anchor=CENTER,stretch=NO,width=70)
            self.tre.heading('sales',text='Amount')
            self.tre.column('sales',anchor=CENTER,stretch=NO,width=70)
            self.tre.heading('costofsales',text='costofsale')
            self.tre.column('costofsales',anchor=CENTER,stretch=NO,width=70)
            self.tre.heading('capital',text='capital')
            self.tre.column('capital',anchor=CENTER,stretch=NO,width=150)
            self.tre.heading('cprofit',text='profit')
            self.tre.column('cprofit',anchor=CENTER,stretch=NO,width=100)
            self.tre.heading('tprofit',text='T_profit')
            self.tre.column('tprofit',anchor=CENTER,stretch=NO,width=100)
            self.tre.heading('mode',text='Mode')
            self.tre.column('mode',anchor=CENTER,stretch=NO,width=100)
            cur.execute('SELECT comodity,particulars,quantity,unitprice,sales,costofsales,capital,cprofit,tprofit,mode FROM transactions WHERE month=%s AND year =%s ORDER BY id ASC',(self.month,self.year,))
            self.result = cur.fetchall()
            if not self.result:
                messagebox.showinfo("no data", "No data for that particular Month")
                self.report.destroy()

            else:
                conn.commit()
                for r in self.result:
                    self.tre.insert('',END,values=r)
                    self.c =r[6]
                    self.p=r[8]
                self.disT_capital=Label(self.report,text=str(self.c),font=('Mochiy Pop P One' ,15,'bold'),bg='#bdbdbd' ).place(x=730,y=120)
                self.disT_profit=Label(self.report,text=str(self.p),font=('Mochiy Pop P One' ,15 ,'bold'),bg='#bdbdbd' ).place(x=1020,y=120)
                self.tre.place(x=100,y=190)
                self.scrollbarr = ttk.Scrollbar(self.upreport, orient=tk.VERTICAL, command=self.tre.yview)
                self.tre.configure(yscroll=self.scrollbarr.set)
                self.scrollbarr.place(x=1110,y=190,relheight=0.6, anchor='ne') 
                self.print_month = Button(self.report,text="Get pdf transaction" ,width=20,bg='steelblue',font=('arial',10,'bold'), fg="white" ,command=self.print_month)
                self.print_month.place( x=850,y=50)
                self.print_m = Button(self.report,text="Get pdf profit" ,width=20,bg='steelblue',font=('arial',10,'bold'), fg="white" ,command=self.print_stock_profit)
                self.print_m.place( x=1050,y=50)     
        except Exception as e:
            print(e)
    def print_stock_profit(self,*args,**kwargs):
        conn,cur = self.database()
        self.monp='close'
        cur.execute('SELECT monthlyp FROM transactions WHERE month=%s AND year =%s AND comodity=%s ',(self.month,self.year,self.monp,))
        r =[i[0] for i in cur.fetchall()]
        conn.commit()
        res=list(filter(None,r))
        q=0
        for x in range(0,len(res)):  
            res[x]=float(res[x])
        total_month_profit = (sum(res))
        
        cur.execute('SELECT date,monthlyp FROM transactions WHERE month=%s AND year =%s AND comodity=%s',(self.month,self.year,self.monp,))
        result =cur.fetchall()
        conn.commit()
        try:
            self.pdf=PDF()
            self.pdf.add_page()
            self.pdf.set_font('helvetica', 'B', 11)
            p=[]
            self.counter=1
            for r in result:
                date="<tr><td align=Center>%s</td>"%r[0]
                p.append(date)
                profit="<td align=Center >%s</td></tr>"%r[1]
                p.append(profit)
                # today =date.today()
                self.counter +=1
            self.pdf.write_html(
                f"""
                <h1>Monthly Profit</h1>
                <table border="0">
                <thead><tr><th width="20%">Date</th><th width="20%">Profit</th></tr></thead>
                <tbody>
                {p}
                </tbody>
                
                </table>
                <h2>Total Monthly Profit : {total_month_profit}</h3>
                """
        )
            messagebox.showinfo('success',"check your directory  (Monthly profit.pdf)")
            self.pdf.output("C:\shoprecords\Monthly Profit.pdf",'F')
        except Exception as e:
            print(traceback.format_exc())
            print(e)
        finally:
            self.report.destroy()
    def print_most(self,*args,**kwargs):
        conn,cur = self.database()
        try:
            self.pdf=PDF()
            self.pdf.add_page()
            self.pdf.set_font('helvetica', 'B', 11)
            p=[]
            self.counter=1
            for re in self.result:
                cur.execute(' SELECT quantity FROM  transactions WHERE comodity=%s AND date=%s',(re,self.mon,))
                r =[i[0] for i in cur.fetchall()]
                conn.commit()
                for x in range(0,len(r)):  
                    r[x]=float(r[x])
                qadd = sum(r)
                cur.execute(' SELECT cprofit FROM  transactions WHERE comodity=%s AND date=%s',(re,self.mon,))
                t =[i[0] for i in cur.fetchall()]
                conn.commit()
                for x in range(0,len(t)):  
                    t[x]=float(t[x])
                padd = sum(t)
                no="<tr><td align=Center>%s</td>"%self.counter
                p.append(no)
                commodity="<td>%s</td>"%re
                p.append(commodity)
                quantity="<td align=Center>%s</td>"%qadd
                p.append(quantity)
                cprofit="<td align=Center>%s</td></tr>"%padd
                p.append(cprofit)
                today =date.today()
                self.counter +=1
            self.pdf.write_html(
                f"""
                <h1> Best Selling </h1> <h2>{today}</h2>
                <table border="0">
                <thead><tr><th width="5%">No</th><th width="20%">commodity</th><th width="15%">Quantity</th><th width="15%">Profit</th></tr></thead>
                <tbody>
                {p}
                </tbody>
                </table>
                """
        )
            messagebox.showinfo('success',"check your directory  (MostSelling record.pdf)")
            self.pdf.output("C:\shoprecords\MostSelling record.pdf",'F')
        except Exception as e:
            print(e)
        # finally:
            # self.top.destroy()

    def print_stock_F(self,*args,**kwargs):

        try:
            self.pdf=PDF()
            self.pdf.add_page()
            self.pdf.set_font('helvetica', 'B', 11)
            p=[]
            self.counter=1
            for r in self.results:
                no="<tr><td align=Center>%s</td>"%self.counter
                p.append(no)
                commodity="<td>%s</td>"%r[0]
                p.append(commodity)
                stock="<td align=Center>%s</td>"%r[1]
                p.append(stock)
                cost="<td align=Center>%s</td>"%r[2]
                p.append(cost)
                sp="<td align=Center>%s</td>"%r[3]
                p.append(sp)
                wholesale="<td align=Center >%s</td></tr>"%r[4]
                p.append(wholesale)
                today =date.today()
                
                self.counter +=1
            self.pdf.write_html(
                f"""
                <h1> Inventory Stock</h1> <h2>{today}</h2>
                
                <table border="0">
                <thead><tr><th width="5%">No</th><th width="20%">commodity</th><th width="15%">stock</th><th width="15%">COS</th><th width="15%">Retail</th><th width="15%">Wholesale</th></tr></thead>
                <tbody>
                {p}
                </tbody>
                </table>
                """
        )
            messagebox.showinfo('success',"check your directory  (Stock record.pdf)")
            self.pdf.output("C:\shoprecords\Stock record.pdf",'F')
        except Exception as e:
            print(e)
        finally:
            self.top.destroy()
    def print_btn(self,*args,**kwargs):
        try:
            self.pdf=PDF()
            self.pdf.add_page()
            self.pdf.set_font('helvetica', 'B', 10)
            p=[]
            for r in self.result:
                commodity="<tr><td >%s</td>"%r[0]
                p.append(commodity)
                particulars="<td>%s</td>"%r[1]
                p.append(particulars)
                quantity="<td align=Center>%s</td>"%r[2]
                p.append(quantity)
                unitprice="<td>%s</td>"%r[3]
                p.append(unitprice)
                Amount="<td>%s</td>"%r[4]
                p.append(Amount)
                costofsales="<td>%s</td>"%r[5]
                p.append(costofsales)
                capital="<td>%s</td>"%r[6]
                p.append(capital)
                profit="<td align=Center>%s</td>"%r[7]
                p.append(profit)
                Tprofit="<td>%s</td>"%r[8]
                p.append(Tprofit)
                mode="<td align=Center>%s</td></tr>"%r[9]
                p.append(mode)
            today =date.today()
            pro=self.profit
            cap=self.capital
            self.pdf.write_html(
                f"""
                <h1>Daily Transaction Records </h1> <h2>{today}</h2>
                <table>
                <thead><tr><th width="18%">commodity</th><th width="10%">particulars</th><th width="10%">quantity</th><th width="10%">unitprice</th><th width="10%">Amount</th><th width="9%">COS</th><th width="10%">capital</th><th width="9%">profit</th><th width="10%">Total profit</th><th width="9%">Mode</th></tr></thead>
                <tbody>
                {p}
                </tbody>
                </table>
                <div>
                <h2>Total Capital : {cap}  Total Profit : {pro}</h2>
                </div>
                """
        )
            messagebox.showinfo('success',"check your directory(Dailyrecord .pdf)")
            self.pdf.output("C:\shoprecords\Daily Record.pdf",'F')
        finally:
            self.report.destroy()
    def print_month(self,*args,**kwargs):
        conn,cur = self.database()
        cur.execute('SELECT date,monthlyp FROM transactions WHERE month=%s AND year =%s',(self.month,self.year,))
        r =[i[1] for i in cur.fetchall()]
        result =cur.fetchall()
        conn.commit()
        res=list(filter(None,r))
        q=0
        for x in range(0,len(res)):  
            res[x]=float(res[x])
        total_month_profit = (sum(res))
        try:
            self.pdf=PDF()
            self.pdf.add_page()
            self.pdf.set_font('helvetica', 'B', 10)
            p=[]
            for r in self.result:
                commodity="<tr><td >%s</td>"%r[0]
                p.append(commodity)
                particulars="<td>%s</td>"%r[1]
                p.append(particulars)
                quantity="<td align=Center>%s</td>"%r[2]
                p.append(quantity)
                unitprice="<td>%s</td>"%r[3]
                p.append(unitprice)
                Amount="<td>%s</td>"%r[4]
                p.append(Amount)
                costofsales="<td>%s</td>"%r[5]
                p.append(costofsales)
                capital="<td>%s</td>"%r[6]
                p.append(capital)
                profit="<td align=Center>%s</td>"%r[7]
                p.append(profit)
                Tprofit="<td>%s</td>"%r[8]
                p.append(Tprofit)
                mode="<td align=Center>%s</td></tr>"%r[9]
                p.append(mode)
            today =date.today()
            cap=self.c
            self.pdf.write_html(
                f"""
                <h1> Monthly Transaction Records </h1> <h2>{today}</h2>
                <table>
                <thead><tr><th width="18%">commodity</th><th width="10%">particulars</th><th width="10%">quantity</th><th width="10%">unitprice</th><th width="10%">Amount</th><th width="9%">COS</th><th width="10%">capital</th><th width="9%">profit</th><th width="10%">Total profit</th><th width="9%">Mode</th></tr></thead>
                <tbody>
                {p}
                </tbody>
                </table>
                <div>
                <h2>Total Capital : {cap} </h2>
                </div>
                """
        )
            messagebox.showinfo('success',"check your directory(Monthlyrecord .pdf)")
            self.pdf.output("C:\shoprecords\Monthly Record.pdf",'F')
        finally:
            self.report.destroy()
    
           

class PDF(FPDF, HTMLMixin):
    pass
window = Tk ()

b=index(window)

window.geometry("1350x658+0+5")
window.title("Shop Inventory and stock keeping")
window.mainloop()