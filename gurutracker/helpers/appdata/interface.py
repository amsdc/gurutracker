import threading
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox


class StdoutRedirector(object):
    # https://stackoverflow.com/questions/18517084/how-to-redirect-stdout-to-a-tkinter-text-widget
    
    def __init__(self, text_widget, stop_func=None):
        self.text_space = text_widget
        self.stop_func = stop_func if callable(stop_func) else print

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')
        
        # check if time to stop
        if string[1] in ("E", "D"):
            self.stop_func(string[1])

    def flush(self):
        pass


class AppdataProgressWindow(tk.Toplevel):
    def __init__(self, parent, module, function, file, *a, **kw):
        self.parent = parent
        self.module = module
        self.function = function
        self.file = file
        super().__init__(parent, *a, **kw)
        self.transient(parent)
        
        # self.resizable(False, False)
        self.title("Appdata Progress")
        
        self.pb = ttk.Progressbar(self, orient='horizontal', mode='indeterminate')
        self.pb.grid(row=0, column=0, sticky=tk.EW, padx=2, pady=2)
        
        
        self.logs = scrolledtext.ScrolledText(self, width=70, height=20)
        self.logs.grid(row=1, column=0, sticky=tk.NSEW, padx=2, pady=2)
        self.logs.insert("0.0", "Press Start to start export.\n\n")
        self.stdout_redir = StdoutRedirector(self.logs, self.stop_export)
        
        self.startbtn = ttk.Button(self, text="Start", command=self.start_export)
        self.startbtn.grid(row=2, column=0, sticky=tk.EW, padx=2, pady=2)
    
    def start_export(self):
        if self.module == "load_from_old":
            from gurutracker.helpers.appdata import load_from_old as mod
        else:
            messagebox.showerror("Error", f"The module {self.module} is "
                                 "untrusted or does not exist.")
            self.destroy()
        
        export_fun = getattr(mod, self.function)
        t = threading.Thread(target=export_fun, args=(self.file, self.stdout_redir,))
        t.start()
        self.startbtn['state'] = "disabled"
        self.pb.start()
    
    def stop_export(self, reason="D"):
        self.pb.stop()
        self.pb['mode'] = 'determinate'
        self.pb['value'] = 100
        if reason == "D":
            self.startbtn['text'] = "Finished data transfer. Click to close"
        else:
            self.startbtn['text'] = "Data transfer failed. Click to close"
        self.startbtn['command'] = self.destroy
        self.startbtn['state'] = "normal"