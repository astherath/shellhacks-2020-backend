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


async def find_user(query, db):
    column = db["carecart"]["users"]
    try:
        document = column.find_one(query)
        if not document:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )
        return document
    except:
        raise Exception("Database exception")


async def login_user(form, db):
    query = {"email": form.email}
    document = await find_user(query, db)
    match = models.FullUserData(**document).check_password(form.password)
    if not match:
        raise HTTPException(
            status_code=403,
            detail="Incorrect password",
        )
    return form.email


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


async def find_ticket(query, db):
    column = db["carecart"]["tickets"]
    try:
        document = column.find_one(query)
        if not document:
            raise HTTPException(
                status_code=404,
                detail="Ticket not found",
            )
        return document
    except:
        raise Exception("Database exception")


async def update_ticket(query, updated_ticket):
    column = db["carecart"]["tickets"]
    try:
        column.update(query, updated_ticket)
    except:
        raise Exception("Database exception")


async def update_user(query, updated_user):
    column = db["carecart"]["users"]
    try:
        column.update(query, updated_user)
    except:
        raise Exception("Database exception")


async def accept_ticket(ticket_id, email, db):
    user_query = {"email": email}
    document = await find_user(user_query, db)

    ticket_query = {"_id": ticket_id}
    ticket = await find_ticket(ticket_query, db)

    ticket["status"] = models.StatusEnum.ACCEPTED
    await update_ticket(ticket_query, ticket)

    document["active_order"] = ticket_id
    await update_user(user_query, document)


# TODO: for use in close ticket method
#  document["orders_completed"].append(ticket_id)
#  document["trips"] += 1
#  document["hours"] += 1
