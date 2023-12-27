import re


def hard_remove_non_alphanum(s: str):
    """
    Remove non-alphanumeric characters from a string including whitespace and comma
    :param s: input string
    :return: string only containing alphanumeric characters
    """
    return re.sub('[^a-zA-Z0-9]+', '', s)


def soft_remove_non_alphanum(s: str):
    """
    Remove non-alphanumeric characters from a string but preserve spaces and commas
    :param s: input string
    :return: string only containing alphanumeric characters
    """
    return re.sub('[^\w\s,]', '', s)
