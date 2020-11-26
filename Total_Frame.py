from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
import Menu_Frame
from client import client

#Display the total and buttons
class TotalSection(object):
    def __init__(self, right):
        label4 = Label(right, text="Selected Items", width=30, height=2, font=("courier", 17, "bold"))
        label5 = Label(right, text="Item                Price", width=30, height=2, font=("courier", 10, "bold"), anchor='w')
        label4.pack()
        label5.pack()
        TotalSection.createScrolling(self, right)
        box = Frame(right, borderwidth=2)
        total_label = Label(box, text="Total=   " + str(0), width=30, height=2, font=("ariel", 17, "bold"))
        box.pack(side="bottom", expand=True, fill="both", padx=10, pady=10)
        nota = self.newNota(box)
        continuar = Button(box, text="Continue",height = 4, width=25, bg="lime green", padx=10, pady=10, command= lambda: self.continuar(nota))
        cancelar = Button(box, text="Cancel",height = 4, width=25, bg="fireBrick2", padx=10, pady=10, command= lambda: self.delete(nota))
        continuar.pack(side = "left")
        cancelar.pack( side = "left")

    #Creates the scrolling widget to allow the cashier enter multiple items
    def createScrolling(self, right):
        container = ttk.Frame(right)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        TotalSection.scrollable_frame = ttk.Frame(canvas)
        TotalSection.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=TotalSection.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    #Return the note for the chef
    def newNota(self, box):
        F = Frame(box)
        F.pack()
        L1 = Label(F, text="Extra instructions",font=("arial", 10, "bold"))
        L1.pack(side=LEFT)
        E1 = Text(F, bd=3, height=2, width=20)
        E1.pack(side=RIGHT)
        return E1

    #Sends the object to the client.
    #So it will send it on the socket for the chef
    def continuar(self, nota):
        global ORDER
        #send order just when total is pressed
        if(Menu_Frame.DISM==0):
            messagebox.showinfo("Order", "Press total")
        else:
            global ORDER
            if len(ORDER)>0:
                ORDER.append({"Nota":nota.get("1.0", "end-1c")})
                client.client_socket(self, ORDER)
                messagebox.showinfo("Order", "Order sent to the chef successfully")
            else:
                messagebox.showinfo("Order", "No items selected")
            self.delete(nota)

    #Reset the values of the JSON
    def delete(self,nota):
        global ORDER, GLOBAL_TOTAL, ITEM_VAL, GLOBAL_LABELS, GLOBAL_TOTAL_LABEL, E
        Menu_Frame.DISM, GLOBAL_TOTAL = 0, 0
        Menu_Frame.TO_GO.set(0)
        Menu_Frame.MenuSection.checkboxToGo.config(state='normal')
        nota.delete("1.0", "end")
        if E != None:
            for i in E:
                i.config(state='normal')
                i.delete(0, "end")
        for i in range(len(GLOBAL_TOTAL_LABEL)):
            GLOBAL_TOTAL_LABEL[i].destroy()
        for i in range(len(ORDER)):
            ORDER.pop()
        for i in range(len(ITEM_VAL)):
            ITEM_VAL.pop()
        for i in range(len(GLOBAL_ITEM_LABELS)):
            GLOBAL_ITEM_LABELS[i].destroy()

#Display the selected items on the right side
class DisplayItems():
    def printItem(self, x, val, right):
        global GLOBAL_ITEM_LABELS, GLOBAL
        num = str(val)
        item = {x: val}
        ORDER.append(item)
        ITEM_VAL.append(val)
        lab_text=x
        lab_cost=str(num)
        whitespace_num=40-len(x)-len(lab_cost)-10
        counter_i=0
        whitespace_txt=""
        while(counter_i<whitespace_num):
            whitespace_txt=whitespace_txt+" "
            counter_i=counter_i+1
        label_final_text=lab_text+whitespace_txt+"Rs."+lab_cost
        label = Label(TotalSection.scrollable_frame, text=label_final_text, width=40, height=1, font=("courier", 10, "bold"), anchor="w")
        GLOBAL_ITEM_LABELS.append(label)
        label.pack(fill='x')
        if x != "Cold Drink" and x!= "Watter Bottle" and x!= "Ice Cream":
            self.calculate()

    #calculate the sum of the items
    def calculate(self):
        global ORDER, GLOBAL_TOTAL
        total = 0
        for i in ITEM_VAL:
            total = total + i
        GLOBAL_TOTAL = total

    #Check if it is a number. Then convert it
    def convertStr(self, d):
        if d.isdigit():
            if len(d) > 0:
                dd = int(d)
        else:
            dd = 0
        return dd

    #store the extras and checkbox in the same JSON as the items
    def showTotal(self, right, checkbox, entrys):
        global ORDER, GLOBAL_TOTAL, GLOBAL_TOTAL_LABEL,PRESSED_TOTAL
        global E
        E = entrys
        d = entrys[0].get()
        v = entrys[1].get()
        b = entrys[2].get()
        intd, intv, intb = self.convertStr(d), self.convertStr(v), self.convertStr(b)
        self.fillEntrys(intd, intv, intb, right)
        self.set_to_go(checkbox)
        GLOBAL_TOTAL = GLOBAL_TOTAL+intd+intv+intb
        label = Label(right, text="Total= Rs."+str(GLOBAL_TOTAL), font=("arial", 15, "bold"), height = 4)
        GLOBAL_TOTAL_LABEL.append(label)
        label.pack()

    #store the checkbox on the order.
    def set_to_go(self, checkbox):
        global ORDER
        if checkbox.get()==1:
            dicC = {"to-go":checkbox.get()}
            ORDER.append(dicC)

    #Check for the values of the Extras
    def fillEntrys(self, d, v, b, right):
        if d!=0:
            self.printItem("Cold Drink", d, right)
        if v != 0:
            self.printItem("Water Bottle", v, right)
        if b != 0:
            self.printItem("Ice Cream", b, right)


#global variables
GLOBAL_TOTAL=0
ITEM_VAL = []
ORDER = []
GLOBAL_ITEM_LABELS = []
GLOBAL_TOTAL_LABEL = []
E = None
