SETTINGS_FILE_NAME = "configuration.ini"
DEFAULT_SETTINGS = {
    "database": {
        "type": "mysql",
        "host": "localhost",
        "user": "root",
        "password": "groot12345",
        "database": "gurutracker",
        "port": 3306
    },
    "notes": {
        "enabled": "true",
        "autosave": "false",
        "textfile": "notes.txt"
    },
    "files": {
        "datadir": "DATA",
        "extension": "pdf"
    },
    "gui.preferences": {
        "mainwindow.onStartup.launchFullScreen": "false",
        "mainwindow.AssignmentBrowserFrame.DoubleButton1.defaultaction": "view_current_record",
        "mainwindow.AssignmentBrowserFrame.ReturnKey.defaultaction": "open_current_record",
        "mainwindow.AssignmentBrowserFrame.ViewTagsDialog.onupdate": "refresh_treeview",
        "mainwindow.AssignmentBrowserFrame.AssignmentListFrame.displaycolumns": "assignment.id, assignment.name, .assignment.uidentifier, assignment.type, tutor.name, subject.name",
        "dialogs.AssignmentDialogBase.TutorListFrame.displaycolumns": "tutor.name, tutor.uidentifier",
        "dialogs.TutorDialogBase.SubjectListFrame.displaycolumns": "subject.name, subject.desc, subject.uidentifier"
    }
}
