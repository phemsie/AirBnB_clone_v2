
AgeseVictor
/
AirBnB_clone_v2
Public
Code
Issues
Pull requests
Actions
Projects
Security
Insights
AirBnB_clone_v2/console.py
@AgeseVictor
AgeseVictor the work is done
 1 contributor
Executable File  275 lines (260 sloc)  9.09 KB
#!/usr/bin/python3
""" the console module for AirBnB"""
import cmd
import sys
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from shlex import split


class HBNBCommand(cmd.Cmd):
    """
    entry point of the command interpreter it contains the
    functionality of the console
    """
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    classes = {"BaseModel", "User", "State", "City",
               "Amenity", "Place", "Review"}

    def emptyline(self):
        '''skips empty spaces'''
        pass

    def do_quit(self, args):
        ''' defines quit to exit the console '''
        return True

    def do_EOF(self, args):
        ''' to exit the console at end of file '''
        return True

    def do_create(self, args):
        ''' Creates an object of any class
        Exceptions:
            SyntaxError: there is no args given
            NameError: there is no object that has the name
        '''
        try:
            if not args:
                raise SyntaxError()
            args_list = split(args)
            if len(args_list) >= 1:
                obj = eval("{}()".format(args_list[0]))
                for i in range(1, len(args_list)):
                    arg_split = args_list[i].split("=")
                    if isinstance(arg_split[1], str):
                        arg_split[1] = arg_split[1].replace("_", " ")
                    try:
                        setattr(obj, arg_split[0], eval(arg_split[1]))
                    except (SyntaxError, NameError):
                        setattr(obj, arg_split[0], arg_split[1])
                storage.new(obj)
                storage.save()
                print("{}".format(obj.id))
            else:
                raise SyntaxError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, args):
        '''
        displays the object instance
        Exceptions:
            SyntaxError: there is no args given
            NameError: there is no object taht has the name
            IndexError: there is no id given
            KeyError: there is no valid id given
        '''
        try:
            if not args:
                raise SyntaxError()
            arg_list = args.split(" ")
            if arg_list[0] not in self.classes:
                raise NameError()
            if len(arg_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = arg_list[0] + '.' + arg_list[1]
            if key in objects:
                print(objects[key])                
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        '''
        Deletes an object specified class name and id
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        '''
        try:
            if not args:
                raise SyntaxError()
            arg_list = args.split(" ")
            if arg_list[0] not in self.classes:
                raise NameError()
            if len(arg_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = arg_list[0] + '.' + arg_list[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, args):
        '''
        shows all objects of a class
        Exceptions:
            NameError: when there is no object taht has the name
        '''
        objects = storage.all()
        arg_list = []
        if not args:
            for key in objects:
                arg_list.append(objects[key])
            print(arg_list)
            return
        try:
            args_list = args.split(" ")
            if args_list[0] not in self.classes:
                raise NameError()
            for key in objects:
                name = key.split('.')
                if name[0] == args_list[0]:
                    arg_list.append(objects[key])
            print(arg_list)
        except NameError:
            print("** class doesn't exist **")

    def do_update(self, args):
        '''
        Updates an instance with new info
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
            AttributeError: when there is no attribute given
            ValueError: when there is no value given
        '''
        try:
            if not args:
                raise SyntaxError()
            arg_list = split(args, " ")
            if arg_list[0] not in self.classes:
                raise NameError()
            if len(arg_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = arg_list[0] + '.' + arg_list[1]
            if key not in objects:
                raise KeyError()
            if len(arg_list) < 3:
                raise AttributeError()
            if len(arg_list) < 4:
                raise ValueError()
            v = objects[key]
            try:
                v.__dict__[arg_list[2]] = eval(arg_list[3])
            except Exception:
                v.__dict__[arg_list[2]] = arg_list[3]
                v.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")

    def count(self, args):
        '''
        counts the number of instances of a class
        '''
        counter = 0
        try:
            arg_list = split(args, " ")
            if arg_list[0] not in self.classes:
                raise NameError()
            objects = storage.all()
            for key in objects:
                name = key.split('.')
                if name[0] == arg_list[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        '''
        strips the argument and return a string of command
        Args:
            args: input list of args
        Return:
            returns string of argumetns
        '''
        new_list = []
        new_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def default(self, args):
        '''
        retrieve all instances of a class and
        retrieve the number of instances
        '''
        arg_list = args.split('.')
        if len(arg_list) >= 2:
            if arg_list[1] == "all()":
                self.do_all(arg_list[0])
            elif arg_list[1] == "count()":
                self.count(arg_list[0])
            elif arg_list[1][:4] == "show":
                self.do_show(self.strip_clean(arg_list))
            elif arg_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(arg_list))
            elif arg_list[1][:6] == "update":
                args_list = self.strip_clean(arg_list)
                if isinstance(args_list, list):
                    obj = storage.all()
                    key = args_list[0] + ' ' + args_list[1]
                    for k, v in args_list[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args_list)
        else:
            cmd.Cmd.default(self, args)


if __name__ == '__main__':
    HBNBCommand().cmdloop()

