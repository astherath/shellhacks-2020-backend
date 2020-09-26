import models.users as models
import bcrypt
import uuid
import geopy
from datetime import datetime
from config.main import AGENT
from starlette.exceptions import HTTPException

async def check_address(address):
        location = AGENT.geocode(address)
        if not location:
            raise HTTPException(status_code=422, detail="Address could not be verified")
        return (location.latitude, location.longitude)

async def register_user(form, db):
    column = db["carecart"]["users"]
    user = models.FullUserData(
        **form.dict(),
        points=0,
        trips=0,
        hours=0.0,
        active_order=None,
        orders_completed=[],
    )
    if user.age < 16:
        raise HTTPException(status_code=422, detail="Too young!")
    user.change_password(user.password)
    user_dict = user.dict()
    user_id = str(uuid.uuid4())
    user_dict["_id"] = user_id
    await check_address(user.address)
    column.insert_one(user_dict)
    return user_id


async def create_ticket(form, db):
    column = db["carecart"]["tickets"]
    ticket = models.FullTicketInfo(
        form,
        _id=str(uuid.uuid4()),
        created=datetime.now(),
        status=models.StatusEnum.CREATED,
        volunteer=None,
    )
    (lat, lng) = check_address(ticket.address)

    # set author's active order
    user = user_column.find_one({"_id": ticket.author})
    user.active_order = ticket._id
    user_column.insert_one(user.dict())

    column.insert_one(ticket.dict)
    return models.ticket_form_output(lat=lat, lng=lng, order_id=ticket._id)


async def cancel_ticket(form, db):
    return 0
