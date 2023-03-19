import mimetypes
import os


from gurutracker.storage.base import Base, FileLinkageError, NoLinkedFileError

class FilesystemDirectory(Base):
    def __init__(self, directory):
        """Use a filesystem directory as the base

        Args:
            directory (str): The directory path.
        """
        self.dir = directory
    
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
        try:
            f = open(os.path.join(self.dir, "file_{:04d}".format(
                assignment.id)), "wb")
            f.write(fp.read())
            f.close()
        except Exception as e:
            raise FileLinkageError(assignment, fp, e)
        
        if not hasattr(fp, "ext"):
            if hasattr(fp, "name"):
                fp.ext = fp.name.split(".")[-1]
            else:
                fp.ext = "bin"
        with open(os.path.join(self.dir, "extn_{:04d}".format(
                assignment.id)), "w") as f:
            f.write(fp.ext)
            f.close()

    def has_linked_file(self, assignment):
        """Check if file is linked to the assignment.

        Args:
            assignment (gurutracker.database.objects.Assignment):
                The assignment to check.
        """
        return os.path.isfile(os.path.join(self.dir, "file_{:04d}".format(
                assignment.id)))

    def get_file(self, assignment):
        """Get the file which is linked to the assignment.

        Args:
            assignment (gurutracker.database.objects.Assignment):
                The assignment whose files are to be got.

        Raises:
            gurutracker.storage.base.CannotGetFileError:
                When the file cannot be got.
        """
        if self.has_linked_file(assignment):
            f = open(os.path.join(self.dir, "file_{:04d}".format(
                assignment.id)), "rb")
            with open(os.path.join(self.dir, "extn_{:04d}".format(
                assignment.id)), "r") as fp:
                f.ext = fp.read()
            return f
        else:
            raise NoLinkedFileError(assignment)

    def unlink_file(self, assignment):
        """Unlink all files related to assignment.

        Args:
            assignment (gurutracker.database.objects.Assignment):
                The assignment whose files are to be unlinked.

        Raises:
            gurutracker.storage.base.CannotUnlinkFileError:
                When the file cannot be created.
        """
        if self.has_linked_file(assignment):
            try:
                os.unlink(os.path.join(self.dir, "file_{:04d}".format(
                assignment.id)))
                os.unlink(os.path.join(self.dir, "extn_{:04d}".format(
                assignment.id)))
            except Exception as e:
                raise FileLinkageError(assignment, None, e)
        else:
            raise NoLinkedFileError(assignment)

    def get_all(self, dirpath):
        """Put all files in a folder, and each file should be named as
        `file_{fileid:04d}`

        Args:
            dirpath (str):
                The directory to put all the files into.
        """
        raise NotImplementedError
