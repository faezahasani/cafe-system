from tkinter import *
import Menu_Frame
from Total_Frame import TotalSection

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        self.left = Frame(self.master, borderwidth=2, relief="solid")
        self.right = Frame(self.master, borderwidth=2, relief="solid")
        self.right.pack(side="right", expand=True, fill="both")

        pad = 3
        self.master.title("Cashier")
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

        Menu_Frame.MenuSection(self.left, self.right)
        TotalSection(self.right)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom

window = Tk()
app = FullScreenApp(window)
window.mainloop()
