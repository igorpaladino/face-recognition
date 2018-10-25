import Tkinter as tk
from App import App

root = tk.Tk() # creating an ordinary window
app = App(root).pack(side="top", fill="both", expand =True)
root.mainloop() # show the window and activate it