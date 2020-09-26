import models.users as models
import bcrypt
import uuid
import geopy
from datetime import datetime


async def register_user(form, db):
    column = db["carecart"]["users"]
    user = models.FullUserData(
        form,
        _id=str(uuid.uuid4()),
        points=0,
        trips=0,
        hours=0.0,
        active_order=None,
        orders_completed=[],
    )
    user.change_password(user.password)
    column.insert_one(user.dict())
    return user._id


async def create_ticket(form, db):
    column = db["carecart"]["tickets"]
    ticket = models.FullTicketInfo(
        form,
        _id=str(uuid.uuid4()),
        created=datetime.now(),
        status=models.StatusEnum.CREATED,
        volunteer=None,
    )
    (lat, lng) = ticket.check_address(ticket.address)

    # set author's active order
    user = user_column.find_one({"_id": ticket.author})
    user.active_order = ticket._id
    user_column.insert_one(user.dict())

    column.insert_one(ticket.dict)
    return models.ticket_form_output(lat=lat, lng=lng, order_id=ticket._id)


async def cancel_ticket(form, db):
    return 0
