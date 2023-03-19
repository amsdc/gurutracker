from abc import ABC, abstractmethod
import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import colorchooser

from gurutracker.globals import settings, controller
from gurutracker.database.objects import Assignment, Tutor, Tag, Subject
from gurutracker.views.listbox import TutorListFrame, TagListFrame, SubjectListFrame, SendToListFrame
from gurutracker.views.helpers import center_window, center_window_wrt
from gurutracker.views.widgets import DropdownCombobox
from gurutracker.helpers.object_typecaster import tagname_list, taglist_to_objects
from gurutracker.helpers.storage import send_file


NAME_VALIDATION_REGEX=r"[a-zA-Z0-9\(\) ]+"
UID_VALIDATION_REGEX=r"[A-Z0-9]+"

# Assignment Dialogs

class AssignmentDialogBase(tk.Toplevel, ABC):
    def __init__(self, parent, assignment=None, callback=None, *a, **kw):
        tk.Toplevel.__init__(self, parent, *a, **kw)
        
        
        self.assignment = assignment
        self.callback = callback
        
        self.transient(parent)
        
        self.assn_id_label = ttk.Label(self, text="Assignment Number")
        self.assn_id_label.grid(row=0, column=0, sticky=tk.E, padx=2, pady=2)
        self.assn_id_entry = tk.StringVar()
        self.assn_id__entry = ttk.Entry(self, state="readonly", textvariable=self.assn_id_entry)
        self.assn_id__entry.grid(row=0, column=1, sticky=tk.EW, padx=2, pady=2)
        
        self.assn_name_label = ttk.Label(self, text="Assignment Name")
        self.assn_name_label.grid(row=1, column=0, sticky=tk.E, padx=2, pady=2)
        self.assn_name_entry = tk.StringVar()
        self.assn_name__entry = ttk.Entry(self, textvariable=self.assn_name_entry)
        self.assn_name__entry.grid(row=1, column=1, sticky=tk.EW, padx=2, pady=2)
        
        self.assn_uid_label = ttk.Label(self, text="Assignment UID")
        self.assn_uid_label.grid(row=2, column=0, sticky=tk.E, padx=2, pady=2)
        self.assn_uid_entry = tk.StringVar()
        self.assn_uid__entry = ttk.Entry(self, textvariable=self.assn_uid_entry)
        self.assn_uid__entry.grid(row=2, column=1, sticky=tk.EW, padx=2, pady=2)
        
        self.assn_type_label = ttk.Label(self, text="Assignment Type")
        self.assn_type_label.grid(row=3, column=0, sticky=tk.E, padx=2, pady=2)
        """
        self.assn_type_entry = ttk.Entry(self)
        self.assn_type_entry.grid(row=3, column=1, sticky=tk.EW, padx=2, pady=2)
        """
        self.assn_type_entry = tk.StringVar()
        self.assn_type_combo = ttk.Combobox(self, textvariable=self.assn_type_entry, state="readonly")
        self.assn_type_combo["values"] = ["summary", "worksheet", "test"]
        self.assn_type_combo.grid(row=3, column=1, sticky=tk.EW, padx=2, pady=2)
        
        self.assn_tutor_label = ttk.Label(self, text="Tutor")
        self.assn_tutor_label.grid(row=4, column=0, sticky=tk.E, padx=2, pady=2)
        self.assn_tutor_tv = TutorListFrame(self, showcols=settings.getlist("gui.preferences", "dialogs.AssignmentDialogBase.TutorListFrame.displaycolumns"))
        self.assn_tutor_tv.extend(controller.list_tutors())
        self.assn_tutor_tv.grid(row=4, column=1, sticky=tk.NSEW, padx=2, pady=2)
        
        self.submit = ttk.Button(self, text="Submit")
        self.submit.grid(row=5, column=0, columnspan=2, sticky=tk.EW, padx=2, pady=2)
        
        tk.Grid.rowconfigure(self, 4, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=1)
        
        self.populate()
        center_window_wrt(self, parent)
        
    @abstractmethod
    def populate(self):
        pass
        
    def validate(self):
        errors = ""
        id_str = self.assn_id_entry.get()
        name = self.assn_name_entry.get()
        uidentifier = self.assn_uid_entry.get()
        type = self.assn_type_entry.get()
        tutor = self.assn_tutor_tv.treeview.selection()
        
        if id_str:
            id = int(id_str)
        else:
            id = None
        
        if not name:
            errors += "* Please enter the assignment name.\n"
            

        if not uidentifier:
            errors += "* Please enter the UID of the assignment.\n"
        else:
            query = controller.get_assignment_by_uid(uidentifier)
            if query and (not id or query.id != id):
                errors += "* The chosen UID is already in use. Please choose another.\n"
        if not type:
            errors += "* Please select the assignment type.\n"
        if tutor and len(tutor) != 1:
            errors += "* Please select only one tutor.\n"
        elif not tutor:
            errors += "* Please select a tutor.\n"
            
        if errors:
            messagebox.showerror("Error", errors)
            
        return not errors


