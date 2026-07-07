# Start Run

# ↓

# Generate Run ID

# ↓

# Store Start Time

# ↓

# Return Run Object


import uuid
from datetime import datetime


class RunManager:

    @staticmethod
    def start():

        return {

            "run_id": str(uuid.uuid4()),

            "start": datetime.now()

        }