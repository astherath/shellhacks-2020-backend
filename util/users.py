import models.users as models
import bcrypt
import uuid

async def register_user(form, db):
    column = db["carecart"]["users"]
    user = models.FullUserData(form,
                             _id=uuid.uuid4(),
                             points=0,
                             trips=0,
                             hours=0.0)
    user.change_password(user.password)
    column.insert_one(user.dict())
    return models.register_form_output(success=True)