from abc import ABC, abstractmethod

class StorageError(Exception):
    pass


class FileLinkageError(StorageError):
    """When a storage adapter cannot link/associate a file, this error to be
    raised.
    """
    def __init__(self, assignment, fp, e):
        self.assignment = assignment
        self.fp = fp
        self.exception = e
        super().__init__("Failed to link file {} to {}. Original exception: {}".format(
            assignment, fp, e))


class NoLinkedFileError(StorageError):
    """When a storage adapter cannot link/associate a file, this error to be
    raised.
    """
    def __init__(self, assignment):
        self.assignment = assignment
        super().__init__("Failed to get files of {} - no file was associated".format(
            assignment))


class Base(ABC):
    """This class is to be used as a base for all storage backends.

    One must implement all the methods declared here, for a fully working
    File Storage adapter.
    """

    @abstractmethod
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

    @abstractmethod
    def has_linked_file(self, assignment):
        """Check if file is linked to the assignment.

        Args:
            assignment (gurutracker.database.objects.Assignment):
                The assignment to check.
        """
        pass

    @abstractmethod
    def get_file(self, assignment):
        """Get the file which is linked to the assignment.

        Args:
            assignment (gurutracker.database.objects.Assignment):
                The assignment whose files are to be got.
                
        Returns:
            File object with an attribute .ext - extension of file

        Raises:
            gurutracker.storage.base.CannotGetFileError:
                When the file cannot be got.
        """
        pass

    @abstractmethod
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

    @abstractmethod
    def get_all(self, dirpath):
        """Put all files in a folder, and each file should be named as
        `file_{fileid:04d}`

        Args:
            dirpath (str):
                The directory to put all the files into.
        """
        pass
