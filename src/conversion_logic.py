import re

def csv_string_to_list(input: str) -> list[str]:
    """Convert string to list.

    Args:
        input (str): Expected csv string.

    Returns:
        list: List of strings.
    """

    if input:
        return re.split(r',\s*', input.strip())

    return []