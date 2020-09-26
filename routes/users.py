import logging

from fastapi import APIRouter, Depends
from typing import Optional

from starlette.exceptions import HTTPException

import util.users as util
import docs.users as docs
import models.users as models

#  from util.auth import get_token_from_header
from config.db import get_database

router = APIRouter()
# set local tag for docs
DOC_TAG = "User Operations"

# takes in UserInDB object from body and returns a token if registration successful
@router.post(
    "/users/register",
    response_model=models.register_form_output,
    tags=[DOC_TAG],
    description=docs.register_description,
    summary=docs.register_summary,
    status_code=201,
)
async def register(form: models.register_form_input):
    logging.info(f"starting register user form with data: {form}")
    # unpack dict
    db = await get_database()
    response = await util.register_user(form, db)
    return response
