SETTINGS_FILE_NAME = "configuration.ini"
DEFAULT_SETTINGS = {
    "database": {
        "type": "sqlite3",
        "file": "~/.gurutracker/database.db"
    },
    "storage": {
        "type": "filesystem.directory",
        "directory": "~/.gurutracker/data/",
        "tempinfo": "~/.gurutracker/tempinfo"
    },
    "notes": {
        "enabled": "true",
        "autosave": "false",
        "textfile": "~/.gurutracker/notesfile.txt"
    },
    "gui.preferences": {
        "mainwindow.onStartup.launchFullScreen": "false",
        "mainwindow.ToolBar.FilesToolbarMenubutton.showSendToOption": "off",
        "mainwindow.AssignmentBrowserFrame.DoubleButton1.defaultaction": "view_current_record",
        "mainwindow.AssignmentBrowserFrame.ReturnKey.defaultaction": "open_current_record",
        "mainwindow.AssignmentBrowserFrame.ViewTagsDialog.onupdate": "refresh_treeview",
        "mainwindow.AssignmentBrowserFrame.AssignmentListFrame.displaycolumns": "assignment.id, assignment.name, .assignment.uidentifier, assignment.type, tutor.name, subject.name",
        "dialogs.AssignmentDialogBase.TutorListFrame.displaycolumns": "tutor.name, tutor.uidentifier",
        "dialogs.TutorDialogBase.SubjectListFrame.displaycolumns": "subject.name, subject.desc, subject.uidentifier"
    }
}
