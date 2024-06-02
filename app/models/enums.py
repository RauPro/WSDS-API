from enum import Enum


class GemmaMode(Enum):
    """
    Represents the different modes for Gemma.

    Attributes:
        ACCURATE (str): Indicates the accurate mode.
        STANDARD (str): Indicates the standard mode.
    """
    ACCURATE = "accurate"
    STANDARD = "standard"

class PrioritySheet(Enum):
    """
    Represents the priority levels for sheets.

    Attributes:
        ACCURATE (int): Indicates the accurate priority level with a value of 3.
        STANDARD (int): Indicates the standard priority level with a value of 4.
        CERTIFICATED (int): Indicates the certificated priority level with a value of 2.
        USER (int): Indicates the user priority level with a value of 1.
    """
    ACCURATE = 3
    STANDARD = 4
    CERTIFICATED = 2
    USER = 1
