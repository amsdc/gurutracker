import tkinter as tk
from tkinter import ttk
from functools import partial

class AssignmentListView(ttk.Treeview):
    def __init__(self, parent, *a, showcols=None, **kw):
        super().__init__(parent, *a, **kw)
        
        cols = ["assignment.id", "assignment.name", "assignment.uidentifier", "assignment.type", "tutor.id", "tutor.name", "tutor.uidentifier", "subject.id", "subject.name", "subject.desc", "subject.uidentifier", ".assignment.uidentifier"]
        self["columns"] = cols
        self['show'] = 'headings'
        self["selectmode"] = tk.BROWSE
        
        if showcols:
            self["displaycolumns"] = showcols
        else:
            self["displaycolumns"] = ("assignment.id", "assignment.name", ".assignment.uidentifier", "assignment.type", "tutor.name", "subject.name")
        
        self.heading('assignment.id', text='A#')
        self.heading('assignment.name', text='Name')
        self.heading('assignment.uidentifier', text='Assignment UID')
        self.heading('assignment.type', text='Type')
        self.heading('tutor.id', text='T#')
        self.heading('tutor.name', text='Tutor')
        self.heading('tutor.uidentifier', text='Tutor UID')
        self.heading('subject.id', text='S#')
        self.heading('subject.name', text='Subject')
        self.heading('subject.desc', text='Subject Description')
        self.heading('subject.uidentifier', text='Subject UID')
        self.heading('.assignment.uidentifier', text='UID') # Subject UID/Tutor UID/Assignment UID
        
        self.column('assignment.id', width=40, stretch=False)
        self.column('tutor.id', width=40, stretch=False)
        self.column('subject.id', width=40, stretch=False)
    
    def insert_queryresult(self, assignment, tags=None):
        values=(assignment.id, assignment.name, assignment.uidentifier, assignment.type, assignment.tutor.id, assignment.tutor.name, assignment.tutor.uidentifier, assignment.tutor.subject.id, assignment.tutor.subject.name, assignment.tutor.subject.desc, assignment.tutor.subject.uidentifier, "/".join((assignment.tutor.subject.uidentifier, assignment.tutor.uidentifier, assignment.uidentifier)))
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
        
        cols = ["tutor.id", "tutor.name", "tutor.uidentifier", "subject.id", "subject.name", "subject.desc", "subject.uidentifier", ".tutor.uidentifier"]
        self["columns"] = cols
        self['show'] = 'headings'
        self["selectmode"] = tk.BROWSE
        
        if showcols:
            self["displaycolumns"] = showcols
        else:
            self["displaycolumns"] = ("tutor.name", ".tutor.uidentifier", "subject.name", "subject.desc")
        
        self.heading('tutor.id', text='T#')
        self.heading('tutor.name', text='Tutor')
        self.heading('tutor.uidentifier', text='Tutor UID')
        self.heading('subject.id', text='S#')
        self.heading('subject.name', text='Subject')
        self.heading('subject.desc', text='Subject Description')
        self.heading('subject.uidentifier', text='Subject UID')
        self.heading('.tutor.uidentifier', text='UID') # Subject UID/Tutor UID
        
        self.column('tutor.id', width=40, stretch=False)
        self.column('subject.id', width=40, stretch=False)
    
    def insert_queryresult(self, tutor, tags=()):
        self.insert('', tk.END, iid="{}".format(tutor.id), values=(tutor.id, tutor.name, tutor.uidentifier, tutor.subject.id, tutor.subject.name, tutor.subject.desc, tutor.subject.uidentifier, "/".join((tutor.subject.uidentifier, tutor.uidentifier))), tags=tags)
    
    def insert_queryresults(self, result):
        for teac in result:
            self.insert_queryresult(teac)


class SubjectListView(ttk.Treeview):
    def __init__(self, parent, *a, showcols=None, **kw):
        super().__init__(parent, *a, **kw)
        
        cols = ["subject.id", "subject.name", "subject.desc", "subject.uidentifier"]
        self["columns"] = cols
        self['show'] = 'headings'
        self["selectmode"] = tk.BROWSE
        
        if showcols:
            self["displaycolumns"] = showcols
        else:
            self["displaycolumns"] = ("subject.name", "subject.desc", "subject.uidentifier")
        
        self.heading('subject.id', text='S#')
        self.heading('subject.name', text='Subject')
        self.heading('subject.desc', text='Subject Description')
        self.heading('subject.uidentifier', text='Subject UID')

        self.column('subject.id', width=40, stretch=False)
    
    def insert_queryresult(self, subject, tags=None):
        values=(subject.id, subject.name, subject.desc, subject.uidentifier)
        if tags:
            self.insert('', tk.END, iid="{}".format(subject.id), values=values, tags=tags)
        else:
            self.insert('', tk.END, iid="{}".format(subject.id), values=values)
    
    def insert_queryresults(self, result, tag_func=None):
        for assn in result:
            if callable(tag_func):
                self.insert_queryresult(assn, tag_func(assn))
            else:
                self.insert_queryresult(assn)


class SendToListView(ttk.Treeview):
    def __init__(self, parent, *a, showcols=None, **kw):
        super().__init__(parent, *a, **kw)
        
        cols = ["app_name", "app_exc"]
        self["columns"] = cols
        self['show'] = ''
        self["selectmode"] = tk.BROWSE
        
        if showcols:
            self["displaycolumns"] = showcols
        else:
            self["displaycolumns"] = ["app_name"]
        
        self.heading('app_name', text='App Name')
        self.heading('app_exc', text='Exc')
    
    def insert_queryresult(self, values, tags=None):
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


class SubjectListFrame(TreeviewFrame):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, SubjectListView, *a, **kw)

class SendToListFrame(TreeviewFrame):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, SendToListView, *a, **kw)