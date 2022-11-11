from fluentfs.common.functional import FunctionalIterator
from fluentfs.common.s import chomp, is_empty
from fluentfs.filelike.file_likes import File, FileIterator


class TextFile(File):
    def __init__(self, path: str, encoding: str = "utf-8"):
        """
        Initialize a new TextFile from a path.

        :param path: The path.
        :param encoding: The encoding. This is assumed to be UTF-8 by default.
        """
        super().__init__(path)

        self.encoding = encoding

    @property
    def content(self) -> str:
        """
        The content of this file.

        :return: The content.
        """
        with open(str(self.path), "r", encoding=self.encoding) as file:
            return file.read()

    @property
    def char_count(self) -> int:
        """
        The number of characters of this file.

        This is similar to `wc -m $FILENAME`.

        :return: The number of characters.
        """
        return len(self.content)

    cc = char_count

    @property
    def words(self) -> FunctionalIterator[str]:
        """
        The words of this file.

        It is assumed that words are separated by whitespace.

        :return: A functional iterator containing the words of this file.
        """
        return FunctionalIterator(self.content.split())

    @property
    def word_count(self) -> int:
        """
        The number of words of this file.

        This is similar to `wc -w $FILENAME`.

        :return: The number of words.
        """
        return self.words.len()

    wc = word_count

    @property
    def lines(self) -> FunctionalIterator[str]:
        """
        The lines of this file.

        :return: A functional iterator containing the lines of this file.
        """
        with open(str(self.path), "r", encoding=self.encoding) as file:
            return FunctionalIterator([chomp(line) for line in file.readlines()])

    @property
    def line_count(self) -> int:
        """
        The number of lines of this file.

        This is similar to `wc -l $FILENAME`.

        :return: The number of lines.
        """
        return self.lines.len()

    lc = line_count

    @property
    def line_lens(self) -> FunctionalIterator[int]:
        """
        The lengths of the lines of this file.

        :return: A functional iterator containing the line lengths of this file.
        """
        return self.lines.map(lambda line: len(line))

    @property
    def max_line_len(self) -> int:
        """
        The maximum line length of this file.

        This is similar to `wc -L $FILENAME`.

        :return: The maximum line length.
        """
        return self.line_lens.max()

    @property
    def empty_lines(self) -> FunctionalIterator[str]:
        return self.lines.filter(lambda line: is_empty(line))

    @property
    def empty_line_count(self) -> int:
        return self.empty_lines.len()

    @property
    def non_empty_lines(self) -> FunctionalIterator[str]:
        return self.lines.filter(lambda line: not is_empty(line))

    @property
    def non_empty_line_count(self) -> int:
        return self.non_empty_lines.len()

    def __repr__(self) -> str:
        return f"TextFile({self.path})"


class TextFileIterator(FileIterator[TextFile]):
    def map_char_count(self) -> FunctionalIterator[int]:
        """
        Map the files to their character counts.

        Note that it is implicitly assumed that all the files are valid text files.
        This function is equivalent to map(lambda file: file.text_file().char_count).

        :return: A functional iterator containing the character counts.
        """
        return self.map(lambda file: file.char_count)

    map_cc = map_char_count

    def map_word_count(self) -> FunctionalIterator[int]:
        """
        Map the files to their word counts.

        Note that it is implicitly assumed that all the files are valid text files.
        This function is equivalent to map(lambda file: file.text_file().word_count).

        :return: A functional iterator containing the word counts.
        """
        return self.map(lambda file: file.word_count)

    map_wc = map_word_count

    def map_line_count(self) -> FunctionalIterator[int]:
        """
        Map the files to their line counts.

        Note that it is implicitly assumed that all the files are valid text files.
        This function is equivalent to map(lambda file: file.text_file().line_count).

        :return: A functional iterator containing the line counts.
        """
        return self.map(lambda file: file.line_count)

    map_lc = map_line_count

    def map_empty_line_count(self) -> FunctionalIterator[int]:
        return self.map(lambda file: file.empty_line_count)

    def map_non_empty_line_count(self) -> FunctionalIterator[int]:
        return self.map(lambda file: file.non_empty_line_count)


# Add attributes to File & FileIterator


def text_file(self: File, encoding: str = "utf-8") -> "TextFile":
    """
    Get a TextFile object for this file.

    Note that you are responsible to ensure that the underlying file is a valid
    text file (since this is very expensive to ensure automatically). This function
    will always succeed, even if the underlying file is not a valid text file.
    However, when calling paths on the resulting TextFile object, errors will occur.

    :param encoding: The encoding to use.
    :return: The obtained TextFile object.
    """
    return TextFile(self.path, encoding)


setattr(File, "text_file", text_file)
setattr(File, "t", text_file)


def text_file_iterator(self: FileIterator) -> "TextFileIterator":
    return TextFileIterator(self.map_self(lambda file: file.text_file()))


setattr(FileIterator, "text_file_iterator", text_file_iterator)
setattr(FileIterator, "t", text_file_iterator)
