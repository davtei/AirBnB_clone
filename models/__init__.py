#!/usr/bin/env python3
"""
Documentation for the models module.

The storage module is a singleton that uses FileStorage
to manage objects and their persistence in a file called file.json.
"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
