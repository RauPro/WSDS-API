from bson import ObjectId


def serialize_new(new):
    """Convert MongoDB document to a dictionary with stringified ObjectId."""
    if isinstance(new, dict):
        for key, value in new.items():
            if isinstance(value, ObjectId):
                new[key] = str(value)
    return new


def is_search_in_text(phrase: str, text: str):
    """Check if phrase in text using the words"""
    phrase = phrase.split()
    is_on_text = True
    for word in phrase:
        if word.lower() not in text.lower():
            is_on_text = False
    return is_on_text
