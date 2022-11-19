from fluentfs.common.functional import FunctionalIterator
from fluentfs.common.s import chomp, is_empty
from fluentfs.exceptions.exceptions import FluentFsException
from fluentfs.filelike.file_iterator import File


class TextFile(File):
    def __init__(
        self, path: str, encoding: str = "utf-8", raise_on_decode_error: bool = True
    ) -> None:
        """
        Initialize a new TextFile from a path.

        :param path: The path.
        :param raise_on_decode_error: Whether to raise an exception in case of a decoding
            error. If this is False and the file cannot be read in the given encoding,
            the content of this file will be returned as an empty string. This is useful
            if you are iterating over a directory where some files are in a different
            encoding, and you want to simply ignore these files.
        :param encoding: The encoding. This is assumed to be UTF-8 by default.
        """
        super().__init__(path)

        self.encoding = encoding
        self.raise_on_decode_error = raise_on_decode_error

    @property
    def content(self) -> str:
        """
        The content of this file.

        :return: The content.
        """
        with open(str(self.path), "r", encoding=self.encoding) as file:
            try:
                return file.read()
            except UnicodeDecodeError as e:
                if self.raise_on_decode_error:
                    raise FluentFsException(
                        f"Cannot decode file at {self.path} using {self.encoding} encoding. "
                        f"The following exception occurred: {str(e)}"
                    )
                else:
                    return ""

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
            try:
                return FunctionalIterator([chomp(line) for line in file.readlines()])
            except UnicodeDecodeError as e:
                if self.raise_on_decode_error:
                    raise FluentFsException(
                        f"Cannot decode file at {self.path} using {self.encoding} encoding. "
                        f"The following exception occurred: {str(e)}"
                    )
                else:
                    return FunctionalIterator([])

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


# Add attributes to File & FileIterator