class NewAssignment(AssignmentDialogBase):
    def populate(self):
        self.title("New Assignment")
        self.submit["text"] = "Add"
        self.submit["command"] = self.add
        
    def add(self):
        sel = self.assn_tutor_tv.treeview.selection()
        if self.validate():
            tid = self.assn_tutor_tv.treeview.item(sel[0])["values"][0]
        
            assn = Assignment(name=self.assn_name_entry.get(),
                              uidentifier=self.assn_uid_entry.get(),
                              type=self.assn_type_entry.get(),
                              tutor=Tutor(id=tid))
                              
            try:
                controller.add_assignment(assn)
            except Exception as e:
                messagebox.showerror("Database Error {}".format(str(type(e))), str(e))
            else:
                messagebox.showinfo("Success", "The ID of the assignment is {}".format(assn.id))
                if callable(self.callback):
                    self.callback()
                self.destroy()


class EditAssignment(AssignmentDialogBase):
    def populate(self):
        self.title("Edit Assignment")
        
        self.assn_id_entry.set(self.assignment.id)
        self.assn_name_entry.set(self.assignment.name)
        self.assn_uid_entry.set(self.assignment.uidentifier)
        self.assn_type_entry.set(self.assignment.type)
        self.assn_tutor_tv.treeview.selection_set("{}".format(self.assignment.tutor.id))
        
        self.submit["text"] = "Edit"
        self.submit["command"] = self.edit
        
    def edit(self):
        sel = self.assn_tutor_tv.treeview.selection()
        if self.validate():
            tid = self.assn_tutor_tv.treeview.item(sel[0])["values"][0]
        
            assn = Assignment(id=int(self.assn_id_entry.get()),
                              name=self.assn_name_entry.get(),
                              uidentifier=self.assn_uid_entry.get(),
                              type=self.assn_type_entry.get(),
                              tutor=Tutor(id=tid))
                              
            try:
                controller.edit_assignment(assn)
            except Exception as e:
                messagebox.showerror("Database Error {}".format(str(type(e))), str(e))
            else:
                messagebox.showinfo("Success", "Edited Assignment {}".format(assn.id))
                if callable(self.callback):
                    self.callback()
                self.destroy()

# Tutor Dialogs

