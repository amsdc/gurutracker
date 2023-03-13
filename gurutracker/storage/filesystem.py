from gurutracker.storage.base import Base

class Filesystem(Base):
    def __init__(self):
        pass
    
    def link_file(self, fp, assignment):
        """Associate a file (binary file object) with an assignment.

        Args:
            fp: A binary file-like object with the .read() method.
            assignment (gurutracker.database.objects.Assignment):
                The assignment to associate `fp` with.

        Raises:
            gurutracker.storage.base.CannotLinkFileError:
                When the file cannot be created.
        """
        pass

    def has_linked_file(self, assignment):
        """Check if file is linked to the assignment.

        Args:
            assignment (gurutracker.database.objects.Assignment):
                The assignment to check.
        """
        pass

    def get_file(self, assignment):
        """Get the file which is linked to the assignment.

        Args:
            assignment (gurutracker.database.objects.Assignment):
                The assignment whose files are to be got.

        Raises:
            gurutracker.storage.base.CannotGetFileError:
                When the file cannot be got.
        """
        pass

    def unlink_file(self, assignment):
        """Unlink all files related to assignment.

        Args:
            assignment (gurutracker.database.objects.Assignment):
                The assignment whose files are to be unlinked.

        Raises:
            gurutracker.storage.base.CannotUnlinkFileError:
                When the file cannot be created.
        """
        pass

    def get_all(self, dirpath):
        """Put all files in a folder, and each file should be named as
        `file_{fileid:04d}`

        Args:
            dirpath (str):
                The directory to put all the files into.
        """
        pass
