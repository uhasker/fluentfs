Recipes
=======

You will need to import fluentfs first::

    import fluentfs as fs

Example recipes
---------------

Number of files and directories in a directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get the number of "file-like" objects (i.e. files & directories) in a directory (including subdirectories)::

    fs.Dir(dir).file_likes.len()

Get the number of files in a directory (including subdirectories)::

    fs.Dir(dir).files.len()

Get the number of directories in a directory (including subdirectories)::

    fs.Dir(dir).dirs.len()

Biggest files in a directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get a table with the n biggest files in a directory (including subdirectories)::

    (
        # e.g. dir_path = ".", n = 20
        fs.Dir(dir_path)                        # 1.
            .files                              # 2.
            .top_n(n)                           # 3.
            .table(                             # 4.
                ["File path", "Size"],
                lambda f: (f.relative_path, f.size)
            )
    )

1. We get a ``Dir`` object whose path is ``dir_path``.
2. We get a ``FileIterator`` for the files of the directory at ``dir_path``.
3. The ``FileIterator`` is a ``FunctionalIterator``, so it has the ``top_n`` method to get the ``n`` biggest items in the iterator.
   Since files are compared by size in ``fluentfs``, we can use it to get the ``n`` biggest files.
   The ``top_n`` function returns another ``FunctionalIterator``.
4. We can obtain a ``Table`` from any ``FunctionalIterator`` by calling the ``table`` method.
   This method takes a list of column names and a function which maps every element of the ``FunctionalIterator`` to a row.
   Therefore we get a table where the column "File path" will be populated with the relative paths of the files (``f.relpath``) and the column "Size" will be populated with the file sizes (``f.size``).

Counting lines and empty lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get a sorted table with all Python files in a directory together with their total lines, source lines and blank lines.::

    (
        # e.g. dir_path = "."
        fs.Dir(dir_path)                            # 1.
            .files                                  # 2.
            .filter_extension("py")                 # 3.
            .text_file_iterator()                   # 4.
            .sort_desc(lambda f: f.line_count)      # 5.
            .table(                                 # 6.
                ["File", "Total lines", "Source lines", "Blank lines"],
                lambda f: (f.relative_path, f.line_count, f.non_empty_line_count, f.empty_line_count)
            )
    )

1. We get a ``Dir`` object whose path is ``dir_path``.
2. We get a ``FileIterator`` for the files of the directory at ``dir_path``.
3. We filter the ``FileIterator`` by the "py" extension, which returns another ``FileIterator``.
4. Since we are about to perform text file operations, we need to obtain a ``TextFileIterator`` from the ``FileIterator`` using the ``text_file_iterator`` function.
   Since we filtered by the "py" extension beforehand, we can be relatively sure that we only have text files.
   Of course theoretically nothing would prevent us from having a binary file with the "py" extension in our directory.
   In that case ``text_file_iterator`` would still succeed, but any further operation would fail when we try to decode those binary files.
5. We use the ``sort_desc`` function together with a lambda that specifies the sort key (similar to how regular Python ``sort`` works) to sort the files by their total line counts.
6. We can obtain a ``Table`` from any ``FunctionalIterator`` by calling the ``table`` method.
   This method takes a list of column names and a function which maps every element of the ``FunctionalIterator`` to a row.
   Therefore we get a table where the columns will be populated with the relative file path and the number of lines, non-blank lines and blank lines.
