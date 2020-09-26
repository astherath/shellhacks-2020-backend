import models.users as models
import bcrypt
import uuid
import geopy
from datetime import datetime

async def register_user(form, db):
    column = db["carecart"]["users"]
    user = models.FullUserData(form,
                             _id=uuid.uuid4(),
                             points=0,
                             trips=0,
                             hours=0.0,
                             active_order=None,
                             orders_completed=[])
    user.change_password(user.password)
    column.insert_one(user.dict())
    return models.register_form_output(success=True)

async def create_ticket(form, db):
    column = db["carecart"]["tickets"]
    ticket = models.FullTicketInfo(form,
                                _id=uuid.uuid4(),
                                created=datetime.now(),
                                status=models.StatusEnum.CREATED,
                                volunteer=None)
    (lat, lng) = ticket.check_address(ticket.address)
    column.insert_one(ticket.dict)
    return models.ticket_form_output(lat=lat,lng=lng,order_id=ticket._id)
    

