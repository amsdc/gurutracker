import os
import platform
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import webbrowser

from PIL import ImageTk, Image

from gurutracker.globals import settings, controller, module_path
import gurutracker.helpers.exporter
from gurutracker.helpers import appdata, netconnection
from gurutracker.helpers.appdata.interface import AppdataProgressWindow as ImportToplevel
from gurutracker.views import frames


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.selected_record = None
        
        # Tkinter starts...
        self.title("Gurutracker")
        self.__icon = ImageTk.PhotoImage(Image.open(os.path.join(module_path, "resources", "icons", "app128.png")))
        self.iconphoto(True, self.__icon)
        
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
        self.tabs_menu = tk.Menu(self.menubar, tearoff=0)
        self.tabs_menu.add_command(label="Assignment Manager", command=self.subject_manager)
        self.tabs_menu.add_command(label="Tutor Manager", command=self.tutor_manager)
        self.tabs_menu.add_command(label="Subject Manager", command=self.subject_manager)
        if settings.getboolean("notes", "enabled"):
            self.tabs_menu.add_command(label="Notes", command=self.notes_manager)
        self.tabs_menu.add_separator()
        self.tabs_menu.add_command(label="Close Tab", command=self.close_tab)
        self.menubar.add_cascade(label="Tabs", menu=self.tabs_menu)
        self.help_menu = tk.Menu(tearoff=0)
        self.help_menu.add_command(label="Help Topics", accelerator="F1", command=self.launch_help)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About Gurutracker")
        self.help_menu.add_command(label="About AMSDC")
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        tk.Tk.config(self, menu=self.menubar)
        
        # help menu
        self.bind_all("<Key-F1>", self.launch_help)
        
        self.notebook = ttk.Notebook(self)
        self.notebook.enable_traversal()
        
        # frames list
        self.tabframe_dict = {} # indexes of tabs
        
        assignment_frame = frames.AssignmentBrowserFrame(self.notebook)
        assignment_frame.pack(fill= tk.BOTH, expand=True)
        self.notebook.add(assignment_frame, text="Assignments")
        self.tabframe_dict["assignment_frame"] = assignment_frame
        
        
        
        # if settings.getboolean("notes", "enabled"):
        #     self.notes_frame = NotesFrame(self.notebook)
        #     self.notes_frame.pack(fill= tk.BOTH, expand=True)
        #     self.notebook.add(self.notes_frame, text="Notes")
        
        self.notebook.pack(fill= tk.BOTH, expand=True)
        
        # auto full screen
        if settings.getboolean("gui.preferences", "mainwindow.onStartup.launchFullScreen"):
            self.win_fullscreen_tkvar.set(True)
            self.toggle_full_screen()
            
    def launch_help(self, event=None):
        if netconnection.is_connected("amsdc.github.io"):
            webbrowser.open_new("https://amsdc.github.io/gurutracker/")
        elif platform.system() == "Windows" and \
                os.path.isfile(os.path.join(module_path, "resources", "help", "help.chm")):
            webbrowser.open_new(os.path.join(module_path, "resources", "help", "help.chm"))
        else:
            messagebox.showinfo("Internet connection required",
                                "Please connect to the Internet to view online help.")
        
    def close_tab(self):
        if self.notebook.index(self.notebook.select()) >= 1:
            self.notebook.forget("current")
        else:
            messagebox.showerror("Error", "Defalult tabs cannot be closed.")
    
    def subject_manager(self):
        df = frames.SubjectFrame(self.notebook)
        df.pack(fill= tk.BOTH, expand=True)
        self.notebook.add(df, text="Subjects")
        self.notebook.select(len(self.notebook.tabs())-1)
        
    def tutor_manager(self):
        if "tutor_frame" in self.tabframe_dict:
            self.tabframe_dict["tutor_frame"].destroy()
            self.tabframe_dict.pop("tutor_frame")
        tutor_frame = frames.TutorBrowserFrame(self.notebook)
        tutor_frame.pack(fill= tk.BOTH, expand=True)
        self.notebook.add(tutor_frame, text="Tutors")
        self.tabframe_dict["tutor_frame"] = tutor_frame
        self.notebook.select(len(self.notebook.tabs())-1)
    
    def notes_manager(self):
        if "notes_frame" in self.tabframe_dict:
            self.tabframe_dict["notes_frame"].destroy()
            self.tabframe_dict.pop("notes_frame")
        notes_frame = frames.NotesFrame(self.notebook)
        notes_frame.pack(fill= tk.BOTH, expand=True)
        self.notebook.add(notes_frame, text="Notes")
        self.tabframe_dict["notes_frame"] = notes_frame
        self.notebook.select(len(self.notebook.tabs())-1)
        
    def toggle_full_screen(self):
        self.attributes("-fullscreen", self.win_fullscreen_tkvar.get())
    
    def export_all_data(self):
        fname = filedialog.asksaveasfilename(filetypes=[
            ('Gurutracker eXport Package', '*.gxp')],
            defaultextension='.gxp')
        if fname:
            ImportToplevel(self, "current", "dump_v2_0", fname)
    
    def import_all_data(self):
        # cur = controller.con.cursor()
        # cur.execute("SELECT COUNT(*) FROM tutor;")
        
        # if cur.fetchone()[0] == 0:
        #     fname = filedialog.askopenfilename(filetypes=[
        #         ('Gurutracker eXport Package', '*.gxp')])
        #     if fname:
        #         try:
        #             gurutracker.helpers.exporter.import_(fname)
        #         except gurutracker.helpers.exporter.VersionMismatchError:
        #             messagebox.showerror("Error", "This file is of an unsupported GXP version.")
        #         except:
        #             messagebox.showerror("Error", "This file is corrupted.")
        #         else:
        #             messagebox.showinfo("Finished", "Import finished. Restart app to see effect.")
        # else:
        #     messagebox.showerror("Error", "Import only possible in fresh install")
            
        # cur.close()
        if appdata.check_loadable():
            fname = filedialog.askopenfilename(filetypes=[
                    ('Gurutracker eXport Package', '*.gxp')])
            if fname:
                if appdata.should_use_converter(fname):
                    messagebox.showwarning("Old Version", "The application will now attempt import data from this file, from an old version of Gurutracker. Imports may not be complete, due to feature changes.")
                    func = appdata.get_converter_name(fname)
                    ImportToplevel(self, "load_from_old", func, fname)
        else:
            messagebox.showerror("Error", "Import of data can only be done when the install is fresh i.e. no data in the database and no files. \n\nTo make your install 'fresh', drop and create the database again, delete the data directory, notes file and the configuration files.")

