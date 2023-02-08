import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import scrolledtext
import webbrowser
from functools import partial

from gurutracker.views.listbox import AssignmentListFrame, TutorListFrame
from gurutracker.views.bars import ToolBar
from gurutracker.views.widgets import ToolbarButton, ToolbarMenubutton
from gurutracker.views import dialogs
from gurutracker.helpers.fileopener import filepath, valid_filepath, dirpath
import gurutracker.helpers.exporter
import gurutracker.views.helpers
import gurutracker.views.pdftools
from gurutracker.helpers.object_typecaster import list_to_objects, get_cobject_tags, tv_tag_config, color_treeview_item



class AssignmentBrowserFrame(tk.Frame):
    def __init__(self, parent, config, controller, *a, **kw):
        super().__init__(parent, *a, **kw)
        
        self.config = config
        self.controller = controller
        
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
        self.toolbar_view.pack()
        self.toolbar_open = ToolbarButton(self.toolbar, text="Open", command=self.open_current_record, state=tk.DISABLED)
        self.toolbar_open.pack()
        self.toolbar_edit = ToolbarButton(self.toolbar, text="Edit", command=self.edit_current_record, state=tk.DISABLED)
        self.toolbar_edit.pack()
        self.toolbar_del = ToolbarButton(self.toolbar, text="Delete", state=tk.DISABLED)
        self.toolbar_del.pack()
        self.toolbar_tags = ToolbarButton(self.toolbar, text="Tags", command=self.view_tags_current_record, state=tk.DISABLED)
        self.toolbar_tags.pack()

        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, anchor=tk.NW, fill='y', pady=2)

        self.toolbar_tools = ToolbarMenubutton(self.toolbar)
        self.toolbar_tools["text"] = "Tools \u25BE"
        self.toolbar_tools_menu = tk.Menu(self.toolbar_tools, tearoff=0)
        self.toolbar_tools["menu"] = self.toolbar_tools_menu
        self.toolbar_tools_menu.add_command(label="Open File Storage Location", command=self.show_datastore)
        self.toolbar_tools_menu.add_command(label="Associate File", command=self.associate_file_rec)
        self.toolbar_tools_menu.add_separator()
        self.toolbar_tools_menu.add_command(label="Query with Custom SQL", command=self.load_treeview_customsql)
        self.toolbar_tools_menu.add_command(label="Show/Hide Columns", state=tk.DISABLED)
        self.toolbar_tools_menu.add_command(label="Edit Tags", command=self.edit_tags_overall)
        self.toolbar_tools_menu.add_separator()
        self.pdf_tools_menu = tk.Menu(self.toolbar_tools_menu, tearoff=0)
        self.pdf_tools_menu.add_command(label="Images to PDF", command=self.images_to_pdf)
        self.pdf_tools_menu.add_command(label="Merge PDF")
        self.toolbar_tools_menu.add_cascade(label="PDF Tools", menu=self.pdf_tools_menu)
        # self.toolbar_tools_menu.add_separator()
        # self.toolbar_tools_menu.add_command(label="Export All Data", command=self.export_all)
        # self.toolbar_tools_menu.add_command(label="Import Data into Database", command=self.import_all)
        # self.toolbar_tools_menu.add_command(label="About", state=tk.DISABLED)
        self.toolbar_tools.pack()
        
        
        self.assn_lst = AssignmentListFrame(self)
        self.assn_lst.grid(row=1, column=0, sticky='nsew')
        self.assn_lst.treeview.bind('<<TreeviewSelect>>', self.tree_item_selected)
        self.assn_lst.treeview.bind('<Double-Button-1>', self.tv_double_click)
        self.assn_lst.treeview.bind('<Return>', self.tv_enter_key)

        # columns
        self.assn_lst.treeview["displaycolumns"] = self.config.getlist("gui.preferences", "mainwindow.AssignmentBrowserFrame.AssignmentListFrame.displaycolumns")
        
        # self.assn_lst.treeview.tag_configure("completed", foreground="#ffffff", background="#216021")
        # self.assn_lst.treeview.tag_configure("incomplete", foreground="#ffffff", background="#ff0000")
        # self.assn_lst.treeview.tag_raise("sel")
        #tags
        tv_tag_config(self.controller, self.assn_lst.treeview)
        
        self.__get_item_color = partial(color_treeview_item, self.controller)
        
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        
        self.refresh_treeview()
    
    def edit_tags_overall(self):
        dialogs.EditTags(self, self.config, self.controller, partial(tv_tag_config, self.controller, self.assn_lst.treeview))

    def do_nothing(self):
        pass
        
    def tv_double_click(self, event):
        getattr(self, self.config.get("gui.preferences", "mainwindow.AssignmentBrowserFrame.DoubleButton1.defaultaction"), self.view_current_record)()
    
    def tv_enter_key(self, event):
        getattr(self, self.config.get("gui.preferences", "mainwindow.AssignmentBrowserFrame.ReturnKey.defaultaction"), self.view_current_record)()
        
    def edit_current_record(self):
        if self.selected_record:
            dialogs.EditAssignment(self, self.config, self.controller, assignment=self.selected_record, callback=self.refresh_treeview)
    
    def open_current_record(self):
        if self.selected_record:
            if valid_filepath(self.config, self.selected_record.uidentifier):
                webbrowser.open_new(filepath(self.config, self.selected_record.uidentifier))
            else:
                messagebox.showerror("Error", "This record does not have any file assocated with it.")
        else:
            messagebox.showinfo("Info", "Please select a record.")
    
    def associate_file_rec(self):
        if self.selected_record:
            # if valid_filepath(self.config, self.selected_record.uidentifier):
            #     if not messagebox.askyesno("Warning", "A file is already present. This will OVERWRITE the file. Proceed?"):
            #         return
        
            fname = filedialog.askopenfilename(filetypes=[
                ('PDF Files', '*.pdf')])
            # if fname:
            #     path = filepath(self.config, self.selected_record.uidentifier)
            #     os.makedirs(os.path.split(path)[0], exist_ok=True)
            #     shutil.copy(fname, path)
            #     messagebox.showinfo("Success", "Success. Please refresh to open file")
            gurutracker.views.helpers.associate_file_with_record(self.config, self.selected_record, fname)
        else:
            messagebox.showinfo("Info", "Please select a record.")
    
    def view_tags_current_record(self):
        if self.selected_record:
            assn = self.selected_record
            cb = getattr(self, self.config.get("gui.preferences", "mainwindow.AssignmentBrowserFrame.ViewTagsDialog.onupdate"), self.refresh_treeview)
            dialogs.ViewTags(self, self.config, self.controller, assignment=self.selected_record, callback=cb)
        else:
            messagebox.showinfo("Info", "Please select a record.")

    def filter_assn(self):
        dialogs.FilterTags(self, self.config, self.controller, callback=self.load_data_treeview)
    
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
            item = self.assn_lst.treeview.item(sel[0])
            self.selected_record = list_to_objects(item['values'])
            
            # special checking for open
            if valid_filepath(self.config, self.selected_record.uidentifier):
                self.toolbar_open["state"] = tk.NORMAL
            else:
                self.toolbar_open["state"] = tk.DISABLED
        else:
            self.toolbar_view["state"] = tk.DISABLED
            self.toolbar_open["state"] = tk.DISABLED
            self.toolbar_edit["state"] = tk.DISABLED
            self.toolbar_del["state"] = tk.DISABLED
            self.toolbar_tags["state"] = tk.DISABLED
            self.selected_record = None
    
    def add_new(self):
        dialogs.NewAssignment(self, self.config, self.controller, callback=self.refresh_treeview)
    
    def refresh_treeview(self):
        self.toolbar_refresh["text"] = "Refresh"
        self.assn_lst.clear()
        self.assn_lst.extend(self.controller.list_all_assignments(), tag_func=self.__get_item_color)
        self.assn_lst.treeview.yview_moveto(1)

    def load_treeview_customsql(self):
        res = simpledialog.askstring("Enter SQL QUERY (leave ending semicolon)",
                                     "SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subject`, `tutor`.`level` FROM `assignment` JOIN `tutor` ON `assignment`.`tid` = `tutor`.`id`")
        if res:
            self.toolbar_refresh["text"] = "Clear"
            self.assn_lst.clear()
            self.assn_lst.extend(self.controller.list_all_assignments_customsql(res), tag_func=self.__get_item_color)
    
    def load_data_treeview(self, data):
        self.toolbar_refresh["text"] = "Clear"
        self.assn_lst.clear()
        self.assn_lst.extend(data, tag_func=self.__get_item_color)
        self.assn_lst.treeview.yview_moveto(1)
    
    def search_treeview_by_assnname(self):
        term = simpledialog.askstring("Search by Name", "Enter Assignment Name/Substring (escape % and _ characters):")
        if term is not None:
            self.assn_lst.clear()
            self.assn_lst.extend(self.controller.search_assignment_by_name_instr(term))
            self.assn_lst.treeview.yview_moveto(0)
            self.toolbar_refresh["text"] = "Clear Search"

    def search_treeview_by_uid(self):
        term = simpledialog.askstring("Search by UID", "Enter Assignment UID/Substring (escape % and _ characters):")
        if term is not None:
            self.assn_lst.clear()
            self.assn_lst.extend(self.controller.search_uid_by_name_instr(term))
            self.assn_lst.treeview.yview_moveto(0)
            self.toolbar_refresh["text"] = "Clear Search"
    
    def get_treeview_item_by_id(self):
        term = simpledialog.askinteger("Search by ID", "Enter Assignment ID")
        if term is not None:
            self.assn_lst.clear()
            res = self.controller.get_assignment_by_id(term)
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
            res = self.controller.get_assignment_by_uid(term)
            if res:
                self.assn_lst.extend((res,))
                self.assn_lst.treeview.yview_moveto(0)
            else:
                messagebox.showwarning("No Record Found", "The given record does not exist.")
            self.toolbar_refresh["text"] = "Clear Search"

    def show_datastore(self):
        if self.selected_record:
            print(filepath(self.config, "/".join(self.selected_record.uidentifier.split("/")[:1])))
            webbrowser.open_new(dirpath(self.config, self.selected_record.uidentifier))
        else:
            webbrowser.open_new(self.config.get("files", "datadir"))
    
    # def export_all(self):
    #     fname = filedialog.asksaveasfilename(filetypes=[
    #         ('Gurutracker eXport Package', '*.gxp')],
    #         defaultextension='.gxp')
    #     if fname:
    #         gurutracker.helpers.exporter.export(self.config, self.controller, fname)
    #         messagebox.showinfo("Finished", "Export finished.")
    
    # def import_all(self):
    #     cur = self.controller.con.cursor()
    #     cur.execute("SELECT COUNT(*) FROM tutor;")
        
    #     if cur.fetchone()[0] == 0:
    #         fname = filedialog.askopenfilename(filetypes=[
    #             ('Gurutracker eXport Package', '*.gxp')])
    #         if fname:
    #             try:
    #                 gurutracker.helpers.exporter.import_(self.config, self.controller, fname)
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
        gurutracker.views.pdftools.ImagesToPDF(self, self.config, self.controller, self.selected_record, self.refresh_treeview)