class TutorDialogBase(tk.Toplevel, ABC):
    def __init__(self, parent, tutor=None, callback=None, *a, **kw):
        tk.Toplevel.__init__(self, parent, *a, **kw)
        
        
        self.tutor = tutor
        self.callback = callback
        
        self.transient(parent)
        
        
        self.tutor_id_label = tk.Label(self, text="Tutor Number")
        self.tutor_id_label.grid(row=0, column=0, sticky=tk.E, padx=2, pady=2)
        self.tutor_id_entry = tk.StringVar()
        self.tutor_id__entry = ttk.Entry(self, state="readonly", textvariable=self.tutor_id_entry)
        self.tutor_id__entry.grid(row=0, column=1, sticky=tk.EW, padx=2, pady=2)
        
        self.tutor_name_label = tk.Label(self, text="Tutor Name")
        self.tutor_name_label.grid(row=1, column=0, sticky=tk.E, padx=2, pady=2)
        self.tutor_name_entry = tk.StringVar()
        self.tutor_name__entry = ttk.Entry(self, textvariable=self.tutor_name_entry)
        self.tutor_name__entry.grid(row=1, column=1, sticky=tk.EW, padx=2, pady=2)
        
        self.tutor_uid_label = tk.Label(self, text="Tutor UID")
        self.tutor_uid_label.grid(row=2, column=0, sticky=tk.E, padx=2, pady=2)
        self.tutor_uid_entry = tk.StringVar()
        self.tutor_uid__entry = ttk.Entry(self, textvariable=self.tutor_uid_entry)
        self.tutor_uid__entry.grid(row=2, column=1, sticky=tk.EW, padx=2, pady=2)
        
        self.tutor_subj_label = tk.Label(self, text="Subject")
        self.tutor_subj_label.grid(row=3, column=0, sticky=tk.E, padx=2, pady=2)
        # self.tutor_subj_entry = tk.StringVar()
        self.tutor_subj = SubjectListFrame(self, showcols=settings.getlist("gui.preferences", "dialogs.TutorDialogBase.SubjectListFrame.displaycolumns"))
        self.tutor_subj.grid(row=3, column=1, sticky=tk.EW, padx=2, pady=2)
        self.tutor_subj.extend(controller.list_all_subjects())
        
        
        self.submit = ttk.Button(self, text="Submit")
        self.submit.grid(row=4, column=0, columnspan=2, sticky=tk.EW, padx=2, pady=2)
        
        tk.Grid.rowconfigure(self, 4, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=1)
        
        self.populate()
        center_window_wrt(self, parent)
        
    @abstractmethod
    def populate(self):
        pass
        
    def validate(self):
        errors = ""
        id_str = self.tutor_id_entry.get()
        name = self.tutor_name_entry.get()
        uidentifier = self.tutor_uid_entry.get()
        subject = self.tutor_subj.treeview.selection()
        if id_str:
            id = int(id_str)
        else:
            id = None
        
        if not name:
            errors += "* Please enter the tutor name.\n"
        elif not re.fullmatch(NAME_VALIDATION_REGEX, name):
            errors += f"* The name must only contain alphabets, numbers and the space character. \n"
            

        if not uidentifier:
            errors += "* Please enter the UID of the tutor.\n"
        elif not re.fullmatch(UID_VALIDATION_REGEX, uidentifier):
            errors += f"* The UID must be in all caps and can only contain letters A-Z, numbers 0-9.\n"
        else:
            query = controller.get_tutor_by_uid(uidentifier)
            if query and (not id or query.id != id):
                errors += "* The chosen UID is already in use. Please choose another.\n"
                
        if subject and len(subject) != 1:
            errors += "* Please select only one subject.\n"
        elif not subject:
            errors += "* Please select a subject.\n"
        
        if errors:
            messagebox.showerror("Error", errors)
            
        return not errors


class EditTutor(TutorDialogBase):
    def populate(self):
        self.title("Edit Tutor")
        
        self.tutor_id_entry.set(self.tutor.id)
        self.tutor_name_entry.set(self.tutor.name)
        self.tutor_uid_entry.set(self.tutor.uidentifier)
        self.tutor_subj.treeview.selection_set("{}".format(self.tutor.subject.id))
        
        self.submit["text"] = "Edit"
        self.submit["command"] = self.edit
        
    def edit(self):
        if self.validate():
            sub = Subject(id=int(self.tutor_subj.treeview.selection()[0]))
            tuto = Tutor(id=int(self.tutor_id_entry.get()),
                         name=self.tutor_name_entry.get(),
                         uidentifier=self.tutor_uid_entry.get(),
                         subject=sub)
            try:
                controller.edit_tutor(tuto)
            except Exception as e:
                messagebox.showerror("Database Error {}".format(str(type(e))), str(e))
            else:
                messagebox.showinfo("Success", "Tutor information updated.")
                if callable(self.callback):
                    self.callback()
                self.destroy()


