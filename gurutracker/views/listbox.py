import tkinter as tk
from tkinter import ttk
from functools import partial

class AssignmentListView(ttk.Treeview):
    def __init__(self, parent, *a, showcols=None, **kw):
        super().__init__(parent, *a, **kw)
        
        cols = ["assignment.id", "assignment.name", "assignment.uidentifier", "assignment.type", "tutor.id", "tutor.name", "tutor.uidentifier", "tutor.subject", "tutor.level"]
        self["columns"] = cols
        self['show'] = 'headings'
        self["selectmode"] = tk.BROWSE
        
        if showcols:
            self["displaycolumns"] = showcols
        else:
            self["displaycolumns"] = ("assignment.id", "assignment.name", "assignment.uidentifier", "assignment.type", "tutor.name", "tutor.subject", "tutor.level")
        
        self.heading('assignment.id', text='A#')
        self.heading('assignment.name', text='Name')
        self.heading('assignment.uidentifier', text='UID')
        self.heading('assignment.type', text='Type')
        self.heading('tutor.id', text='T#')
        self.heading('tutor.name', text='Tutor')
        self.heading('tutor.uidentifier', text='Tutor UID')
        self.heading('tutor.subject', text='Subject')
        self.heading('tutor.level', text='Level')
        
        self.column('assignment.id', width=40)
    
    def insert_queryresult(self, assignment, tags=None):
        values=(assignment.id, assignment.name, assignment.uidentifier, assignment.type, assignment.tutor.id, assignment.tutor.name, assignment.tutor.uidentifier, assignment.tutor.subject, assignment.tutor.level)
        if tags:
            self.insert('', tk.END, values=values, tags=tags)
        else:
            self.insert('', tk.END, values=values)
    
    def insert_queryresults(self, result, tag_func=None):
        for assn in result:
            if callable(tag_func):
                self.insert_queryresult(assn, tag_func(assn))
            else:
                self.insert_queryresult(assn)


class TutorListView(ttk.Treeview):
    def __init__(self, parent, *a, showcols=None, **kw):
        super().__init__(parent, *a, **kw)
        
        cols = ["tutor.id", "tutor.name", "tutor.uidentifier", "tutor.subject", "tutor.level"]
        self["columns"] = cols
        self['show'] = 'headings'
        self["selectmode"] = tk.BROWSE
        
        if showcols:
            self["displaycolumns"] = showcols
        else:
            self["displaycolumns"] = ("tutor.name", "tutor.uidentifier", "tutor.subject", "tutor.level")
        
        self.heading('tutor.id', text='T#')
        self.heading('tutor.name', text='Tutor')
        self.heading('tutor.uidentifier', text='Tutor UID')
        self.heading('tutor.subject', text='Subject')
        self.heading('tutor.level', text='Level')
        
        self.column('tutor.id', width=40)
    
    def insert_queryresult(self, tutor, tags=()):
        self.insert('', tk.END, iid="{}".format(tutor.id), values=(tutor.id, tutor.name, tutor.uidentifier, tutor.subject, tutor.level), tags=tags)
    
    def insert_queryresults(self, result):
        for teac in result:
            self.insert_queryresult(teac)


class TagListView(ttk.Treeview):
    def __init__(self, parent, *a, showcols=None, **kw):
        super().__init__(parent, *a, **kw)
        
        cols = ["tag.id", "tag.text", "tag.fgcolor", "tag.bgcolor"]
        self["columns"] = cols
        self['show'] = 'headings'
        
        if showcols:
            self["displaycolumns"] = showcols
        else:
            self["displaycolumns"] = ("tag.text",)
        
        self.heading('tag.id', text='#')
        self.heading('tag.text', text='Tag')
        self.heading('tag.fgcolor', text='Foreground Color')
        self.heading('tag.bgcolor', text='Background Color')
        
        self.column('tag.id', width=40)
    
    def insert_queryresult(self, tag, tags=()):
        f = "" if tag.fgcolor is None else tag.fgcolor
        b = "" if tag.bgcolor is None else tag.bgcolor
        self.insert('', tk.END, iid="{}".format(tag.id), values=(tag.id, tag.text, f, b), tags=tags)
    
    def insert_queryresults(self, result):
        for tag in result:
            self.insert_queryresult(tag)


class TreeviewFrame(tk.Frame):
    def __init__(self, parent, treeview, *a, **kw):
        super().__init__(parent)
        
        self.treeview = treeview(self, *a, **kw)
        self.treeview.grid(row=0, column=0, sticky='nsew')
        
        self.yscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscroll=self.yscrollbar.set)
        self.yscrollbar.grid(row=0, column=1, sticky='ns')
        
        
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        
        self.append = self.treeview.insert_queryresult
        self.extend = self.treeview.insert_queryresults
        
        self.bind = self.treeview.bind
        self.selection = self.treeview.selection
        
    def clear(self):
        self.treeview.delete(*self.treeview.get_children())


class AssignmentListFrame(TreeviewFrame):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, AssignmentListView, *a, **kw)


class TutorListFrame(TreeviewFrame):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, TutorListView, *a, **kw)


class TagListFrame(TreeviewFrame):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, TagListView, *a, **kw)
        