class TutorBrowserFrame(tk.Frame):
    def __init__(self, parent, config, controller, *a, **kw):
        super().__init__(parent, *a, **kw)
        
        self.config = config
        self.controller = controller
        
        self.selected_record = None 

        self.toolbar = ToolBar(self)
        self.toolbar.grid(row=0, column=0, sticky='nsew')
        
        self.toolbar_new = ToolbarButton(self.toolbar, text="New", command=self.add_new)
        self.toolbar_new.pack()
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, anchor=tk.NW, fill='y', pady=2)
        self.toolbar_view = ToolbarButton(self.toolbar, text="View", command=self.view_record)
        self.toolbar_view.pack()
        self.toolbar_edit = ToolbarButton(self.toolbar, text="Edit", state=tk.DISABLED)
        self.toolbar_edit.pack()
        
        
        self.tutor_list = TutorListFrame(self)
        self.tutor_list.grid(row=1, column=0, sticky='nsew')
        self.tutor_list.treeview.bind('<<TreeviewSelect>>', self.tree_item_selected)
        
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        
        self.tutor_list.extend(self.controller.list_tutors())
        
    def refresh_treeview(self):
        self.tutor_list.clear()
        self.tutor_list.extend(self.controller.list_tutors())
        
    def add_new(self):
        dialogs.NewTutor(self, self.config, self.controller, callback=self.refresh_treeview)
    
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
            # self.toolbar_edit["state"] = tk.NORMAL
            item = self.tutor_list.treeview.item(sel[0])
            self.selected_record = item['values']
        else:
            self.toolbar_view["state"] = tk.DISABLED
            # self.toolbar_edit["state"] = tk.DISABLED
            self.selected_record = None


