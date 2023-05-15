#!/usr/bin/python3
"""The FileStorage module."""

import json
import os
import datetime


class FileStorage:
    """A class that serializes object instances to a JSON file and deserializes
    JSON file to instances.
    This is used for storing and retrieving object data.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Public instance method that returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Method that creates obj with key <obj class name>.id
        for __objects.
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Method that serializes __objects to the JSON file
        (path: __file_path).
        """
        with open(FileStorage.__file_path, 'w', encoding="utf-8") as jfile:
            d = {key: v.to_dict() for key, v in FileStorage.__objects.items()}
            json.dump(d, jfile)

    def classes(self):
        """Method that returns a dictionary of valid classes and their
        references.
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def reload(self):
        """Method that deserializes the JSON file to __objects (only if the
        JSON file (__file_path) exists, otherwise, does nothing and raises
        no exception).
        """
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, 'r', encoding="utf-8") as jfile:
            obj_dict = json.load(jfile)
            obj_dict = {key: self.classes()[value["__class__"]](**value)
                        for key, value in obj_dict.items()}
            FileStorage.__objects = obj_dict

    def attributes(self):
        """Method that returns the classname and their attributes."""
        attribute = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
            }
        return attribute