import bcrypt
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum, auto
from typing import Optional
from starlette.exceptions import HTTPException

class register_form_output(BaseModel):
    success: bool

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class TransportEnum(AutoName):
    CAR = auto()
    BIKE = auto()
    FOOT = auto()

class StatusEnum(AutoName):
    CREATED = auto()
    ACCEPTED = auto()
    PICKED_UP = auto()
    INVALID = auto()
    COMPLETED = auto()

class register_form_input(BaseModel):
    email: EmailStr
    password: str
    first: str
    last: str
    age: int
    address: str
    volunteer: bool
    transport: TransportEnum

class FullUserData(register_form_input):
    _id: str
    points: int
    trips: int
    hours: float

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


class ticket_form_input(BaseModel):
    created: datetime
    destinationAddress: str
    orderNumber: str
    author: str
    status: StatusEnum
    volunteer: Optional[str]
    contactInfo: str
    expireAt: datetime

