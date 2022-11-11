# fluentfs

The `fluentfs` library provides a functional and [fluent](https://en.wikipedia.org/wiki/Fluent_interface) interface for filesystem interactions.

This library is usable and tested, but the API is currently not stable, a lot of features are still missing etc.

In summary - **try it out, but (obviously) don't use it for anything in production**.

## Requirements

You need `Python >= 3.9` for this library.

## Installation

You can install fluentfs using the `pip` package manager:

```shell
pip install fluentfs
```

## Code examples

Let's say you need to get the total number of lines of all `txt` files in the current directory (including its subdirectories).
The `fluentfs` library allows you to express this functionally as following:

1. **Filter** the files by the "txt" extension
2. **Map** the files to their line counts
3. **Reduce** the line counts to their sum

This is how it looks in code:

```python
import fluentfs as fs

total_txt_line_count = (
    fs.Dir(".")                         # get the current directory
        .files                          # get an iterator for the (regular) files in the current directory
        .filter_extension("txt")        # filter the files by the txt extension
        .text_file_iterator()           # all the files should now be text files -> obtain a text file iterator to enable text file functions
        .map_line_count()               # map every file to its line count
        .sum()                          # sum the line count
)
print(total_txt_line_count)
```

The library is very flexible, allowing you to write both short and long forms for most properties:

```python
import fluentfs as fs

# Short form (for when you quickly need to prototype something)
fs.Dir(".").files.filter_ext("txt").t().map_lc().sum()

# Long form (for when you need to use the library in a codebase)
(
    fs.Dir(".")
        .files
        .filter_extension("txt")
        .text_file_iterator()
        .map_line_count()
        .sum()
)
```

The `fluentfs` library is very general.
If you need to perform an operation that is currently not present, simply call the respective higher-order functions with your own callables.
For example here is how we could perform our task by explicitly calling the respective higher-order functions:

```python
import fluentfs as fs

(
    fs.Dir(".")
    .files
    .filter(lambda f: f.extension == "txt")
    .text_file_iterator()
    .map_self(lambda f: f.line_count)
    .reduce(lambda x, y: x + y, 0)
)
```

## Documentation

You can have a look at the [basics](https://uhasker.github.io/fluentfs/basics.html) if this is the first time you are using this library.

You can have a look at the [guide](https://uhasker.github.io/fluentfs/guide.html) if you wish to go more in-depth.

You can have a look at the [recipes](https://uhasker.github.io/fluentfs/recipes.html) if you have a specific task you want to accomplish and want to look at some fluent chains that accomplish this or a similar task.

You can also have a look at the [API documentation](https://uhasker.github.io/fluentfs/api.html). 
