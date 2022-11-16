from fluentfs.common.functional import FunctionalIterator
from fluentfs.filelike.file_iterator import FileIterator
from fluentfs.filelike.text_file import TextFile


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
