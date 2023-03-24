import os
import re
import platform
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import scrolledtext
import webbrowser
from functools import partial

from gurutracker.globals import settings, controller, storage
from gurutracker.storage.base import FileLinkageError
from gurutracker.views.listbox import AssignmentListFrame, TutorListFrame, SubjectListFrame
from gurutracker.views.bars import ToolBar
from gurutracker.views.widgets import ToolbarButton, ToolbarMenubutton
from gurutracker.views import dialogs
from gurutracker.helpers.fileopener import filepath, dirpath
from gurutracker.helpers.storage import open_file
import gurutracker.helpers.exporter
import gurutracker.views.helpers
import gurutracker.views.pdftools
from gurutracker.helpers.object_typecaster import list_to_objects, tv_tag_config, color_treeview_item
from gurutracker.database import objects


NAME_VALIDATION_REGEX=r"[a-zA-Z0-9\(\) ]+"
UID_VALIDATION_REGEX=r"[A-Z0-9]+"


class AssignmentBrowserFrame(tk.Frame):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, *a, **kw)
        
        self.selected_record = None 

        self.toolbar = ToolBar(self)
        self.toolbar.grid(row=0, column=0, sticky='nsew')
        
        self.toolbar_new = ToolbarButton(self.toolbar, text="New", command=self.add_new)
        self.toolbar_new.pack()
        self.toolbar_refresh = ToolbarButton(self.toolbar, text="Refresh", command=self.refresh_treeview) # text changed in comand
        self.toolbar_refresh.pack()
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, anchor=tk.NW, fill='y', pady=2)
        
        self.toolbar_search = ToolbarMenubutton(self.toolbar)
        self.toolbar_search["text"] = "Search"
        self.toolbar_search_menu = tk.Menu(self.toolbar_search, tearoff=0)
        self.toolbar_search["menu"] = self.toolbar_search_menu
        self.toolbar_search_menu.add_command(label="Find by", state=tk.DISABLED)
        self.toolbar_search_menu.add_command(label="Assignment ID", command=self.get_treeview_item_by_id)
        self.toolbar_search_menu.add_command(label="Assignment UID", command=self.get_treeview_item_by_uid)
        self.toolbar_search_menu.add_separator()
        self.toolbar_search_menu.add_command(label="Search by", state=tk.DISABLED)
        self.toolbar_search_menu.add_command(label="Assignment UID", command=self.search_treeview_by_uid)
        self.toolbar_search_menu.add_command(label="Assignment Name", command=self.search_treeview_by_assnname)
        self.toolbar_search.pack()
        
        self.toolbar_filter = ToolbarButton(self.toolbar, text="Filter", command=self.filter_assn)
        self.toolbar_filter.pack()
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, anchor=tk.NW, fill='y', pady=2)
        self.toolbar_view = ToolbarButton(self.toolbar, text="View", command=self.view_current_record, state=tk.DISABLED)
        # self.toolbar_view.pack()
        self.toolbar_open = ToolbarButton(self.toolbar, text="Open", command=self.open_current_record, state=tk.DISABLED)
        # self.toolbar_open.pack()
        self.toolbar_edit = ToolbarButton(self.toolbar, text="Edit", command=self.edit_current_record, state=tk.DISABLED)
        self.toolbar_edit.pack()
        self.toolbar_del = ToolbarButton(self.toolbar, text="Delete", command=self.del_record, state=tk.DISABLED)
        self.toolbar_del.pack()
        self.toolbar_tags = ToolbarButton(self.toolbar, text="Tags", command=self.view_tags_current_record, state=tk.DISABLED)
        self.toolbar_tags.pack()

        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, anchor=tk.NW, fill='y', pady=2)
        
        self.toolbar_files = ToolbarMenubutton(self.toolbar, text="Files", state=tk.DISABLED)
        self.toolbar_files_menu = tk.Menu(self.toolbar_files, tearoff=0)
        self.toolbar_files["menu"] = self.toolbar_files_menu
        self.toolbar_files_menu.add_command(label="Link File", command=self.associate_file_rec)
        self.toolbar_files_menu.add_command(label="View File", command=self.open_current_record)
        self.toolbar_files_menu.add_command(label="Unlink File", command=self.disassociate_file_rec)
        if platform.system() == "Windows" and settings.getboolean("gui.preferences", "mainwindow.ToolBar.FilesToolbarMenubutton.showSendToOption"):
            self.toolbar_files_menu.add_separator()
            self.toolbar_files_menu.add_command(label="Send To", command=self.file_send_to)
        self.toolbar_files.pack()
        

        self.toolbar_tools = ToolbarMenubutton(self.toolbar)
        self.toolbar_tools["text"] = "Tools \u25BE"
        self.toolbar_tools_menu = tk.Menu(self.toolbar_tools, tearoff=0)
        self.toolbar_tools["menu"] = self.toolbar_tools_menu
        # self.toolbar_tools_menu.add_command(label="Open File Storage Location", command=self.show_datastore)
        # self.toolbar_tools_menu.add_command(label="Associate File", command=self.associate_file_rec)
        # self.toolbar_tools_menu.add_separator()
        # self.toolbar_tools_menu.add_command(label="Query with Custom SQL", command=self.load_treeview_customsql)
        # self.toolbar_tools_menu.add_command(label="Show/Hide Columns", state=tk.DISABLED)
        self.toolbar_tools_menu.add_command(label="Edit Tags", command=self.edit_tags_overall)
        # self.toolbar_tools_menu.add_separator()
        # self.pdf_tools_menu = tk.Menu(self.toolbar_tools_menu, tearoff=0)
        # self.pdf_tools_menu.add_command(label="Images to PDF", command=self.images_to_pdf)
        # self.pdf_tools_menu.add_command(label="Merge PDF")
        # self.toolbar_tools_menu.add_cascade(label="PDF Tools", menu=self.pdf_tools_menu)
        # self.toolbar_tools_menu.add_separator()
        # self.toolbar_tools_menu.add_command(label="Export All Data", command=self.export_all)
        # self.toolbar_tools_menu.add_command(label="Import Data into Database", command=self.import_all)
        # self.toolbar_tools_menu.add_command(label="About", state=tk.DISABLED)
        self.toolbar_tools.pack(side=tk.RIGHT)
        
        
        self.assn_lst = AssignmentListFrame(self)
        self.assn_lst.grid(row=1, column=0, sticky='nsew')
        self.assn_lst.treeview.bind('<<TreeviewSelect>>', self.tree_item_selected)
        self.assn_lst.treeview.bind('<Double-Button-1>', self.tv_double_click)
        self.assn_lst.treeview.bind('<Return>', self.tv_enter_key)

        # columns
        self.assn_lst.treeview["displaycolumns"] = settings.getlist("gui.preferences", "mainwindow.AssignmentBrowserFrame.AssignmentListFrame.displaycolumns")
        
        # self.assn_lst.treeview.tag_configure("completed", foreground="#ffffff", background="#216021")
        # self.assn_lst.treeview.tag_configure("incomplete", foreground="#ffffff", background="#ff0000")
        # self.assn_lst.treeview.tag_raise("sel")
        #tags
        tv_tag_config( self.assn_lst.treeview)
        
        self.__get_item_color = color_treeview_item
        
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        
        self.refresh_treeview()
    
    def edit_tags_overall(self):
        dialogs.EditTags(self, partial(tv_tag_config, self.assn_lst.treeview))

    def do_nothing(self):
        pass
        
    def tv_double_click(self, event):
        getattr(self, settings.get("gui.preferences", "mainwindow.AssignmentBrowserFrame.DoubleButton1.defaultaction"), self.view_current_record)()
    
    def tv_enter_key(self, event):
        getattr(self, settings.get("gui.preferences", "mainwindow.AssignmentBrowserFrame.ReturnKey.defaultaction"), self.open_current_record)()
        
    def edit_current_record(self):
        if self.selected_record:
            dialogs.EditAssignment(self, assignment=self.selected_record, callback=self.refresh_treeview)
    
    def del_record(self):
        if self.selected_record:
            doit = messagebox.askyesno("Confirmation", "Are you sure you want to delete this assignment? This action is irreversible.")
            if doit:
                storage.unlink_file(self.selected_record)
                controller.del_assignment(self.selected_record)
                self.refresh_treeview()
    
    def open_current_record(self):
        if self.selected_record:
            if storage.has_linked_file(self.selected_record):
                f = storage.get_file(self.selected_record)
                open_file(f)
                f.close()
            else:
                messagebox.showerror("Error", "This record does not have any file assocated with it.")
        else:
            messagebox.showinfo("Info", "Please select a record.")
    
    def file_send_to(self):
        if self.selected_record:
            if storage.has_linked_file(self.selected_record):
                f = storage.get_file(self.selected_record)
                dialogs.SendToMenu(self, f)
                # f.close()
            else:
                messagebox.showerror("Error", "This record does not have any file assocated with it.")
        else:
            messagebox.showinfo("Info", "Please select a record.")
    
    def disassociate_file_rec(self):
        if self.selected_record:
            if storage.has_linked_file(self.selected_record):
                c = messagebox.askyesno("Confirmation", "Deleted files are deleted forever. Are you sure?")
                if c:
                    storage.unlink_file(self.selected_record)
                    self.refresh_treeview()
            else:
                messagebox.showerror("Error", "This record does not have any file assocated with it.")
        else:
            messagebox.showinfo("Info", "Please select a record.")
    
    def associate_file_rec(self):
        if self.selected_record:
            # if valid_filepath(self.config, self.selected_record.uidentifier):
            #     if not messagebox.askyesno("Warning", "A file is already present. This will OVERWRITE the file. Proceed?"):
            #         return
            if storage.has_linked_file(self.selected_record):
                if not messagebox.askyesno("Warning", "A file is already present. This will OVERWRITE the file. Proceed?"):
                    return
        
            fname = filedialog.askopenfilename(filetypes=[
                ('All Files', '*.*')])
            
            if fname:
                f = open(fname, "rb")
                try:
                    storage.link_file(f, self.selected_record)
                except FileLinkageError as e:
                    messagebox.showerror("Failed to link file", "The system failed to link the file.")
                else:
                    messagebox.showinfo("Success", "Linked file. Refresh for changes to reflect.")
        else:
            messagebox.showinfo("Info", "Please select a record.")
    
    def view_tags_current_record(self):
        if self.selected_record:
            cb = getattr(self, settings.get("gui.preferences", "mainwindow.AssignmentBrowserFrame.ViewTagsDialog.onupdate"), self.refresh_treeview)
            dialogs.ViewTags(self, assignment=self.selected_record, callback=cb)
        else:
            messagebox.showinfo("Info", "Please select a record.")

    def filter_assn(self):
        dialogs.FilterTags(self, callback=self.load_data_treeview)
    
    def view_current_record(self):
        if self.selected_record:
            t = self.selected_record
            tot = zip(("assignment.id", "assignment.name", "assignment.uidentifier", "assignment.type", "tutor.id", "tutor.name", "tutor.uidentifier", "tutor.subject", "tutor.level"), (t.id, t.name, t.uidentifier, t.type, t.tutor.id, t.tutor.name, t.tutor.uidentifier, t.tutor.subject, t.tutor.level))
            op = "\n".join(["{}: {}".format(k, v) for k, v in tot])
            
            messagebox.showinfo("Selected Record Details", op)
        else:
            messagebox.showinfo("Info", "Please select a record.")
    
    def tree_item_selected(self, event):
        sel = self.assn_lst.treeview.selection()
        if sel:
            self.toolbar_view["state"] = tk.NORMAL
            self.toolbar_edit["state"] = tk.NORMAL
            self.toolbar_del["state"] = tk.NORMAL
            self.toolbar_tags["state"] = tk.NORMAL
            self.toolbar_files["state"] = tk.NORMAL
            item = self.assn_lst.treeview.item(sel[0])
            self.selected_record = objects.Assignment.from_list(item['values'])
            
            # special checking for open
            if storage.has_linked_file(self.selected_record):
                self.toolbar_open["state"] = tk.NORMAL
            else:
                self.toolbar_open["state"] = tk.DISABLED
        else:
            self.toolbar_view["state"] = tk.DISABLED
            self.toolbar_open["state"] = tk.DISABLED
            self.toolbar_edit["state"] = tk.DISABLED
            self.toolbar_del["state"] = tk.DISABLED
            self.toolbar_tags["state"] = tk.DISABLED
            self.toolbar_files["state"] = tk.DISABLED
            self.selected_record = None
    
    def add_new(self):
        dialogs.NewAssignment(self, callback=self.refresh_treeview)
    
    def refresh_treeview(self):
        self.toolbar_refresh["text"] = "Refresh"
        self.assn_lst.clear()
        self.assn_lst.extend(controller.list_all_assignments(), tag_func=self.__get_item_color)
        self.assn_lst.treeview.yview_moveto(1)

    def load_treeview_customsql(self):
        res = simpledialog.askstring("Enter SQL QUERY (leave ending semicolon)",
                                     "SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subject`, `tutor`.`level` FROM `assignment` JOIN `tutor` ON `assignment`.`tid` = `tutor`.`id`")
        if res:
            self.toolbar_refresh["text"] = "Clear"
            self.assn_lst.clear()
            self.assn_lst.extend(controller.list_all_assignments_customsql(res), tag_func=self.__get_item_color)
    
    def load_data_treeview(self, data):
        self.toolbar_refresh["text"] = "Clear"
        self.assn_lst.clear()
        self.assn_lst.extend(data, tag_func=self.__get_item_color)
        self.assn_lst.treeview.yview_moveto(1)
    
    def search_treeview_by_assnname(self):
        term = simpledialog.askstring("Search by Name", "Enter Assignment Name/Substring (escape % and _ characters):")
        if term is not None:
            self.assn_lst.clear()
            self.assn_lst.extend(controller.search_assignment_by_name_instr(term))
            self.assn_lst.treeview.yview_moveto(0)
            self.toolbar_refresh["text"] = "Clear Search"

    def search_treeview_by_uid(self):
        term = simpledialog.askstring("Search by UID", "Enter Assignment UID/Substring (escape % and _ characters):")
        if term is not None:
            self.assn_lst.clear()
            self.assn_lst.extend(controller.search_uid_by_name_instr(term))
            self.assn_lst.treeview.yview_moveto(0)
            self.toolbar_refresh["text"] = "Clear Search"
    
    def get_treeview_item_by_id(self):
        term = simpledialog.askinteger("Search by ID", "Enter Assignment ID")
        if term is not None:
            self.assn_lst.clear()
            res = controller.get_assignment_by_id(term)
            if res:
                self.assn_lst.extend((res,))
                self.assn_lst.treeview.yview_moveto(0)
            else:
                messagebox.showwarning("No Record Found", "The given record does not exist.")
            self.toolbar_refresh["text"] = "Clear Search"
    
    def get_treeview_item_by_uid(self):
        term = simpledialog.askstring("Search by UID", "Enter Assignment UID")
        if term is not None:
            self.assn_lst.clear()
            res = controller.get_assignment_by_uid(term)
            if res:
                self.assn_lst.extend((res,))
                self.assn_lst.treeview.yview_moveto(0)
            else:
                messagebox.showwarning("No Record Found", "The given record does not exist.")
            self.toolbar_refresh["text"] = "Clear Search"

    def show_datastore(self):
        if self.selected_record:
            print(filepath(settings, "/".join(self.selected_record.uidentifier.split("/")[:1])))
            webbrowser.open_new(dirpath(settings, self.selected_record.uidentifier))
        else:
            webbrowser.open_new(settings.get("files", "datadir"))
    
    # def export_all(self):
    #     fname = filedialog.asksaveasfilename(filetypes=[
    #         ('Gurutracker eXport Package', '*.gxp')],
    #         defaultextension='.gxp')
    #     if fname:
    #         gurutracker.helpers.exporter.export(self.config, controller, fname)
    #         messagebox.showinfo("Finished", "Export finished.")
    
    # def import_all(self):
    #     cur = controller.con.cursor()
    #     cur.execute("SELECT COUNT(*) FROM tutor;")
        
    #     if cur.fetchone()[0] == 0:
    #         fname = filedialog.askopenfilename(filetypes=[
    #             ('Gurutracker eXport Package', '*.gxp')])
    #         if fname:
    #             try:
    #                 gurutracker.helpers.exporter.import_(self.config, controller, fname)
    #             except gurutracker.helpers.exporter.VersionMismatchError:
    #                 messagebox.showerror("Error", "This file is of an unsupported GXP version.")
    #             except:
    #                 messagebox.showerror("Error", "This file is corrupted.")
    #             else:
    #                 messagebox.showinfo("Finished", "Import finished.")
    #     else:
    #         messagebox.showerror("Error", "Import only possible in fresh install")
            
    #     cur.close()

    def images_to_pdf(self):
        gurutracker.views.pdftools.ImagesToPDF(self, self.selected_record, self.refresh_treeview)