class NotesFrame(tk.Frame):
    def __init__(self, parent, config, controller, *a, **kw):
        super().__init__(parent, *a, **kw)
        
        self.config = config
        self.controller = controller

        self.toolbar = ToolBar(self)
        self.toolbar.grid(row=0, column=0, sticky='nsew')
        
        self.toolbar_save = ToolbarButton(self.toolbar, text="Save", command=self.save_notes)
        self.toolbar_save.pack()
        
        self.content = scrolledtext.ScrolledText(self, height=10)
        self.content.grid(row=1, column=0, sticky=tk.NSEW)
        
        self.populate()
        
        if self.config.getboolean("notes", "autosave"):
            self.content.bind("<KeyRelease>", self.save_notes)
        else:
            self.content.bind("<KeyRelease>", self.save_indicate)
        
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
    
    def save_indicate(self, event=None):
        self.toolbar_save["text"] = "*Save"
    
    def populate(self):
        if os.path.isfile(self.config.get("notes", "textfile")): 
            with open(self.config.get("notes", "textfile")) as f:
                self.content.insert(tk.END, f.read())
    
    def save_notes(self, event=None):
        self.toolbar_save["text"] = "Save"
        with open(self.config.get("notes", "textfile"), "w") as f:
            f.write(self.content.get("1.0", "end-1c"))


