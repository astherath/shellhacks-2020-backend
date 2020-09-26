import bcrypt
import geopy
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum, auto
from typing import Optional, List
from starlette.exceptions import HTTPException

class register_form_output(BaseModel):
    success: bool

class ticket_form_output(BaseModel):
    lat: float
    lng: float

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class TransportEnum(AutoName):
    CAR = auto()
    BIKE = auto()
    FOOT = auto()

class register_form_input(BaseModel):
    email: EmailStr
    password: str
    first: str
    last: str
    age: int
    address: str
    volunteer: bool
    transport: Optional[TransportEnum]

class FullUserData(register_form_input):
    _id: str
    points: int
    trips: int
    hours: float
    active_order: Optional[str]
    orders_completed: List[str]

    def change_password(self, new_password: str):
        try:
            assert len(new_password) >= 8
        except:
            raise HTTPException(
                    status_code=422,
                    detail="Password does not meet minimum length requirement (length >= 10)"
                    )
        self.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, pwd: str) -> bool:
        match = bcrypt.checkpw(pwd.encode('utf-8'), self.password.encode('utf-8'))
        return match

class login_form(BaseModel):
    email: str
    password: str

class StatusEnum(AutoName):
    CREATED = auto()
    ACCEPTED = auto()
    PICKED_UP = auto()
    INVALID = auto()
    COMPLETED = auto()

class ticket_form_input(BaseModel):
    destinationAddress: str
    orderNumber: str #from store confirmation email or smth
    author: str
    phone: str
    expireAt: datetime

class FullTicketInfo(ticket_form_input):
    _id: str
    created: datetime
    status: StatusEnum
    volunteer: Optional[str]

    def check_address(self, address):
        agent = geopy.Nominatim(user_agent="default")
        location = agent.geocode(address)
        if location is None:
            raise HTTPException(
                    status_code=422,
                    detail="Address could not be verified"
                    )
        return (location.latitude, location.longitude)

