from pydantic import BaseModel, EmailStr


class register_form_output(BaseModel):
    success: bool


class register_form_input(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