class NewTutor(TutorDialogBase):
    def populate(self):
        self.title("New Tutor")
        self.submit["text"] = "Add"
        self.submit["command"] = self.add
        
    def add(self):
        if self.validate():
            sub = Subject(id=int(self.tutor_subj.treeview.selection()[0]))
            tuto = Tutor(name=self.tutor_name_entry.get(),
                         uidentifier=self.tutor_uid_entry.get(),
                         subject=sub)
            try:
                controller.add_tutor(tuto)
            except Exception as e:
                messagebox.showerror("Database Error {}".format(str(type(e))), str(e))
            else:
                messagebox.showinfo("Success", "The ID of the tutor is {}".format(tuto.id))
                if callable(self.callback):
                    self.callback()
                self.destroy()

# Tag Dialogs

class TagDialogBase(tk.Toplevel):
    def __init__(self, parent, assignment=None, callback=None, *a, **kw):
        tk.Toplevel.__init__(self, parent, *a, **kw)
        
        self.assignment = assignment
        self.callback = callback
        
        self.transient(parent)
        
        self.assn_tag_label = tk.Label(self, text="Tags")
        self.assn_tag_label.grid(row=0, column=0, columnspan=2, sticky=tk.EW, padx=2, pady=2)
        self.assn_tag_tv = TagListFrame(self, showcols=("tag.text",))
        self.assn_tag_tv.treeview['show'] = ""
        self.assn_tag_tv.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=2, pady=2)
        
        self.populate()
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        center_window_wrt(self, parent)
        
    def populate(self):
        pass
        
    def refresh(self):
        self.assn_tag_tv.clear()
        self.assn_tag_tv.extend(controller.assignment_tags(self.assignment))


class ViewTags(TagDialogBase):
    def populate(self):
        self.assn_tag_label["text"] = "Tags for {}".format(self.assignment.name)
        self.assn_tag_tv.extend(controller.assignment_tags(self.assignment))
        
        # for deletion
        self.assn_tag_tv.treeview.bind('<Double-Button-1>', self.tv_double_click)
        
        self.addtag_val = tk.StringVar()
        self.addtag_combo = DropdownCombobox(self, textvariable=self.addtag_val)
        self.addtag_combo.bind("<KeyPress>", self.change_data)
        self.addtag_combo["values"] = tagname_list(controller.list_tags())
        self.addtag_combo.grid(row=2, column=0, sticky=tk.EW, padx=2, pady=2)
        
        self.submit = ttk.Button(self, text="Add Tag", command=self.add_tag)
        self.submit.grid(row=2, column=1, sticky=tk.EW, padx=2, pady=2)
        
    def tv_double_click(self, event):
        sel = self.assn_tag_tv.treeview.selection()
        if sel:
            id = self.assn_tag_tv.treeview.item(sel[0])["values"][0]
            controller.untag_assignment(self.assignment, Tag(id=id))
            self.refresh()
            if callable(self.callback):
                self.callback()
        
    def change_data(self, event):
        self.addtag_combo["values"] = tagname_list(controller.search_tag_by_text_instr(self.addtag_val.get()))
        
    def _add_tag(self, tag):
        controller.tag_assignment(self.assignment, tag)
        self.refresh()
        if callable(self.callback):
            self.callback()
        
    def add_tag(self):
        tag = controller.get_tag(self.addtag_val.get())
        if tag:
            self._add_tag(tag)
        else:
            yn = messagebox.askyesno("Create Tag", "Tag does not exist\nCreate new tag?")
            if yn:
                tag = Tag(text=self.addtag_val.get())
                controller.add_tag(tag)
                self._add_tag(tag)


