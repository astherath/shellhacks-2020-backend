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
    token = await auth.create_access_token(user_id)
    return models.register_form_output(token=token)


# takes in login_form object from body and returns a token if login successful
@router.post(
    "/users/login",
    response_model=models.register_form_output,
    tags=[DOC_TAG],
    description=docs.login_description,
    summary=docs.login_summary,
    status_code=201,
)
async def login(form: models.login_form):
    logging.info(f"starting user login with data: {form}")
    # unpack dict
    db = await get_database()
    response = await util.login_user(form, db)
    token = await auth.create_access_token(response)
    return models.register_form_output(token=token)


# takes in ticket_form_input object from body and returns a token if ticket creation was successful
@router.post(
    "/users/create_ticket",
    response_model=models.ticket_form_output,
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


# takes in cancel_ticket_request object from body and returns a token if ticket cancellation was successful
@router.post(
    "/users/cancel_ticket",
    response_model=models.cancel_ticket_request,
    tags=[DOC_TAG],
    description=docs.cancel_ticket_description,
    summary=docs.cancel_ticket_summary,
    status_code=201,
)
async def cancel_ticket(form: models.cancel_ticket_request):
    logging.info(f"starting ticket cancellation with data: {form}")
    # unpack dict
    db = await get_database()
    response = await util.cancel_ticket(form, db)
    return response


@router.get(
    "/users/accept_ticket",
    tags=[DOC_TAG],
    description=docs.accept_ticket_desc,
    summary=docs.accept_ticket_summ,
    status_code=204,
)
async def accept_ticket(ticket: str, header: str = Depends(auth.get_token_from_header)):
    logging.info(f"starting ticket acceptance with data: {ticket}, {header}")
    # check credentials
    payload = await auth.decode(header)
    # unpack dict
    db = await get_database()
    await util.accept_ticket(ticket, payload["data"], db)


@router.get(
    "/users/close_ticket",
    tags=[DOC_TAG],
    description=docs.close_ticket_desc,
    summary=docs.close_ticket_summ,
    status_code=204,
)
async def close_ticket(ticket: str, header: str = Depends(auth.get_token_from_header)):
    logging.info(f"starting ticket acceptance with data: {ticket}, {header}")
    # check credentials
    payload = await auth.decode(header)
    # unpack dict
    db = await get_database()
    await util.close_ticket(ticket, payload["data"], db)


@router.get(
    "/users/all_tickets",
    response_model=models.ticket_list,
    tags=[DOC_TAG],
    description=docs.all_tickets_desc,
    summary=docs.all_tickets_summ,
    status_code=201,
)
async def all_tickets(header: str = Depends(auth.get_token_from_header)):
    logging.info(f"starting get all tickets")
    # check credentials
    payload = await auth.decode(header)
    # unpack dict
    db = await get_database()
    tickets = await util.all_tickets(db)
    return models.ticket_list(tickets=tickets)