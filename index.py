from tkinter import*
from tkinter import ttk 
import tkinter as tk
from tkinter import messagebox 
import mysql.connector



class housekeeping:
    def __init__(self,root) :
        self.root=root
        self.root.title("Housekeeing Management System")
        self.root.geometry("1550x800+0+0")

        # variables
        self.var_room_entry=StringVar()
        self.var_room_type=StringVar()
        self.var_status=StringVar()
        self.var_keeper=StringVar()
        self.var_fo_status=StringVar()

        # title
        title=Label(self.root,text="Housekeeing Management System",font=("times new roman",48,"bold"),bg="black",fg="gold")
        title.place(x=0,y=20,width=1550,height=80)
        
        # Room Number
        self.room=Label(self.root, text = "Room No:", font = ("Times New Roman", 18))
        self.room.place(x=5,y=150)
        self.room_entry = ttk.Entry(self.root,textvariable=self.var_room_entry, font=('Times New Roman',12))
        self.room_entry.place(x=150,y=150)
        
        # Room Type
        self.room_type1=Label(self.root, text = "Room Type:", font = ("Times New Roman", 18))
        self.room_type1.place(x=5,y=200)
        self.room_type=ttk.Combobox(root,textvariable=self.var_room_type,font =("Times New Roman", 15,"bold"),width=10,values=["Single","Double","Deluxe","Duplex","Cabana"],state="readonly")
        self.room_type.place(x=150, y=200)
        self.room_type.current() 

        # Room Status
        self.room_status=Label(root, text = "Room Status:", font = ("Times New Roman", 18))
        self.room_status.place(x=400,y=150)
        self.status=ttk.Combobox(self.root,textvariable= self.var_status,font =("Times New Roman", 15,"bold"),width=15 ,values=[" Clean"," Out of order"," Out of service"," Dirty"," Pickup"," Inspected"],state="readonly")
        self.status.place(x=560, y=150)
        self.status.current() 

        # Name of the housekeeper
        self.housekeeper=Label(self.root, text = "House Keeper:", font = ("Times New Roman", 18))
        self.housekeeper.place(x=400,y=200)
        self.keeper=ttk.Combobox(root,textvariable=self.var_keeper,font =("Times New Roman", 15,"bold"),width=15 ,values=[" None"," Rajesh Sharma", " Sanjay Patel"," Amit Singh"," Ravi Reddy"," Arjun Nair"," Anil Yadav"," Sunil Verma", " Deepak Mehta", " Ajay Joshi", " Vinod Desai"," Priya Gupta"," Sita Iyer", " Nisha Khan", " Aarti Sharma", " Anjali Das", " Pooja Choudhary", " Swati Rao", " Rekha Menon"],state="readonly")
        self.keeper.place(x=560, y=200)
        self.keeper.current() 

        # FRont office Status
        self.fostatus=Label(self.root, text = "FO Status:", font = ("Times New Roman", 18))
        self.fostatus.place(x=850,y=150)
        self.fo_status=ttk.Combobox(root,textvariable=self.var_fo_status,font =("Times New Roman", 15,"bold"),width=10 ,values=[" Vacant"," Occupied"," Check In"," Check Out"," Stay over"],state="readonly")
        self.fo_status.place(x=980, y=150)
        self.fo_status.current() 

        # Buttons 

        add=Button(self.root,text="ADD",command=self.add,font=("arial",12,"bold"),bg="red",fg="white",width=8)
        add.place(x=1180,y=120)

        update=Button(self.root,text="UPDATE",command=self.update,font=("arial",12,"bold"),bg="red",fg="white",width=8)
        update.place(x=1350,y=120)

        self.search_var=StringVar()
        self.search_text=StringVar()

        search=Button(self.root,text="SEARCH",command=self.search,font=("arial",12,"bold"),bg="red",fg="white",width=8)
        search.place(x=1350,y=220)
        s = tk.Entry(root,textvariable=self.search_text,font=('Times New Roman',15))
        s.place(x=1160,y=220,height=30,width=150)

        searchby=Label(self.root,text="SEARCH BY",font=("arial",12,"bold"),bg="brown",fg="white",width=8)
        searchby.place(x=850,y=220,width=110)
        self.sb=ttk.Combobox(self.root,textvariable=self.search_var,font =("Times New Roman", 8,"bold"),width=15 ,values=["ROOM" , "ROOM_TYPE", "ROOM_STATUS" , "HK_STATUS" ,"FRONT_OFFICE_STATUS"],state="readonly")
        self.sb.place(x=980, y=220,width=150,height=30)
        

        reset=Button(self.root,text="RESET",command=self.reset,font=("arial",12,"bold"),bg="red",fg="white",width=8)
        reset.place(x=1180,y=170)

        show=Button(self.root,text="SHOW ALL",command=self.fetch_data,font=("arial",12,"bold"),bg="red",fg="white",width=8)
        show.place(x=1350,y=170,width=100)

        # Table frame 
        
        frame=LabelFrame(self.root,bd=5,relief=RIDGE,font=("arial",12,"bold"),padx=2)
        frame.place(x=120,y=290,width=1300,height=480)
        
        # Adding scroll bar
        scroll_x=ttk.Scrollbar(frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(frame,orient=VERTICAL)

        # show data table 
        self.table=ttk.Treeview(frame,column=("ROOM" , "ROOM_TYPE", "ROOM_STATUS" , "HOUSEKEEPER" ,"FRONT_OFFICE_STATUS"),xscrollcommand=scroll_x,yscrollcommand=scroll_y)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.table.xview)
        scroll_y.config(command=self.table.yview)

        self.table.heading("ROOM",text="ROOM NUMBER")
        self.table.heading("ROOM_TYPE",text="ROOM TYPE")
        self.table.heading("ROOM_STATUS",text="ROOM STATUS")
        self.table.heading("HOUSEKEEPER",text="HOUSEKEEPER")
        self.table.heading("FRONT_OFFICE_STATUS",text="FRONT OFFICE STATUS")
        self.table["show"]="headings"
        self.table.pack(fill=BOTH,expand=1)
        self.table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()


    def add(self):
        try:
            a=str(self.room_entry.get())
            b=str(self.room_type.get())
            c=str(self.status.get())
            d=str(self.keeper.get())
            e=str(self.fo_status.get())
                
            myconn=mysql.connector.connect(host="localhost",username="root",password="root",database="moon")
            my_cursor=myconn.cursor()
            my_cursor.execute("insert into moon.data(ROOM,ROOM_TYPE,ROOM_STATUS,HK_STATUS,FRONT_OFFICE_STATUS)values(%s,%s,%s,%s,%s)",(a,b,c,d,e))
            myconn.commit()
            self.fetch_data()
            myconn.close()
            messagebox.showinfo("Success!","Successfully added",parent=self.root)
        except Exception as e:
            messagebox.showwarning("Warning!",f" Something went wrong:{str(e)}",parent=self.root)


    def fetch_data(self):
        myconn=mysql.connector.connect(host="localhost",username="root",password="root",database="moon")
        my_cursor=myconn.cursor()
        my_cursor.execute("select * from data")
        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.table.delete(*self.table.get_children())
            for i in rows:
                self.table.insert("",END,values=i)
            myconn.commit()
        myconn.close() 

    def get_cursor(self,event=""):
        select_row=self.table.focus()
        content=self.table.item(select_row)
        row=content["values"]

        self.var_room_entry.set(row[0]),
        self.var_room_type.set(row[1]),
        self.var_status.set(row[2]),
        self.var_keeper.set(row[3]),
        self.var_fo_status.set(row[4])
 
    def update(self):
        try:
            a=str(self.room_entry.get())
            b=str(self.room_type.get())
            c=str(self.status.get())
            d=str(self.keeper.get())
            e=str(self.fo_status.get())
            myconn=mysql.connector.connect(host="localhost",username="root",password="root",database="moon")
            my_cursor=myconn.cursor()
            my_cursor.execute("update data set ROOM_TYPE=%s,ROOM_STATUS=%s ,Hk_STATUS=%s ,FRONT_OFFICE_STATUS=%s where ROOM=%s",(b,c,d,e,a))
            myconn.commit()
            self.fetch_data()
            myconn.close()
            messagebox.showinfo("Update!","Successfully Updated.")
        except Exception as e:
            messagebox.showwarning("Warning!",f" Something went wrong:{str(e)}",parent=self.root)


    def reset(self):
        self.var_room_entry.set(""),
        self.var_room_type.set(""),
        self.var_status.set(""),
        self.var_keeper.set(""),
        self.var_fo_status.set("")
        self.search_var.set("")
        self.search_text.set("")

    def search(self):
        try:
            myconn=mysql.connector.connect(host="localhost",username="root",password="root",database="moon")
            my_cursor=myconn.cursor()
            v=str(self.search_var.get())
            t=str(self.search_text.get())
            my_cursor.execute("select* from data where {} LIKE '%{}%'".format(v,t))
            rows=my_cursor.fetchall()
            if len(rows)!=0:
                self.table.delete(*self.table.get_children())
                for i in rows:
                    self.table.insert("",END,values=i)
                myconn.commit()
            myconn.close() 
        except Exception as e:
            messagebox.showwarning("Warning!",f" Something went wrong:{str(e)}",parent=self.root)

# Main function
if __name__=="__main__":
    root=Tk()
    obj=housekeeping(root)
    root.mainloop()
