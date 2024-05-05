from enum import Enum


class GemmaMode(Enum):
    ACCURATE = "accurate"
    STANDARD = "standard"

class PrioritySheet(Enum):
    ACCURATE = 3
    STANDARD = 4
    CERTIFICATED = 2
    USER = 1
