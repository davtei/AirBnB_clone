#!/usr/bin/python3
"""The Review module."""

from models.base_model import BaseModel


class Review(BaseModel):
    """A class for creating a Review object."""

    place_id = ""
    user_id = ""
    text = ""
