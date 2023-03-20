#!/usr/bin/python3
""" This module defines DBStorage class """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv


class DBStorage():
    ''' Class definition for DBStorage '''
    __engine = None
    __session = None

    def __init__(self):
        ''' class constructors dbStorage '''
        db_user = getenv('HBNB_MYSQL_USER')
        db_pwd = getenv('HBNB_MYSQL_PWD')
        db_host = getenv('HBNB_MYSQL_HOST')
        db_db = getenv('HBNB_MYSQL_DB')
        db_env = getenv('HBNB_ENV')

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                db_user, db_pwd, db_host, db_db), pool_pre_ping=True)

        if db_env == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        '''
        Returns a dictionary of __object
        '''
        dict_return = {}
        if cls:
            cls = eval(cls) if type(cls) == str else cls
            objs = self.__session.query(cls).all()
        else:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Amenity).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
        for obj in objs:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            dict_return[key] = obj
        return dict_return

    def new(self, obj):
        ''' Adds a new element to the database '''
        self.__session.add(obj)

    def save(self):
        ''' Saves all changes to database  '''
        self.__session.commit()

    def delete(self, obj=None):
        ''' Deletes an element from the database '''
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        ''' Creates all tables on the database '''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        ''' Closes and stops the session '''
        self.__session.close()
