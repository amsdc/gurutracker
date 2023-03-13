"""PDF tools
"""

import os
import shutil
import tempfile
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from PIL import Image

import gurutracker.views.helpers
from gurutracker.globals import settings, controller

class ImagesToPDF(tk.Toplevel):
    def __init__(self, parent, sel_record=None, callback=None, *a, **kw):
        tk.Toplevel.__init__(self, parent, *a, **kw)
        
        self.title("Images to PDF")
        
        self.transient(parent)
        
        self.callback = callback
        self.selected_record = sel_record
        
        self.pdf_list_label = ttk.Label(self, text="Image Files", anchor=tk.W)
        self.pdf_list_label.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=2, pady=2)
        
        self.pdf_list = tk.Variable()
        self.pdf_listbox = tk.Listbox(self, 
                                      listvariable=self.pdf_list,
                                      width=50,
                                      height=6,
                                      selectmode=tk.BROWSE)
        self.pdf_listbox.grid(row=1, column=0, sticky=tk.NSEW, pady=2)
        self.pdf_scroll = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.pdf_scroll.grid(row=1, column=1, sticky=tk.NS)
        self.pdf_scrollh = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.pdf_scrollh.grid(row=2, column=0, sticky=tk.EW)
        self.pdf_listbox["yscrollcommand"]=self.pdf_scroll.set
        self.pdf_scroll["command"] = self.pdf_listbox.yview
        self.pdf_listbox["xscrollcommand"]=self.pdf_scrollh.set
        self.pdf_scrollh["command"] = self.pdf_listbox.xview

        self.add_file_button = ttk.Button(self, text="Add File", command=self.add_file)
        self.add_file_button.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, padx=2, pady=2)
        self.save_file_button = ttk.Button(self, text="Save as PDF File", command=self.save_somewhere)
        self.save_file_button.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW, padx=2, pady=2)
        self.save_rec_button = ttk.Button(self, text="Save to Selected record", 
                                          command=self.save_sel_rec,
                                          state=(tk.NORMAL if sel_record else tk.DISABLED))
        self.save_rec_button.grid(row=5, column=0, columnspan=2, sticky=tk.NSEW, padx=2, pady=2)
        
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        
        self.pdf_listbox.bind('<Double-Button-1>', self.delete_selected)
        
        gurutracker.views.helpers.center_window_wrt(self, parent)
        
    def add_file(self):
        fname = filedialog.askopenfilenames(filetypes=[
                ('Image Files', '.jpg .jpeg .png .bmp .gif .tiff .svg')])
        if fname:
            for name in fname:
                self.pdf_listbox.insert(tk.END, name)
    
    def delete_selected(self, event=None):
        # https://stackoverflow.com/questions/53107722/python-tkinter-deleting-selected-listbox-item
        sel = self.pdf_listbox.curselection()
        # added reversed here so index deletion work for multiple selections.
        for index in reversed(sel):
            self.pdf_listbox.delete(index)
        
    def save_to_temp(self):
        imgpaths = self.pdf_list.get()
        if len(imgpaths) > 0:
            dr =  tempfile.TemporaryDirectory()
            image_1 = Image.open(imgpaths[0]).convert('RGB')
            
            if len(imgpaths) > 1:
                imgs = []

                for i in range(1, len(imgpaths)):
                    imgs.append(Image.open(imgpaths[i]).convert('RGB'))

                image_1.save(os.path.join(dr.name, "output.pdf"),
                        save_all=True, append_images=imgs)
            else:
                image_1.save(os.path.join(dr.name, "output.pdf"))
            
            return dr, "output.pdf"
        else:
            return None
        
    def save_somewhere(self):
        dat = self.save_to_temp()
        if dat:
            dr, op = dat
            f = filedialog.asksaveasfilename(filetypes=[
                    ('PDF Files', '*.pdf')],
                    defaultextension='.pdf')
            if f:
                shutil.copy(os.path.join(dr.name, op), f)
                messagebox.showinfo("Success", "Success")
                if callable(self.callback):
                    self.callback()
                self.destroy()
            dr.cleanup()
        else:
            messagebox.showerror("Error", "Please add atleast one file.")
    
    def save_sel_rec(self):
        dat = self.save_to_temp()
        if dat:
            dr, op = dat
            gurutracker.views.helpers.associate_file_with_record(self.config, self.selected_record, os.path.join(dr.name, op))
            dr.cleanup()
                
            messagebox.showinfo("Success", "Success")
            if callable(self.callback):
                self.callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "Please add atleast one file.")
