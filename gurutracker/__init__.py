__version__ = "0.3.0"
__db_revision__ = "4"
__gxp_version__ = "2.0.0"

def main():
    import tkinter as tk
    from gurutracker.views.mainwindow import MainWindow
    import gurutracker.helpers.excdialog
    tk.Tk.report_callback_exception = gurutracker.helpers.excdialog.show_error
    
    win = MainWindow()
    # theming
    # style = ttk.Style()
    # win.tk.call("source", "themes/azure/light.tcl")
    # style.theme_use("azure-light")
    # theming end
    
    win.mainloop()
    
