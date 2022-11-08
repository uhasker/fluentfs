Recipes
=======

You will need to import fluentfs first::

    import fluentfs as fs

Example recipes
---------------

Note that ``fs.Dir`` is recursive, i.e. it descends into all subdirectories.

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
        fs.Dir(dir_path)                                                  # 1.
            .files                                                        # 2.
            .top_n(n)                                                     # 3.
            .table(["File path", "Size"], lambda f: (f.relpath, f.size))  # 4.
    )

1. We get a ``Dir`` object whose path is ``dir_path``.
2. We get a ``FileIterator`` for the files of the directory at ``dir_path``.
3. The ``FileIterator`` is a ``FunctionalIterator``, so it has the ``top_n`` method to get the ``n`` biggest items in the iterator.
   Since files are compared by size in ``fluentfs``, we can use it to get the ``n`` biggest files.
4. The ``top_n`` function returns another ``FunctionalIterator``.
   We can obtain a ``Table`` from any ``FunctionalIterator`` by calling the ``table`` method.
   This method takes a list of column names and a function which maps every element of the ``FunctionalIterator`` to a row.
   Therefore we get a table where the column "File path" will be populated with the relative paths of the files (``f.relpath``) and the column "Size" will be populated with the file sizes (``f.size``).