import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
FILE = "sales_data.csv"
def load():
    return pd.read_csv(FILE) if os.path.exists(FILE) else pd.DataFrame(
        columns=["Date","Customer","Product","Category","Quantity","Price","Total"])
def save():
    df.to_csv(FILE, index=False)
def clear():
    for w in content.winfo_children():
        w.destroy()
def card(parent, title, value, col):
    box = tk.Frame(parent, bg="#edf2f6", width=210, height=90)
    box.grid(row=0, column=col, padx=6)
    box.grid_propagate(False)
    tk.Label(box,text=title,bg="#edf2f6",fg="#65727e",
             font=("Arial",10)).pack(pady=(14,3))
    tk.Label(box,text=value,bg="#edf2f6",fg="#20364d",
             font=("Arial",16,"bold")).pack()
def dashboard():
    global df
    df=load(); clear()
    tk.Label(content,text="Dashboard",bg="white",fg="#20364d",
             font=("Arial",22,"bold")).pack(anchor="w",padx=25,pady=(22,3))
    tk.Label(content,text="Retail shop sales summary",
             bg="white",fg="#65727e").pack(anchor="w",padx=25)
    row=tk.Frame(content,bg="white"); row.pack(fill="x",padx=25,pady=25)
    card(row,"Total Sales",f"₹ {df.Total.sum():,.2f}",0)
    card(row,"Total Quantity",f"{df.Quantity.sum():.0f}",1)
    card(row,"Orders",str(len(df)),2)
    card(row,"Average Bill",f"₹ {df.Total.mean():,.2f}",3)
    tk.Label(content,text="Recent Sales",bg="white",fg="#20364d",
             font=("Arial",14,"bold")).pack(anchor="w",padx=25,pady=8)
    t=ttk.Treeview(content,columns=("Date","Customer","Product","Total"),
                   show="headings",height=7); t.pack(fill="x",padx=25)
    for c in t["columns"]:
        t.heading(c,text=c); t.column(c,width=170,anchor="center")
    for _,r in df.tail(7).iterrows():
        t.insert("","end",values=(r.Date,r.Customer,r.Product,f"₹ {r.Total:.2f}"))
def fill(data):
    for x in tree.get_children(): tree.delete(x)
    for _,r in data.iterrows():
        tree.insert("","end",values=(r.Date,r.Customer,r.Product,r.Category,
                     r.Quantity,f"{r.Price:.2f}",f"{r.Total:.2f}"))
def search_data(text):
    text=text.lower().strip()
    if not text: fill(df); return
    a=df[df.Product.str.lower().str.contains(text,na=False)]
    b=df[df.Customer.str.lower().str.contains(text,na=False)]
    fill(pd.concat([a,b]).drop_duplicates())
def sales_page():
    clear()
    tk.Label(content,text="Sales Data",bg="white",fg="#20364d",
             font=("Arial",22,"bold")).pack(anchor="w",padx=25,pady=(22,3))
    top=tk.Frame(content,bg="white"); top.pack(fill="x",padx=25,pady=15)
    tk.Label(top,text="Search by Customer or Product:",bg="white",fg="#20364d",
             font=("Arial",10,"bold")).pack(side="left",padx=(0,10))
    e=ttk.Entry(top,width=30); e.pack(side="left")
    ttk.Button(top,text="Search",command=lambda:search_data(e.get())).pack(side="left",padx=8)
    ttk.Button(top,text="Show All",command=lambda:fill(df)).pack(side="left")
    global tree
    tree=ttk.Treeview(content,columns=("Date","Customer","Product","Category","Qty","Price","Total"),
                      show="headings"); tree.pack(side="left",fill="both",expand=True,padx=(25,0))
    for c in tree["columns"]:
        tree.heading(c,text=c); tree.column(c,width=105,anchor="center")
    s=ttk.Scrollbar(content,command=tree.yview); s.pack(side="right",fill="y",padx=(0,25))
    tree.configure(yscrollcommand=s.set); fill(df)
