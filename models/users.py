import bcrypt
import geopy
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum, auto
from typing import Optional, List
from starlette.exceptions import HTTPException


class register_form_output(BaseModel):
    token: str
    user_id: str


class ticket_form_output(BaseModel):
    lat: float
    lng: float
    order_id: str


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
    address: str
    volunteer: bool
    transport: Optional[TransportEnum]


class FullUserData(register_form_input):
    points: int
    trips: int
    hours: float
    active_order: Optional[str]
    orders_completed: List[str]

    def change_password(self, new_password: str):
        try:
            assert len(new_password) >= 6
        except:
            raise HTTPException(
                status_code=422,
                detail="Password does not meet minimum length requirement (length >= 6)",
            )
        self.password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, pwd: str) -> bool:
        match = bcrypt.checkpw(pwd.encode("utf-8"), self.password.encode("utf-8"))
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
    orderNumber: str  # from store confirmation email or smth
    author: str
    phone: str
    expireAt: Optional[datetime] = datetime.now()


class FullTicketInfo(ticket_form_input):
    created: datetime
    status: StatusEnum
    volunteer: Optional[str]
    latitude: float
    longitude: float
    ticket_id: str


class cancel_ticket_request(BaseModel):
    order_id: str
    author_id: str


class ticket_list(BaseModel):
    tickets: List[FullTicketInfo]
