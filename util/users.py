import models.users as models


async def register_user(form, db):
    column = db["carecart"]["users"]
    column.insert_one(form.dict())
    return models.register_form_output(success=True)
