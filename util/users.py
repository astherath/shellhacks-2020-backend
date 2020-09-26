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
    user_column = db["carecart"]["users"]
    ticket = models.FullTicketInfo(form,
                                _id=uuid.uuid4(),
                                created=datetime.now(),
                                status=models.StatusEnum.CREATED,
                                volunteer=None)
    (lat, lng) = ticket.check_address(ticket.address)
    user = user_column.find_one({'_id': ticket.author})
    user.active_order = ticket._id
    user_column.insert_one(user.dict())
    column.insert_one(ticket.dict)
    return models.ticket_form_output(lat=lat,lng=lng,order_id=ticket._id)
    