class TutorBrowserFrame(tk.Frame):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, *a, **kw)
        
        self.selected_record = None 

        self.toolbar = ToolBar(self)
        self.toolbar.grid(row=0, column=0, sticky='nsew')
        
        self.toolbar_new = ToolbarButton(self.toolbar, text="New", command=self.add_new)
        self.toolbar_new.pack()
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, anchor=tk.NW, fill='y', pady=2)
        self.toolbar_view = ToolbarButton(self.toolbar, text="View", command=self.view_record, state=tk.DISABLED)
        self.toolbar_view.pack()
        self.toolbar_edit = ToolbarButton(self.toolbar, text="Edit", command=self.edit_record, state=tk.DISABLED)
        self.toolbar_edit.pack()
        self.toolbar_del = ToolbarButton(self.toolbar, text="Delete", command=self.del_record, state=tk.DISABLED)
        self.toolbar_del.pack()
        
        self.tutor_list = TutorListFrame(self)
        self.tutor_list.grid(row=1, column=0, sticky='nsew')
        self.tutor_list.treeview.bind('<<TreeviewSelect>>', self.tree_item_selected)
        
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        
        self.tutor_list.extend(controller.list_tutors())
        
    def refresh_treeview(self):
        self.tutor_list.clear()
        self.tutor_list.extend(controller.list_tutors())
        
    def add_new(self):
        dialogs.NewTutor(self, callback=self.refresh_treeview)
        
    def edit_record(self):
        if self.selected_record:
            tuto = objects.Tutor(id=int(self.selected_record[0]),
                                 name=self.selected_record[1],
                                 uidentifier=self.selected_record[2],
                                 subject=objects.Subject(
                                     id=int(self.selected_record[3]),
                                     name=self.selected_record[4],
                                     desc=self.selected_record[5],
                                     uidentifier=self.selected_record[6]
                                 ))
            dialogs.EditTutor(self, tutor=tuto, callback=self.refresh_treeview)
    
    def del_record(self):
        if self.selected_record:
            doit = messagebox.askyesno("Confirmation", "Are you sure you want to delete this tutor? This action is irreversible.")
            if doit:
                tuto = objects.Tutor(id=int(self.selected_record[0]))
                controller.delete_tutor(tuto)
                self.refresh_treeview()
    
    def view_record(self):
        if self.selected_record:
            tot = zip(("tutor.id", "tutor.name", "tutor.uidentifier", "tutor.subject", "tutor.level"), self.selected_record)
            op = "\n".join(["{}: {}".format(k, v) for k, v in tot])
            
            messagebox.showinfo("Selected Record Details", op)
        else:
            messagebox.showinfo("Info", "Please select a record.")
        
    def tree_item_selected(self, event):
        sel = self.tutor_list.treeview.selection()
        if sel:
            self.toolbar_view["state"] = tk.NORMAL
            self.toolbar_edit["state"] = tk.NORMAL
            self.toolbar_del["state"] = tk.NORMAL
            item = self.tutor_list.treeview.item(sel[0])
            self.selected_record = item['values']
        else:
            self.toolbar_view["state"] = tk.DISABLED
            self.toolbar_edit["state"] = tk.DISABLED
            self.toolbar_del["state"] = tk.DISABLED
            self.selected_record = None


