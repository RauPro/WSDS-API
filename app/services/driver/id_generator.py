from datetime import datetime
from uuid import uuid4

def ObjectId():
    return datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())