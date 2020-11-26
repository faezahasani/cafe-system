from tkinter import *
import Total_Frame

#Menusection class contains the menu on the cashier side.
class MenuSection(object):
    def __init__(self, left, right):
        container = Frame(left, borderwidth=2, relief="solid")
        checkbox = self.Checkboxes(left)
        left.pack(side="left", expand=True, fill="both")
        container.pack(expand=True, fill="both", padx=10, pady=10)
        Menu(container, right, checkbox)

    # class in charge of create checkbox ToGo
    def Checkboxes(self, left):
        global TO_GO
        TO_GO = IntVar()
        checkboxContainer = Frame(left)
        checkboxContainer.pack()

        MenuSection.checkboxToGo = Checkbutton(checkboxContainer, text="To-Go", variable=TO_GO)
        MenuSection.checkboxToGo.pack(side=LEFT, fill="both", padx=10, pady=10)
        return TO_GO


# Create the menu items, entrys, and "Total button"
class Menu(object):
    def __init__(self, container, right, checkbox):
        container_left = Frame(container, borderwidth=2)
        container_middle = Frame(container, borderwidth=2)
        container_right = Frame(container, borderwidth=2)
        container_left.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        container_middle.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        container_right.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        col1 = {"Red Sauce Pasta": 220, "White Sauce Pasta": 240, "Taco": 180, "Hakka Noodles": 200, "Veg. Chowmein": 120, "Plain Dosa": 80, "Masala Dosa": 120,
                "Cheese Pizza": 200, "Chicken Pizza": 250}
        col2 = {"Chilli Potato": 80, "Veg. Momos": 60, "Chicken Momos": 80, "Spring Roll": 60,
                    "Idli Sambhar": 80, "Vada Sambhar": 80}
        col3 = {"Paneer Tikka": 120, "Malai Chaanp": 120, "Chicken Tikka": 200,
                  "French Fries": 80, "Veg. Burger": 60, "Grilled Sandwich": 60, "Veg. Manchurian": 200, 
                    "Waffles": 100, "Choco Brownie": 120}
        text = ["Cold Drink", "Water Bottle", "Ice Cream"]
        self.fillMenu(col1, container_left, right)
        self.fillMenu(col2, container_middle, right)
        self.fillMenu(col3, container_right, right)
        entrys = self.setEntry(container_middle, text)

        # when click the "Total" it will display the total at the Total_frame
        done_button = Button(container_right, text="Total",
                             command=lambda: self.disableButton(right, checkbox, entrys), height=4, width=30,
                             font=("arial", 10, "bold"), bg="orange")
        done_button.pack(side=BOTTOM)

    # After the Total has been clicked, it will disable Menu and total
    def disableButton(self, right, checkbox, entrys):
        global DISM
        if DISM == 0:
            MenuSection.checkboxToGo.config(state='disable')
            for i in entrys:
                i.config(state='disable')
            Total_Frame.DisplayItems().showTotal(right, checkbox, entrys)
        DISM = 1

    #Return the entry widget
    def setEntry(self, container, t):
        entrys = []
        for i in t:
            L1 = Label(container, text=i, font=("arial", 10, "bold"))
            L1.pack()
            E1 = Entry(container, bd=3)
            E1.pack()
            entrys.append(E1)
        return entrys

    #Creates the button for each item of the menu.
    def fillMenu(self, item, container, right):
        for i in item:
            button = Button(container, text=i, command=lambda key=i, val=item[i]: self.disableMenu(key, val, right),
                            height=4, width=30)
            button.pack(fill=BOTH)

    # disable the menu
    def disableMenu(self, key, val, right):
        global DISM
        if DISM == 0:
            Total_Frame.DisplayItems().printItem(key, val, right)

DISM = 0
TO_GO = 0