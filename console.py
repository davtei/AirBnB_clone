#!/usr/bin/python3
"""The Console module."""

import cmd
import re
from models import storage
from models.base_model import BaseModel
import json


class HBNBCommand(cmd.Cmd):
    """A class that creates a command interpreter."""

    prompt = "(hbnb) "

    def do_quit(self, line):
        """Method to exit the program."""
        return True

    def do_EOF(self, line):
        """Method to handle EOF."""
        print()
        return True

    def emptyline(self):
        """Method that handles empty line inputs."""
        pass

    def default(self, line):
        """Method that handles unkown commands."""
        self._precmd(line)

    def _precmd(self, line):
        """Method to process input commands."""
        cmatch = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not cmatch:
            return line
        classname = cmatch.group(1)
        method = cmatch.group(2)
        args = cmatch.group(3)
        match_uid_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_args:
            uid = match_uid_args.group(1)
            attr_or_dict = match_uid_args.group(2)
        else:
            uid = args
            attr_or_dict = False
        attr_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_value:
                attr_value = (match_attr_value.group(
                    1) or "") + " " + (match_attr_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_value
        self.onecmd(command)
        return command

    def do_create(self, line):
        """Creates a new instance of BaseModel."""
        if line == "" or line is None:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            bm = storage.classes()[line]()
            bm.save()
            print(bm.id)

    def do_show(self, line):
        """Method that prints the string representation of an instance based
        on the class name and id.
        """
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        """Method that deletes an instance based on the class name and id.
        The change is saved into the JSON file.
        """
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, line):
        """Method that prints all string representation of all instances based
        or not on the class name.
        """
        if line != "":
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                nlst = [str(obj) for key, obj in storage.all().items()
                        if type(obj).__name__ == words[0]]
                print(nlst)
        else:
            nlist = [str(obj) for key, obj in storage.all().items()]
            print(nlist)

    def update_dict(self, classname, uid, s_dict):
        """Method that updates an instance based on its id to a dictionary."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_update(self, line):
        """Method that updates an instance based on the class name and id
        by adding or updating attribute.
        The change is saved into the JSON file).
        """
        if line == "" or line is None:
            print("** class name missing **")
            return
        regx = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(regx, line)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_count(self, line):
        """Method that gives the count of instances of a class."""
        words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
        elif words[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(words[0] + '.')]
            print(len(matches))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
