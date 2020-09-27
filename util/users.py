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
    except Exception as e:
        raise Exception(f"Database exception: {e}")
    if not document:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return document


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
    lat, long = await check_address(form.destinationAddress)
    ticket = models.FullTicketInfo(
        **form.dict(),
        created=datetime.now(),
        status=models.StatusEnum.CREATED.value,
        volunteer=None,
        latitude=lat,
        longitude=long,
    )
    order_id = str(uuid.uuid4())
    order_dict = ticket.dict()
    order_dict.update(
        {
            "_id": order_id,
            "status": models.StatusEnum.CREATED.value,
        }
    )
    # set author's active order
    user_query = {"_id": ticket.author}
    user = await find_user(user_query, db)
    user["active_order"] = order_dict["_id"]
    await update_user({"_id": order_dict["author"]}, user, db)
    column.insert_one(order_dict)
    return models.ticket_form_output(lat=lat, lng=long, order_id=order_dict["_id"])


async def cancel_ticket(form, db):
    return 0


async def find_ticket(query, db):
    column = db["carecart"]["tickets"]
    try:
        document = column.find_one(query)
    except:
        raise Exception("Database exception")
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )
    return document


async def update_ticket(query, updated_ticket, db):
    column = db["carecart"]["tickets"]
    try:
        column.update(query, updated_ticket)
    except:
        raise Exception("Database exception")


async def update_user(query, updated_user, db):
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

    ticket["status"] = models.StatusEnum.ACCEPTED.value
    await update_ticket(ticket_query, ticket, db)

    document["active_order"] = ticket_id
    await update_user(user_query, document, db)


async def close_ticket(ticket_id, email, db):
    user_query = {"email": email}
    document = await find_user(user_query, db)

    ticket_query = {"_id": ticket_id}
    ticket = await find_ticket(ticket_query, db)

    ticket["status"] = models.StatusEnum.COMPLETED.value
    await update_ticket(ticket_query, ticket, db)

    document["orders_completed"].append(ticket_id)
    document["trips"] += 1
    document["hours"] += 1
    document["active_order"] = None
    await update_user(user_query, document, db)


async def all_tickets(db):
    column = db["carecart"]["tickets"]
    try:
        documents = column.find({"orderNumber": "#312342132"})
    except:
        raise Exception("Database exception")
    if not documents:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )
    tickets = [models.FullTicketInfo(**x) for x in documents]
    #  documents = [x for x in documents]
    #  for document in documents:
    #  tickets.append(models.FullTicketInfo(**document))
    return tickets
