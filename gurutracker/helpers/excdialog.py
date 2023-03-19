import sys
import traceback
import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtxt

from gurutracker.views.helpers import center_window

class ExceptionDialog(tk.Toplevel):
    def __init__(self, parent, errmsg, *a, **kw):
        super().__init__(parent, *a, **kw)
        
        self.title("Unhandled Exception")
        self.transient(parent)
        self.grab_set()
        self.attributes("-topmost", 1)

        self.lbl = tk.Label(self, 
                            text="Unhandled Exception has occured in the code.", 
                            anchor=tk.W)
        self.lbl.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=tk.EW)
        
        self.textbox = scrolledtxt.ScrolledText(self, width=40, height=10)
        self.textbox.grid(row=1, column=0, rowspan=3, padx=2, pady=2, sticky=tk.NSEW)
        self.textbox.insert("end", errmsg)
        
        self.textbox.config(state=tk.DISABLED)

        self.continuebtn = tk.Button(self, text="Continue", command=self.destroy)
        self.continuebtn.grid(row=1, column=1, sticky=tk.EW, padx=2, pady=2)

        self.quitbtn = tk.Button(self, text="Quit", command=self.bye)
        self.quitbtn.grid(row=2, column=1, sticky=tk.EW, padx=2, pady=2)
        
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.rowconfigure(self, 3, weight=1)
        center_window(self)
    
    def bye(self):
        self.destroy()
        sys.exit(1)


def errstr(*args):
    return "".join(tuple(traceback.format_exception(*args)))


def show_error(self, *args):
    err = errstr(*args)
    ExceptionDialog(self, err)

if __name__ == "__main__":
    ExceptionDialog("wdw\n"*10)
