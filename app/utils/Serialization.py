from bson import ObjectId


def serialize_new(new):
    """Convert MongoDB document to a dictionary with stringified ObjectId."""
    if isinstance(new, dict):
        for key, value in new.items():
            if isinstance(value, ObjectId):
                new[key] = str(value)
    return new