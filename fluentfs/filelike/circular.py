import os

from fluentfs.filelike.dir import Dir
from fluentfs.filelike.file import File
from fluentfs.filelike.file_iterator import FileIterator
from fluentfs.filelike.text_file import TextFile
from fluentfs.filelike.text_file_iterator import TextFileIterator


def dir(self: File) -> "Dir":
    """
    The directory containing this file.

    :return: A Dir object representing the directory.
    """
    return Dir(os.path.dirname(self.path))


setattr(File, "dir", property(dir))


def text_file(
    self: File, encoding: str = "utf-8", raise_on_decode_error: bool = True
) -> "TextFile":
    """
    Get a TextFile object for this file.

    Note that you are responsible to ensure that the underlying file is a valid
    text file (since this is very expensive to ensure automatically). This function
    will always succeed, even if the underlying file is not a valid text file.
    However, when calling paths on the resulting TextFile object, errors will occur.

    :param encoding: The encoding to use.
    :return: The obtained TextFile object.
    """
    return TextFile(self.path, encoding, raise_on_decode_error)


setattr(File, "text_file", text_file)
setattr(File, "t", text_file)


def text_file_iterator(
    self: FileIterator, encoding: str = "utf-8", raise_on_decode_error: bool = True
) -> "TextFileIterator":
    return TextFileIterator(
        self.map_self(lambda file: file.text_file(encoding, raise_on_decode_error))
    )


setattr(FileIterator, "text_file_iterator", text_file_iterator)
setattr(FileIterator, "t", text_file_iterator)
