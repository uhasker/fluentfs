Basics
======

The **fluentfs** library provides a functional and fluent interface for filesystem interactions.

If you want to follow along, you will need to import fluentfs first::

    import fluentfs as fs

File-like objects
-----------------

There are currently four classes for representing "file-like objects" - ``FileLike``, ``Dir``, ``File`` and ``TextFile``.

Files and directories
~~~~~~~~~~~~~~~~~~~~~

A ``Dir`` represents a directory::

    >>> fs.Dir("/home/username/somedir")
    Dir("/home/username/somedir")

A ``File`` represents a regular file (either a binary or a text file)::

    >>> fs.File("/home/username/somedir/myfile.txt")
    File("/home/username/somedir/myfile.txt")

Both ``Dir`` and ``File`` are ``FileLike`` objects (i.e. ``Dir`` and ``File`` inherit from ``FileLike``)::

    >>> issubclass(fs.Dir, fs.FileLike)
    True
    >>> issubclass(fs.File, fs.FileLike)
    True

The FileLike class
~~~~~~~~~~~~~~~~~~

Generally speaking, a ``FileLike`` object is anything that is "like a file", i.e. has the ``path`` and ``name`` properties.
The ``path`` property is the *maximally expanded* path of the respective ``FileLike`` object.
This means that ``path`` is absolute and all environment variables, special characters (like `~`) are expanded.
The ``name`` property is the base name of the ``FileLike`` object, i.e. the file name or the directory base name.

For example, let's say that `~` points to `/home/username` and you have an environment variable `DIRNAME` with the value `somedir`.
Then you can do the following::

    >>> dir = fs.Dir("~/$DIRNAME")
    Dir("/home/username/somedir")
    >>> dir.path
    '/home/username/somedir'
    >>> dir.name
    'somedir'

Both ``Dir`` and ``File`` implement additional methods and properties which are useful when dealing with files or directories.
For example::

    >>> file = dir.File("myfile.txt")
    File("/home/username/somedir/myfile.txt")
    >>> file.extension
    'txt'
    >>> file.mod_time
    datetime.datetime(2022, 10, 26, 16, 37, 37, 533307)

You can have a look at the guide or at the documentation of ``Dir`` and ``File`` for more.

Text files
~~~~~~~~~~

Text files are represented by ``TextFile`` (which inherits from ``File``).
You can create a ``TextFile`` from a ``File`` object using the ``text_file`` function::

    >>> text_file = file.text_file()
    TextFile("/home/username/somedir/myfile.txt")

By default the encoding is assumed to be UTF-8, but you can pass an ``encoding`` argument to ``text_file`` to change that.
Note that the ``text_file`` function doesn't attempt to check if the underlying file is actually a text file in the given encoding (since that would require trying to decode the entire file, which could get very expensive).
Therefore a call to ``text_file`` will always succeed, but if the underlying file isn't actually a text file, you will get errors when calling functions that require decoding the content of the file.

For a simple example, let us say that this is the content of the UTF-8 encoded file ``myfile.txt`` on a system where line endings are represented by ``\n``:

    | Roses are red.
    | Violets are blue.
    | fluentfs is a great library,
    | and I am too lazy to rhyme something at you.

Then this would be the output of some of the text file functions and properties::

    >>> text_file.content
    'Roses are red.\nViolets are blue.\nfluentfs is a great library,\nand I am too lazy to rhyme something at you.\n'
    >>> text_file.encoding
    'utf-8'
    >>> text_file.char_count
    104
    >>> text_file.line_count
    4
    >>> text_file.word_count
    21
    >>> text_file.max_line_len
    44

You can have a look at the documentation of ``TextFile`` for more.

Functional iterators
--------------------

The FunctionalIterator class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The functions and properties we had a look at so far returned a single object.
For example the ``word_count`` property returned the number of words in a file.
Let's try to get the actual words of a text file::

    >>> text_file.words
    <fluentfs.common.functional.FunctionalIterator object at 0x7f415b228d30>

