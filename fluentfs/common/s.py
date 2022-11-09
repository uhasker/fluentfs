def chomp(s: str) -> str:
    """
    Removes a trailing newline from a string, if present.

    Note that both "\\\\n" and "\\\\r\\\\n" are counted as a trailing newline.

    :param s: The string.
    :return: The string without a trailing newline.
    """
    if s.endswith("\r\n"):
        return s[:-2]
    elif s.endswith("\n"):
        return s[:-1]
    return s


def is_empty(s: str) -> bool:
    """
    Checks if this string is empty, i.e. has length 0 or has only whitespace characters.

    Note that the behaviour of this function is different from the built-in isspace(),
    since isspace() returns False for strings of length 0, which is undesirable in
    many situations.

    :param s: The string.
    :return: Whether the string is empty.
    """
    return len(s) == 0 or s.isspace()
