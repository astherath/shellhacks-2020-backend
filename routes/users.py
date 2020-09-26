import logging

from fastapi import APIRouter, Depends
from typing import Optional

from starlette.exceptions import HTTPException

import util.users as util
import docs.users as docs
import models.users as models

from util import auth
from config.db import get_database

router = APIRouter()
# set local tag for docs
DOC_TAG = "User Operations"

# takes in register_form_input object from body and returns a token if registration successful
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
    user_id = await util.register_user(form, db)
    # make token to return
    token = awit auth.create_access_token(user_id)
    return models.register_form_output(token=token)

# takes in login_form object from body and returns a token if login successful
@router.post(
        "/users/login",
        response_model=models.login_form,
        tags=[DOC_TAG],
        description=docs.login_description,
        summary=docs.login_summary,
        status_code=201,
        )
async def login(form: models.login_form):
    #TODO: Fix login
    logging.info(f"starting user login with data: {form}")
    # unpack dict
    db = await get_database()
    #response = await util.register_user(form, db)
    return None

# takes in ticket_form_input object from body and returns a token if ticket creation was successful
@router.post(
        "/users/create_ticket",
        response_model=models.ticket_form_input,
        tags=[DOC_TAG],
        description=docs.create_ticket_description,
        summary=docs.create_ticket_summary,
        status_code=201,
        )
async def create_ticket(form: models.ticket_form_input):
    logging.info(f"starting ticket creation with data: {form}")
    # unpack dict
    db = await get_database()
    response = await util.create_ticket(form, db)
    return response