class FilterTags(TagDialogBase):
    def populate(self):
        self.assn_tag_label["text"] = "Filter Tags"
        self.assn_tag_tv.extend(controller.list_tags())
        # debug
        # self.assn_tag_tv.treeview["show"] = "headings"
        # self.assn_tag_tv.treeview["displaycolumns"] = ("tag.id", "tag.text",)
        # debug end
        
        # for filter
        self.assn_tag_tv.treeview.bind('<Double-Button-1>', self.tv_double_click)
        self.addtag_val = tk.StringVar()
        self.addtag_combo = ttk.Entry(self, textvariable=self.addtag_val)
        self.addtag_combo.bind("<KeyRelease>", self.change_data)
        # self.addtag_combo.bind("<<ComboboxSelected>>", self.change_data)
        # self.addtag_combo["values"] = tagname_list(controller.list_tags())
        self.addtag_combo.grid(row=2, column=0, columnspan=2, sticky=tk.EW, padx=2, pady=2)
        
        self.searchb = ttk.Button(self, text="Search", command=self.tv_double_click)
        self.searchb.grid(row=3, column=0, columnspan=2, sticky=tk.EW, padx=2, pady=2)
        
    def tv_double_click(self, event=None):
        sel = self.assn_tag_tv.treeview.selection()
        if sel:
            data = list()
            for id in sel:
                # id = self.assn_tag_tv.treeview.item(id)["values"][1])
                data += controller.tagged_assignments(Tag(id=int(id)))
            
            if callable(self.callback):
                self.callback(data)
                
    def change_data(self, event=None):
        d = controller.search_tag_by_text_instr(self.addtag_val.get())
        self.assn_tag_tv.clear()
        self.assn_tag_tv.extend(d)
        # self.addtag_combo["values"] = tagname_list(d)


