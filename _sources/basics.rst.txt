Basics
======

fluentfs provides a functional interface for filesystem interactions.

If you want to follow along, you will need to import fluentfs first::

    import fluentfs as fs

Basic concepts
--------------

There are currently four classes for representing "file-like objects" - ``FileLike``, ``Dir``, ``File`` and ``TextFile``.

A ``Dir`` represents a directory::

    >>> fs.Dir("/home/username/somedir")
    Dir("/home/username/somedir")

Note that if we are in the "/home/username/somedir" directory already, we can pass a relative path to ``fs.Dir``::

    >>> fs.Dir(".")
    Dir("/home/username/somedir")

A ``File`` represents a regular file (either a binary or a text file)::

    >>> fs.File("/home/username/somedir/myfile.txt")
    File("/home/username/somedir/myfile.txt")

Just like with ``fs.Dir`` we can pass relative paths to ``fs.File``::

    >>> fs.File("myfile.txt")
    File("/home/username/somedir/myfile.txt")

Both ``Dir`` and ``File`` are ``FileLike`` objects (i.e. ``Dir`` and ``File`` inherit from ``FileLike``)::

    >>> issubclass(fs.Dir, fs.FileLike)
    True
    >>> issubclass(fs.File, fs.FileLike)
    True

Generally speaking, a ``FileLike`` object is anything that is "like a file", i.e. has the ``path`` and the ``name`` properties.
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

You can have a look at the documentation of ``Dir`` and ``File`` for more.

Text files are represented by ``TextFile`` (which inherits from ``File``).
You can create a ``TextFile`` from a ``File`` object using the ``text_file`` function::

    >>> text_file = file.text_file()
    TextFile("/home/username/somedir/myfile.txt")

By default the encoding is assumed to be UTF-8, but you can pass an ``encoding`` argument to ``text_file`` to change that.
Note that the ``text_file`` function doesn't attempt to check if the underlying file is actually a text file in the given encoding (since that would require trying to decode the entire file, which could get very expensive).
Therefore a call to ``text_file`` will always succeed, but if the underlying file isn't actually a text file, you will get errors when calling functions that require decoding the content of the file.

Now let us say that this is the content of myfile.txt:

    | Roses are red.
    | Violets are blue.
    | fluentfs is a great library,
    | and I am to lazy to rhyme something at you.

Then this would be the output of some of the text file functions and properties::

    >>> text_file.content
    'Roses are red.\nViolets are blue.\nfluentfs is a great library,\nand I am to lazy to rhyme something at you.\n'
    >>> text_file.encoding
    'utf-8'
    >>> text_file.char_count
    103
    >>> text_file.line_count
    4
    >>> text_file.word_count
    21
    >>> text_file.max_line_len
    43

You can have a look at the documentation of ``TextFile`` for more.

Functional iterators
--------------------

The functions and properties we had a look at so far returned a single object.
For example the ``word_count`` property returned the number of words in a file.
Let's try to get the actual words of a text file::

    >>> text_file.words
    <fluentfs.common.functional.FunctionalIterator object at 0x7f415b228d30>

If a function in ``fluentfs`` returns multiple objects, it doesn't return a ``list`` or ``tuple`` or ``set`` - instead it returns an instance of ``FunctionalIterator``.
You can convert this to a list using the ``list`` function:

    >>> text_file.words.list()
    ['Roses', 'are', 'red.', 'Violets', 'are', 'blue.', 'fluentfs', 'is', 'a', 'great', 'library,', 'and', 'I', 'am', 'to', 'lazy', 'to', 'rhyme', 'something', 'at', 'you.']

The most important instances of ``FunctionalIterator`` are iterators of file-like objects.
``FileIterator`` and ``TextFileIterator`` are iterators which iterate over files and text files respectively and implement various useful functions.

The most common way to get a ``FileIterator`` is via the ``files`` property of a ``Dir`` object::

    files = fs.Dir("/home/username/somedir").files

You can then call various useful functions on the ``FileIterator`` object::

    files.len()

You can get a ``TextFileIterator`` from a ``FileIterator`` by calling ``text_file_iterator`` on it::

    text_files = fs.Dir("/home/username/somedir").text_file_iterator()

Just like with ``text_file()`` this will always succeed, but subsequent method calls may fail if the underlying files are not actually text files.

The most important part about ``FunctionalIterator`` is that a lot of functions implemented by it return instances of ``FunctionalIterator`` themselves.
This means you can build filter-map-reduce chains of functions::

    >>> fs.Dir("/home/username/somedir").files.filter(lambda f: f.extension == "txt")
    <fluentfs.filelike.file_likes.FileIterator object at 0x7f415b076a10>
    >>> fs.Dir("/home/username/somedir").files.filter(lambda f: f.extension == "txt").map(lambda f: f.bytes_count)
    <fluentfs.common.functional.FunctionalIterator object at 0x7f415b074ac0>
    >>> fs.Dir(".").files.filter(lambda f: f.extension == "txt").map(lambda f: f.bytes_count).reduce(lambda x, y: x + y, 0)
    198938

You can always call ``list()`` on a ``FunctionalIterator`` to obtain a list from the respective iterator.

Instead of writing your own functions to pass to filter, map and reduce you can also often use built-in functions to accomplish the same task::

    >>> fs.Dir(".").files.filter_extension("txt").map_bytes_count().sum()
    198938

This allows you to accomplish common tasks in a single line of clear and readable code.
That's the power of writing higher-order functions for the filesystem!

To view some recipes for common tasks, check out the "Recipes" section.
You can also have a look at the documentation of ``FileIterator`` and ``TextFileIterator`` object for more information.
