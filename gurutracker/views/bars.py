import tkinter as tk
from tkinter import ttk

class ToolBar(tk.Frame):
    def __init__(self, parent, *a, bd=1, relief = tk.RAISED, **kw):
        self.parent = parent
        super().__init__(self.parent, *a, bd=bd, relief=relief, **kw)

        self.menus = {}

    def set_menu(self, name, text, menu):
        if name not in self.menus:
            mb = ttk.Menubutton(self)
            mb.pack(side=tk.LEFT, anchor=tk.NW)
            self.menus[name] = mb
        self.menus[name]["text"] = text
        self.menus[name]["menu"] = menu

    def set_button(self, name, text, command=None, state=tk.NORMAL):
        if name not in self.menus:
            mb = tk.Button(self, bd=0, relief=tk.FLAT)
            mb.pack(side=tk.LEFT, anchor=tk.NW)
            self.menus[name] = mb
        self.menus[name]["text"] = text
        self.menus[name]["command"] = command
        self.menus[name]["state"] = state


class MultiStatusBar(ttk.Frame):
    def __init__(self, master, **kw):
        ttk.Frame.__init__(self, master, **kw)
        self.labels = {}

    def set_label(self, name, text='', side='left', width=0):
        if name not in self.labels:
            label = ttk.Label(self, borderwidth=0, anchor='w')
            label.pack(side=side, pady=0, padx=4)
            self.labels[name] = label
        else:
            label = self.labels[name]
        if width != 0:
            label.config(width=width)
        label.config(text=text)