from datetime import datetime
from uuid import uuid4


def ObjectId():
    """
    Generates a unique identifier based on the current timestamp and a random UUID.

    Returns:
        str: A unique identifier string in the format 'YYYYMMDD-HHMMSS-<uuid>'.

    Example:
        >>> ObjectId()
        '20230602-082034-d41d8cd9-8f00-4b5d-8311-2d8a7b7f4e1d'
    """
    return datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