class EditTags(tk.Toplevel):
    def __init__(self, parent, callback=None, *a, **kw):
        tk.Toplevel.__init__(self, parent, *a, **kw)
        
        
        self.callback = callback
        
        self.selected_record = None
        
        self.transient(parent)
        
        self.assn_tag_label = tk.Label(self, text="Edit Tags")
        self.assn_tag_label.grid(row=0, column=0, sticky=tk.EW, padx=2, pady=2)
        
        self.pw = tk.PanedWindow(self, orient =tk.HORIZONTAL)
        self.pw.grid(row=1, column=0, sticky=tk.NSEW)
        self.pw.configure(sashrelief=tk.RAISED)
        self.assn_tag_tv = TagListFrame(self.pw, showcols=("tag.id", "tag.text", "tag.fgcolor", "tag.bgcolor"))
        self.assn_tag_tv.treeview['show'] = "headings"
        self.assn_tag_tv.pack(fill=tk.BOTH, expand=True)
        self.pw.add(self.assn_tag_tv)
        
        self.data_frame = ttk.Frame(self.pw)
        self.data_frame.pack(fill=tk.BOTH, expand=True)
        self.pw.add(self.data_frame)
        
        ttk.Label(self.data_frame, text="Tag ID").grid(row=0, column=0, sticky=tk.NSEW, padx=2, pady=2)
        self.tag_id = tk.StringVar()
        ttk.Entry(self.data_frame, textvariable=self.tag_id, state="readonly").grid(row=0, column=1, sticky=tk.NSEW, padx=2, pady=2)
        
        ttk.Label(self.data_frame, text="Tag Text").grid(row=1, column=0, sticky=tk.NSEW, padx=2, pady=2)
        self.tag_name = tk.StringVar()
        ttk.Entry(self.data_frame, textvariable=self.tag_name).grid(row=1, column=1, sticky=tk.NSEW, padx=2, pady=2)
        
        ttk.Label(self.data_frame, text="FG Color").grid(row=2, column=0, sticky=tk.NSEW, padx=2, pady=2)
        self.fgcolor_button = tk.Button(self.data_frame, text="\t", command=self.change_fgcolor)
        self.fgcolor_button.grid(row=2, column=1, sticky="nsw", padx=2, pady=2)
        
        ttk.Label(self.data_frame, text="BG Color").grid(row=3, column=0, sticky=tk.NSEW, padx=2, pady=2)
        self.bgcolor_button = tk.Button(self.data_frame, text="\t", command=self.change_bgcolor)
        self.bgcolor_button.grid(row=3, column=1, sticky="nsw", padx=2, pady=2)
        
        self.edit_tag_button = ttk.Button(self.data_frame, text="Edit Tag", command=self.update_tag, state=tk.DISABLED)
        self.edit_tag_button.grid(row=4, column=0, columnspan=2, sticky="ew", padx=2, pady=2)
        
        self.assn_tag_tv.bind("<<TreeviewSelect>>", self.selection_change_tv)
        
        tk.Grid.columnconfigure(self.data_frame, 1, weight=1)
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        
        self.refresh()
        center_window_wrt(self, parent)
        
    def selection_change_tv(self, event=None):
        sel = self.assn_tag_tv.treeview.selection()
        if sel:
            item = self.assn_tag_tv.treeview.item(sel[0])
            self.selected_record = taglist_to_objects(item['values'])
            self.edit_tag_button["state"] = tk.NORMAL
            # update items
            self.tag_id.set(self.selected_record.id)
            self.tag_name.set(self.selected_record.text)
            self.fgcolor_button["bg"] = "#{}".format(self.selected_record.fgcolor) if self.selected_record.fgcolor else "SystemButtonFace"
            self.bgcolor_button["bg"] = "#{}".format(self.selected_record.bgcolor) if self.selected_record.bgcolor else "SystemButtonFace"
        else:
            self.edit_tag_button["state"] = tk.DISABLED
            self.tag_id.set("")
            self.tag_name.set("")
            self.fgcolor_button["bg"] = "SystemButtonFace"
            self.bgcolor_button["bg"] = "SystemButtonFace"
            self.selected_record = None
    
    def refresh(self):
        self.assn_tag_tv.clear()
        self.assn_tag_tv.extend(controller.list_tags())
    
    def change_fgcolor(self):
        c = colorchooser.askcolor()[1]
        self.fgcolor_button["bg"] = "SystemButtonFace" if c=="#000000" else c
    
    def change_bgcolor(self):
        c = colorchooser.askcolor()[1]
        self.bgcolor_button["bg"] = "SystemButtonFace" if c=="#ffffff" else c
    
    def update_tag(self):
        controller.edit_tag(Tag(
            id=int(self.tag_id.get()),
            text=str(self.tag_name.get()),
            fgcolor=(self.fgcolor_button["bg"][1:]
                     if self.fgcolor_button["bg"] != "SystemButtonFace"
                     else None),
            bgcolor=(self.bgcolor_button["bg"][1:]
                     if self.bgcolor_button["bg"] != "SystemButtonFace"
                     else None)
        ))
        self.refresh()
        if callable(self.callback):
            self.callback()


class SendToMenu(tk.Toplevel):
    def __init__(self, parent, fp=None, callback=None, *a, **kw):
        tk.Toplevel.__init__(self, parent, *a, **kw)
        
        self.fp = fp
        self.callback = callback
        
        self.transient(parent)
        
        self.title("Send To")
        
        self.assn_tag_tv = SendToListFrame(self)
        self.assn_tag_tv.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=2, pady=2)
        
        self.populate()
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        center_window_wrt(self, parent)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.assn_tag_tv.treeview.bind("<<TreeviewSelect>>", self.sendto)
        
    def populate(self):
        for d in os.listdir(os.path.expanduser("~/AppData/Roaming/Microsoft/Windows/SendTo")):
            if d == "desktop.ini": continue
            self.assn_tag_tv.append((".".join(d.split(".")[:-1]), d))
        
    def sendto(self, event=None):
        if self.assn_tag_tv.treeview.selection():
            send_file(self.fp, self.assn_tag_tv.treeview.item(self.assn_tag_tv.treeview.selection()[0])['values'][1])
            self.fp.close()
            self.destroy()
    
    def on_closing(self, event=None):
        self.fp.close()
        self.destroy()