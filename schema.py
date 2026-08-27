from pydantic import BaseModel

class Event(BaseModel):
    name            : str
    description     : str
    location        : str
    date            : str
    capacity        : int

class Registration(BaseModel):
    event_id        : int
    name            : str
    email           : str
