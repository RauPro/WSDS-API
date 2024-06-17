from bson import ObjectId


def serialize_new(new: dict) -> dict:
    """
    Convert MongoDB document to a dictionary with stringified ObjectId.

    Args:
        new (dict): The MongoDB document to be serialized.

    Returns:
        dict: The serialized dictionary with ObjectId values converted to strings.

    Description:
        This function takes a MongoDB document represented as a dictionary and
        converts any ObjectId values to their string representation. It recursively
        iterates over the dictionary items and checks if the value is an instance
        of ObjectId. If so, it replaces the value with its string representation.

    Example:
        >>> document = {"_id": ObjectId("60a1c2d3e4f5c6b7c8d9e0f1"), "name": "John"}
        >>> serialized_document = serialize_new(document)
        >>> serialized_document
        {"_id": "60a1c2d3e4f5c6b7c8d9e0f1", "name": "John"}
    """
    if isinstance(new, dict):
        for key, value in new.items():
            if isinstance(value, ObjectId):
                new[key] = str(value)
    return new


def is_search_in_text(phrase: str, text: str) -> bool:
    """
    Check if a phrase is present in the given text using individual words.

    Args:
        phrase (str): The phrase to search for in the text.
        text (str): The text to search within.

    Returns:
        bool: True if all the words in the phrase are found in the text, False otherwise.

    Description:
        This function takes a phrase and a text as input and checks if all the individual
        words of the phrase are present in the text. It splits the phrase into words and
        iterates over each word, checking if it is present in the text (case-insensitive).
        If any word is not found in the text, the function returns False. Otherwise, it
        returns True.

    Example:
        >>> phrase = "quick brown fox"
        >>> text = "The quick brown fox jumps over the lazy dog"
        >>> is_search_in_text(phrase, text)
        True
        >>> phrase = "quick brown cat"
        >>> is_search_in_text(phrase, text)
        False
    """
    phrase = phrase.split()
    is_on_text = True
    for word in phrase:
        if word.lower() not in text.lower():
            is_on_text = False
    return is_on_text