class NotesFrame(tk.Frame):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, *a, **kw)

        self.toolbar = ToolBar(self)
        self.toolbar.grid(row=0, column=0, sticky='nsew')
        
        self.toolbar_save = ToolbarButton(self.toolbar, text="Save", command=self.save_notes)
        self.toolbar_save.pack()
        
        self.content = scrolledtext.ScrolledText(self, height=10)
        self.content.grid(row=1, column=0, sticky=tk.NSEW)
        
        self.populate()
        
        if settings.getboolean("notes", "autosave"):
            self.content.bind("<KeyRelease>", self.save_notes)
        else:
            self.content.bind("<KeyRelease>", self.save_indicate)
        
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
    
    def save_indicate(self, event=None):
        self.toolbar_save["text"] = "*Save"
    
    def populate(self):
        if os.path.isfile(os.path.expanduser(settings.get("notes", "textfile"))): 
            with open(os.path.expanduser(settings.get("notes", "textfile"))) as f:
                self.content.insert(tk.END, f.read())
    
    def save_notes(self, event=None):
        self.toolbar_save["text"] = "Save"
        with open(os.path.expanduser(settings.get("notes", "textfile")), "w") as f:
            f.write(self.content.get("1.0", "end-1c"))


class SubjectFrame(ttk.Frame):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, *a, **kw)
        
        
        self.pw = tk.PanedWindow(self, orient =tk.HORIZONTAL)
        self.pw.grid(row=1, column=0, sticky=tk.NSEW)
        self.pw.configure(sashrelief=tk.RAISED)
        
        self.subjects = SubjectListFrame(self.pw)
        self.subjects.pack(fill=tk.BOTH, expand=True)
        self.pw.add(self.subjects)
        
        self.data_frame = ttk.Frame(self.pw)
        self.pw.add(self.data_frame)
        
        tk.Grid.columnconfigure(self.data_frame, 1, weight=1)
        tk.Grid.rowconfigure(self.data_frame, 2, weight=1)
        
        ttk.Label(self.data_frame, text="Subject ID").grid(row=0, column=0, sticky=tk.NSEW, padx=2, pady=2)
        self.sub_id = tk.StringVar()
        ttk.Entry(self.data_frame, textvariable=self.sub_id, state="readonly").grid(row=0, column=1, sticky=tk.NSEW, padx=2, pady=2)
        
        ttk.Label(self.data_frame, text="Subject Name").grid(row=1, column=0, sticky=tk.NSEW, padx=2, pady=2)
        self.sub_name = tk.StringVar()
        ttk.Entry(self.data_frame, textvariable=self.sub_name).grid(row=1, column=1, sticky=tk.NSEW, padx=2, pady=2)
        
        ttk.Label(self.data_frame, text="Subject Description").grid(row=2, column=0, sticky="new", padx=2, pady=2)
        self.sub_desc = scrolledtext.ScrolledText(self.data_frame, width=20, height=5)
        self.sub_desc.grid(row=2, column=1, sticky=tk.NSEW, padx=2, pady=2)
        
        ttk.Label(self.data_frame, text="Subject UID").grid(row=3, column=0, sticky=tk.NSEW, padx=2, pady=2)
        self.sub_uid = tk.StringVar()
        ttk.Entry(self.data_frame, textvariable=self.sub_uid).grid(row=3, column=1, sticky=tk.NSEW, padx=2, pady=2)
        
        self.toolbar = ToolBar(self.data_frame)
        self.toolbar.grid(row=4, column=0, columnspan=2, sticky='sew')
        
        self.toolbar_del = ToolbarButton(self.toolbar, text="Delete", state=tk.DISABLED, command=self.delete_subject)
        self.toolbar_del.pack(side=tk.RIGHT)
        
        self.toolbar_edit = ToolbarButton(self.toolbar, text="Edit", state=tk.DISABLED, command=self.edit_selected)
        self.toolbar_edit.pack(side=tk.RIGHT)
        
        ttk.Label(self.toolbar, text="With Selected: ").pack(side=tk.RIGHT)
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.RIGHT, anchor=tk.NW, fill='y', pady=2)
        
        self.toolbar_new = ToolbarButton(self.toolbar, text="New", command=self.add_new)
        self.toolbar_new.pack(side=tk.RIGHT)
        
        self.toolbar_refresh = ToolbarButton(self.toolbar, text="Refresh", command=self.refresh_form)
        self.toolbar_refresh.pack(side=tk.LEFT)
        
        self.subjects.treeview.bind('<<TreeviewSelect>>', self.tree_item_selected)
        # self.assn_lst.treeview.bind('<Double-Button-1>', self.tv_double_click)
        # self.assn_lst.treeview.bind('<Return>', self.tv_enter_key)
        
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.rowconfigure(self, 1, weight=1)
        self.populate_treeview()
        
    def populate_treeview(self):
        self.subjects.clear()
        self.subjects.extend(controller.list_all_subjects())
        
    def clear_fields(self):
        self.sub_id.set("")
        self.sub_name.set("")
        self.sub_desc.delete("0.0", "end")
        self.sub_uid.set("")
    
    def refresh_form(self):
        self.populate_treeview()
        self.clear_fields()
        
    def validate(self, checktype="N"):
        errors = ""
        sid = self.sub_id.get().strip()
        snam = self.sub_name.get().strip()
        sdesc=self.sub_desc.get("0.0", "end-1c").strip()
        uid = self.sub_uid.get().strip()
        
        if not snam:
            errors += "* Please enter subject name\n"
        elif not re.fullmatch(NAME_VALIDATION_REGEX, snam):
            errors += f"* The subject name must match the regular expression {NAME_VALIDATION_REGEX}.\n"
            
        if not sdesc:
            errors += "* Please enter the description of subject.\n"
            
        if not uid:
            errors += "* Please enter the Unique Identifier.\n"
        elif not re.fullmatch(UID_VALIDATION_REGEX, uid):
            errors += f"* The UID must be in all caps and can only contain letters A-Z, numbers 0-9.\n"
        elif (checktype == "N" or not sid) and controller.get_subject_by_uid(uid): # checktype new
            errors += "* That UID is already taken. Please use another UID.\n"
        elif checktype == "E" and sid: # edit
            sub = controller.get_subject_by_uid(uid)
            if sub and sub.id != int(sid):
                errors += "* That UID is already taken. Either use the same UID or pick a new one."
        
        if errors:
            messagebox.showerror("Validation Error", errors)
        
        return not errors
    
    def add_new(self):
        if self.validate("N"):
            sub = objects.Subject(name=self.sub_name.get(),
                                desc=self.sub_desc.get("0.0", "end-1c"),
                                uidentifier=self.sub_uid.get())
            controller.add_subject(sub)
            self.populate_treeview()
            self.clear_fields()
    
    def edit_selected(self):
        if self.validate("E"):
            sub = objects.Subject(id=int(self.sub_id.get()),
                                name=self.sub_name.get(),
                                desc=self.sub_desc.get("0.0", "end-1c"),
                                uidentifier=self.sub_uid.get())
            controller.edit_subject(sub)
            self.populate_treeview()
            self.clear_fields()
        
    def delete_subject(self):
        if self.sub_id.get().strip():
            controller.delete_subject(objects.Subject(id=int(self.subjects.treeview.item(
                self.subjects.treeview.selection()[0])['values'][0])))
            self.clear_fields()
            self.populate_treeview()
    
    def tree_item_selected(self, event=None):
        sel = self.subjects.treeview.selection()
        if sel:
            item = self.subjects.treeview.item(sel[0])['values']
            self.sub_id.set(item[0])
            self.sub_name.set(item[1])
            self.sub_desc.delete("0.0", "end")
            self.sub_desc.insert("end", item[2])
            self.sub_uid.set(item[3])
            self.toolbar_edit['state'] = tk.NORMAL
            self.toolbar_del['state'] = tk.NORMAL
        else:
            self.clear_fields()
            self.toolbar_edit['state'] = tk.DISABLED
            self.toolbar_del['state'] = tk.DISABLED