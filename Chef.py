from tkinter import *
import threading
import socket
import pickle
import Inventory
import tkinter as tk
from tkinter import ttk


#Global variable
ORDER_DIC = {}
ORDER_NUM = 0
BUTTON_NUM=1

#Creates a thread to run the chef socket
#The thread helps to avoid interference with the gui
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        Inventory.Inv()
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        server.server_socket(self)

#Establish the server connection that receives the socket from cashier.
#place your own ip
class server(object):
    def server_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 3125 
        ip = '' #insert server ip

        s.bind((ip, port))
        s.listen(3)
        print ('socket is listening')

        while True:
            c, addr = s.accept()
            message = pickle.loads(c.recv(1024))
            FullScreenApp.set_dic(self, message)

#Contains the gui for the chef and its funtionabilities
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        FullScreenApp.master = master
        FullScreenApp.left = Frame(self.master,width=((FullScreenApp.master.winfo_screenwidth())/3), borderwidth=2, relief="solid")
        FullScreenApp.right = Frame(self.master, borderwidth=2, relief="solid")
        FullScreenApp.right.pack(side="right", fill="both",expand=TRUE)
        FullScreenApp.left.pack(side="left", fill="both")

        pad = 3
        FullScreenApp.master.title("Ordenes")
        FullScreenApp._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

    #Set size of the gui to full screen
    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom

    #Create the button for each order and re arranges them
    def createButtons(self):
        global ORDER_NUM, BUTTONS
        temp = ORDER_NUM
        children_num=0
        button_order = Button(FullScreenApp.left, text="Order #" + str(temp),
                          height=1, width=60, bg="blue", fg='white')
        button_order.pack(side="top")
        button_order.config(command=lambda: FullScreenApp.disp_obj(self, button_order['text']))
        for component in FullScreenApp.left.winfo_children():
            children_num=children_num+1
        for component_1 in FullScreenApp.left.winfo_children():
            component_1.config(height=int(27/children_num))

    #In charge of displaying the order
    def disp_obj(self,num):
        global ORDER_DIC
        FullScreenApp.clean_right_frame(self)
        #FullScreenApp.createScrolling(self)
        str_ord = num.split("#")
        n = int(str_ord[1])
        count = len(ORDER_DIC)
        if count>0:
            FullScreenApp.createScrolling(self,n)
            #FullScreenApp.display.config(text=ORDER_DIC[n], width=30, height=10, font=("courier", 17, "bold"))
        button_complete = Button(FullScreenApp.right, text="Complete",
                                 command=lambda: FullScreenApp.clearOrder(self, n),
                                 height=4, width=30, font=("arial", 10, "bold"), bg="green")
        button_complete.place(rely=1.0, relx=1.0, x=-25, y=-50, anchor=SE)

    #Cleans the completed order
    def clean_right_frame(self):
        for widget in FullScreenApp.right.winfo_children():
            widget.destroy()

    #Receive the order and store it on the dictoriary
    def set_dic(self, rx):
        global ORDER_NUM, ORDER_DIC
        Inventory.Inv.add(self, rx)
        ORDER_NUM = ORDER_NUM+1
        order_str = ""
        for i in rx:
            for y in i:
                if y == 'Nota':
                    order_str = order_str + "\n" + i[y]
                else:
                    order_str = order_str + "\n" + y
        ORDER_DIC[ORDER_NUM] = order_str
        FullScreenApp.createButtons(self)

    #After the order is done, deletes the button order
    def clearOrder(self,button_n):
        global ORDER_DIC
        if ORDER_DIC:
            del ORDER_DIC[button_n]
        for widget in FullScreenApp.left.winfo_children():
            if widget['text'] == "Order #" + str(button_n):
                messagebox.showinfo("Order", "Order #" + str(button_n) + "completed. Send message to display screen.")
                widget.destroy()
        FullScreenApp.clean_right_frame(self)

    #Creates the scrolling that shows the itemps in the order
    def createScrolling(self,n):
        container = ttk.Frame(FullScreenApp.right,height=550,width=550)
        canvas = tk.Canvas(container,height=550,width=550)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas,height=550,width=550)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        spl_order = ORDER_DIC[n].splitlines()
        for i in spl_order:
            FullScreenApp.display = Label(scrollable_frame, text=i,font=("courier", 16, "bold"))
            FullScreenApp.display.pack()
        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


thread_server = myThread(1, "Thread-1", 1)
thread_server.start()
window = Tk()
app = FullScreenApp(window)
window.mainloop()