def add_page():
    clear()
    tk.Label(content,text="Add New Sale",bg="white",fg="#20364d",
             font=("Arial",22,"bold")).pack(anchor="w",padx=25,pady=(22,3))
    box=tk.Frame(content,bg="#f5f7f9",bd=1,relief="solid")
    box.pack(padx=100,pady=25,fill="x")
    fields=["Date","Customer","Product","Category","Quantity","Price"]; es={}
    for i,n in enumerate(fields):
        tk.Label(box,text=n,bg="#f5f7f9",font=("Arial",10,"bold")).grid(
            row=i,column=0,padx=20,pady=7,sticky="w")
        es[n]=ttk.Entry(box,width=32); es[n].grid(row=i,column=1,padx=20,pady=7)
    es["Date"].insert(0,pd.Timestamp.today().strftime("%Y-%m-%d"))
    def add():
        global df
        try:
            date=pd.to_datetime(es["Date"].get(),errors="raise")
            q=float(es["Quantity"].get()); p=float(es["Price"].get())
            if date>pd.Timestamp.today() or q<=0 or p<0 or not all(es[x].get() for x in fields[1:4]):
                raise ValueError
            new=pd.DataFrame([[date.strftime("%Y-%m-%d"),es["Customer"].get(),
                es["Product"].get(),es["Category"].get(),q,p,q*p]],columns=df.columns)
            df=pd.concat([df,new],ignore_index=True); save()
            messagebox.showinfo("Success","Sale added successfully!"); dashboard()
        except:
            messagebox.showerror("Error","Enter valid details. Future dates are not allowed.")
    ttk.Button(box,text="Add Sale",command=add).grid(row=6,column=0,columnspan=2,pady=15)
def analysis_page():
    clear()
    tk.Label(content,text="Charts & Analysis",bg="white",fg="#20364d",
             font=("Arial",22,"bold")).pack(anchor="w",padx=25,pady=(22,3))
    high=np.max(df.Total); low=np.min(df.Total); avg=np.mean(df.Total)
    tk.Label(content,text=f"Highest Bill: ₹ {high:.2f}   |   Lowest Bill: ₹ {low:.2f}   |   Average: ₹ {avg:.2f}",
             bg="#f5f7f9",fg="#20364d",font=("Arial",11,"bold"),
             bd=1,relief="solid",padx=15,pady=14).pack(fill="x",padx=25,pady=20)
    b=tk.Frame(content,bg="white"); b.pack(pady=20)
    def category():
        df.groupby("Category").Total.sum().plot(kind="pie",autopct="%1.1f%%",figsize=(6,5))
        plt.title("Category Sales Share"); plt.ylabel(""); plt.tight_layout(); plt.show()
    def product():
        df.groupby("Product").Quantity.sum().sort_values().plot(kind="barh",figsize=(7,4))
        plt.title("Customer Buying Pattern"); plt.xlabel("Quantity Sold")
        plt.tight_layout(); plt.show()
    def monthly():
        x=df.copy(); x["Date"]=pd.to_datetime(x.Date)
        m=x.groupby(x.Date.dt.month).Total.sum()
        m.plot(kind="line",marker="o",figsize=(8,4))
        plt.title("Monthly Sales Trend"); plt.xlabel("Month Number"); plt.ylabel("Sales (₹)")
        plt.xticks(range(1,10)); plt.grid(True); plt.tight_layout(); plt.show()
    ttk.Button(b,text="Sales by Category",command=category).grid(row=0,column=0,padx=8)
    ttk.Button(b,text="Buying Pattern",command=product).grid(row=0,column=1,padx=8)
    ttk.Button(b,text="Monthly Sales",command=monthly).grid(row=0,column=2,padx=8)
df=load()
root=tk.Tk(); root.title("Retail Shop Sales & Customer Buying Pattern Analyzer")
root.geometry("1050x650"); root.configure(bg="white")
style=ttk.Style(); style.theme_use("clam")
style.configure("TButton",font=("Arial",10,"bold"),padding=8)
style.configure("Treeview",rowheight=28)
side=tk.Frame(root,bg="#243b53",width=220); side.pack(side="left",fill="y"); side.pack_propagate(False)
tk.Label(side,text="RETAIL SHOP",bg="#243b53",fg="white",
         font=("Arial",17,"bold")).pack(pady=(30,3))
tk.Label(side,text="Sales Analyzer",bg="#243b53",fg="#c9d6e2").pack(pady=(0,30))
def nav(text,cmd):
    tk.Button(side,text=text,command=cmd,bg="#314e68",fg="white",bd=0,
              anchor="w",padx=25,pady=12,font=("Arial",10,"bold")).pack(fill="x",padx=15,pady=4)
nav("Dashboard",dashboard); nav("Sales Data",sales_page)
nav("Add New Sale",add_page); nav("Charts & Analysis",analysis_page)
nav("Exit",root.destroy)
content=tk.Frame(root,bg="white"); content.pack(side="right",fill="both",expand=True)
dashboard(); root.mainloop()