class MainWindow(tk.Tk):
    def __init__(self, config, controller):
        super().__init__()
        
        self.config = config
        self.controller = controller
        
        self.selected_record = None
        
        # Tkinter starts...
        self.title("Gurutracker")
        
        self.menubar = tk.Menu(self, tearoff=0)
        self.window_menu = tk.Menu(self.menubar, tearoff=0)
        self.win_fullscreen_tkvar = tk.BooleanVar(self)
        self.win_fullscreen_tkvar.set(False)
        self.window_menu.add_checkbutton(label="Full Screen", command=self.toggle_full_screen,
                                         variable=self.win_fullscreen_tkvar,
                                         onvalue=True,
                                         offvalue=False)
        self.window_menu.add_separator()
        self.window_menu.add_command(label="Export All Data", command=self.export_all_data)
        self.window_menu.add_command(label="Import Data into Database", command=self.import_all_data)
        self.window_menu.add_separator()
        self.window_menu.add_command(label="Exit", command=self.destroy)
        self.menubar.add_cascade(label="Application", menu=self.window_menu)
        tk.Tk.config(self, menu=self.menubar)
        
        self.notebook = ttk.Notebook(self)
        
        self.assignment_frame = AssignmentBrowserFrame(self.notebook, self.config, self.controller)
        self.assignment_frame.pack(fill= tk.BOTH, expand=True)
        self.notebook.add(self.assignment_frame, text="Assignments")
        
        self.tutor_frame = TutorBrowserFrame(self.notebook, self.config, self.controller)
        self.tutor_frame.pack(fill= tk.BOTH, expand=True)
        self.notebook.add(self.tutor_frame, text="Tutors")
        
        if self.config.getboolean("notes", "enabled"):
            self.notes_frame = NotesFrame(self.notebook, self.config, self.controller)
            self.notes_frame.pack(fill= tk.BOTH, expand=True)
            self.notebook.add(self.notes_frame, text="Notes")
        
        self.notebook.pack(fill= tk.BOTH, expand=True)
        
        # auto full screen
        if self.config.getboolean("gui.preferences", "mainwindow.onStartup.launchFullScreen"):
            self.win_fullscreen_tkvar.set(True)
            self.toggle_full_screen()
        
    def toggle_full_screen(self):
        self.attributes("-fullscreen", self.win_fullscreen_tkvar.get())
    
    def export_all_data(self):
        fname = filedialog.asksaveasfilename(filetypes=[
            ('Gurutracker eXport Package', '*.gxp')],
            defaultextension='.gxp')
        if fname:
            gurutracker.helpers.exporter.export(self.config, self.controller, fname)
            messagebox.showinfo("Finished", "Export finished.")
    
    def import_all_data(self):
        cur = self.controller.con.cursor()
        cur.execute("SELECT COUNT(*) FROM tutor;")
        
        if cur.fetchone()[0] == 0:
            fname = filedialog.askopenfilename(filetypes=[
                ('Gurutracker eXport Package', '*.gxp')])
            if fname:
                try:
                    gurutracker.helpers.exporter.import_(self.config, self.controller, fname)
                except gurutracker.helpers.exporter.VersionMismatchError:
                    messagebox.showerror("Error", "This file is of an unsupported GXP version.")
                except:
                    messagebox.showerror("Error", "This file is corrupted.")
                else:
                    messagebox.showinfo("Finished", "Import finished. Restart app to see effect.")
        else:
            messagebox.showerror("Error", "Import only possible in fresh install")
            
        cur.close()
