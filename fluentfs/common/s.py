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
