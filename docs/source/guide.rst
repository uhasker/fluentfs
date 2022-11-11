Guide
=====

Building method chains
----------------------

In its most general form a ``FunctionalIterator`` takes an iterator and provides a **functional** and **fluent** interface on top of it::

    >>> fs.FunctionalIterator([1, 2, 3, 4])
    <fluentfs.common.functional.FunctionalIterator object at 0x7efd9fb46170>

The most important methods for building method chains are ``map``, ``filter`` and ``reduce`` (that's the **functional** part of the interface).
Both ``map`` and ``filter`` again return a ``FunctionalIterator`` (that's the **fluent** part of the interface).
These methods are available on every ``FunctionalIterator``::

    >>> fs.FunctionalIterator([1, 2, 3, 4]).map(lambda f: f ** 2).list()
    [1, 4, 9, 16]
    >>> fs.FunctionalIterator([1, 2, 3, 4]).filter(lambda f: f % 2 == 0).list()
    [2, 4]
    >>> fs.FunctionalIterator([1, 2, 3, 4]).reduce(lambda x, y: x + y, 0)
    10

Because the interface is fluent, you can build method chains on a ``FunctionalIterator``:

    >>> fs.FunctionalIterator([1, 2, 3, 4]).map(lambda f: f ** 2).filter(lambda f: f % 2 == 0).reduce(lambda x, y: x + y, 0)
    20

Note that you can only iterate once through an iterator (this is not just the case for a ``FunctionalIterator`` but for all iterators).
After that the iterator will be exhausted::

    f = fs.FunctionalIterator([1, 2, 3, 4])
    >>> f.list()
    [1, 2, 3, 4]
    >>> f.list()
    []

A minor technical point is that ``FunctionalIterator`` should not be built over any iterator, but only over a **finite** iterator.
Otherwise most methods of ``FunctionalIterator`` will never return, trying to process an infinite iterator::

    >>> from itertools import cycle
    >>> f = fs.FunctionalIterator(cycle([1, 2, 3, 4]))
    >>> f.list()
    ... this will never return ...

However you will rarely need to work with infinite iterators in the context of a filesystem.

Working with file iterators
---------------------------

The most important ``FunctionalIterator`` in fluentfs is the ``FileIterator``.
You could build one manually by creating an iterator of files and passing it to the ``FunctionalIterator`` constructor.
However this is unnecessary, because usually you will get one by accessing the ``files`` property of a ``Dir`` object.
Let's assume that we have a directory ``/home/username/somedir`` which contains the text files ``a.txt``, ``b.txt``, ``c.py`` and the binary files ``bin1`` and ``bin2``::

    >>> fs.Dir("/home/username/somedir").files
    <fluentfs.filelike.file_likes.FileIterator object at 0x7f38d7f5cb80>
    >>> fs.Dir("/home/username/somedir").files.list()
    [File("/home/username/somedir/a.txt"), File("/home/username/somedir/b.txt"), File("/home/username/somedir/bin1"), File("/home/username/somedir/bin2"), File("/home/username/somedir/c.py")]

You can use ``map``, ``filter`` and ``reduce`` on ``FunctionalIterator`` the same way you would use them on ``FileIterator``.
Note that in the context of a ``FunctionalIterator`` the ``map`` method returns a ``FunctionalIterator``, but ``filter`` returns a ``FileIterator``::

    >>> fs.Dir("/home/username/somedir").files.map(lambda f: f.name)
    <fluentfs.common.functional.FunctionalIterator object at 0x7f38d7f5cd00>
    >>> fs.Dir("/home/username/somedir").files.map(lambda f: f.name).list()
    ['a.txt', 'b.txt', 'bin1', 'bin2', 'c.py']
    >>> fs.Dir("/home/username/somedir").files.filter(lambda f: f.extension == "txt")
    <fluentfs.filelike.file_likes.FileIterator object at 0x7f38d7eeffd0>
    >>> fs.Dir("/home/username/somedir").files.filter(lambda f: f.extension == "txt").list()
    [File("/home/username/somedir/a.txt"), File("/home/username/somedir/b.txt")]
    >>> fs.Dir("/home/username/somedir").files.reduce(lambda bc, f: bc + f.bytes_count, 0)
    24

The ``FileIterator`` provides you with various shortcuts for common ``map``, ``filter`` and ``reduce`` operations.
For example to map files by their byte counts you can use the ``map_byte_count``::

    >>> fs.Dir(".").files.map_byte_count().list()
    [24, 46, 24, 32, 50]

To filter files by their extension you can use ``filter_extension``::

    >>> fs.Dir(".").files.filter_extension("txt").list()
    [File("/home/username/somedir/a.txt"), File("/home/username/somedir/b.txt")]

Have a look at the documentation of ``FileIterator`` for more information.

Including and excluding files
-----------------------------

A particularly important operation is to include or exclude (i.e. to generally filter) files based on some pattern recognition.
The simplest one is to filter files by their extension, which we already discussed.
A more complex one is to filter files by glob.
For example to get all txt files that end with `a.txt` you would use the glob `*a.txt`::

    fs.Dir(dir_path).files.filter_glob("*a.txt")

If you need to construct complex patterns, you can use regular expressions together with the ``filter_name_regex`` and ``filter_path_regex`` methods.
These take a regular expression and keep only those file whose name or path respectively matches that regular expression.
This is how you could keep all files whose name matches the regular expression `a+\.txt`::

    fs.Dir(dir_path).files.filter_name_regex(r"a+\.txt").list()
