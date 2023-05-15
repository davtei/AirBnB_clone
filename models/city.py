#!/usr/bin/python3
"""The City module."""

from models.base_model import BaseModel


class City(BaseModel):
    """A class for creating a city object."""

    state_id = ""
    name = ""