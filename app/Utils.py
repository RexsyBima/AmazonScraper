def remove_duplicates(input_list):
    """
    Remove duplicates from a list while preserving the original order.

    Args:
    - input_list (list): The input list with potential duplicate values.

    Returns:
    - list: A new list with duplicates removed.
    """
    seen = set()
    result = []

    for item in input_list:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result
