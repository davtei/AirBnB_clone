#!/usr/bin/python3
"""The User module."""

from models.base_model import BaseModel


class User(BaseModel):
    """A class for creating a User object."""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