If a function in ``fluentfs`` returns multiple objects, it usually doesn't return a ``list`` or ``tuple`` or ``set`` - instead it returns an instance of ``FunctionalIterator``.
You can convert such an object to a list using the ``list`` function::

    >>> text_file.words.list()
    ['Roses', 'are', 'red.', 'Violets', 'are', 'blue.', 'fluentfs', 'is', 'a', 'great', 'library,', 'and', 'I', 'am', 'to', 'lazy', 'to', 'rhyme', 'something', 'at', 'you.']

The FileIterator class
~~~~~~~~~~~~~~~~~~~~~~

The most important instances of ``FunctionalIterator`` are iterators of file-like objects.
A ``FileIterator`` object represents an iterator which iterates over files and implements various useful methods for working with files.

The most common way to get a ``FileIterator`` is via the ``files`` property of a ``Dir`` object.
Do note that ``files`` will contain the files of the given directory along with all its **subdirectories**.
Let's assume that the ``/home/username/somedir`` has the text files ``a.txt``, ``b.txt``, ``c.py`` and the binary files ``bin1`` and ``bin2``::

    files = fs.Dir("/home/username/somedir").files
    >>> <fluentfs.filelike.file_likes.FileIterator object at 0x7f888098cbb0>
    files.list()
    >>> [File("/home/username/somedir/a.txt"), File("/home/username/somedir/b.txt"), File("/home/username/somedir/bin1"), File("/home/username/somedir/bin2"), File("/home/username/somedir/c.py")]

You can then call various useful methods on the ``FileIterator`` object::

    >>> files.len()
    5

There are two important things to realize about ``FunctionalIterator``.
First, it has a lot of higher-order functions available which makes it very flexible and powerful - thus the **functional** part of fluentfs.
Seconds, a lot of methods implemented by it return instances of ``FunctionalIterator`` (or its subclasses like ``FileIterator``) which enables you to build function chains - thus the **fluent** part of fluentfs.
Combined together, this means that you can build filter-map-reduce chains of functions::

    >>> fs.Dir("/home/username/somedir").files.filter(lambda f: f.extension == "txt")
    <fluentfs.filelike.file_likes.FileIterator object at 0x7f415b076a10>
    >>> fs.Dir("/home/username/somedir").files.filter(lambda f: f.extension == "txt").map(lambda f: f.byte_count)
    <fluentfs.common.functional.FunctionalIterator object at 0x7f415b074ac0>
    >>> fs.Dir("/home/username/somedir").files.filter(lambda f: f.extension == "txt").map(lambda f: f.byte_count).reduce(lambda x, y: x + y, 0)
    70

Instead of writing your own functions to pass to filter, map and reduce you can also often use functions already provided for you by fluentfs to accomplish the same task::

    >>> fs.Dir("/home/username/somedir").files.filter_extension("txt").map_byte_count().sum()
    70

The TextFileIterator class
~~~~~~~~~~~~~~~~~~~~~~~~~~

A ``TextFileIterator`` object represents an iterator which iterates over text files and implements various useful methods for working with text files.
For example it has the ``map_line_count`` method, which a regular ``FileIterator`` does not have (since binary files usually do not have the concept of lines).

You can get a ``TextFileIterator`` from a ``FileIterator`` by calling ``text_file_iterator`` on it::

    text_file_it = some_iterator_with_text_files.text_file_iterator()

Just like with ``text_file()`` this will always succeed, but subsequent method calls may fail if the underlying files are not actually text files.
This means that you are responsible to remove all binary files from the iterator before calling ``text_file_iterator`` (see below for how to do that).
You can use the filter function to ensure that you file iterator contains text files only.
For example if you know that all files with the ``txt`` extension are text files (which they hopefully are), you can do the following::

    >>> fs.Dir(".").files.filter_extension("txt").text_file_iterator()
    <fluentfs.filelike.text_file.TextFileIterator object at 0x7f888069ab30>

As soon as you have a ``TextFileIterator``, you can call the respective methods.
This is how you would get the total number of lines in all your ``txt`` files::

    >>> fs.Dir(".").files.filter_extension("txt").text_file_iterator().map_line_count().sum()
    6

Further reading
---------------

All of this allows you to accomplish common tasks in a single line of clear and readable code.
That's the power of a functional and fluent interface for the filesystem!

To go beyond the basics, check out the guide.

To view some recipes for common tasks, check out the recipes.

You can also have a look at the API documentation.
