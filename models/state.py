#!/usr/bin/python3
"""This module defines the state class"""
import os
import models
from models.base_model import (BaseModel, Base)
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    '''
    This is class definition for State
    Attributes:
        name: input name
    '''

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")

    else:
        @property
        def cities(self):
            '''Get cities by state'''
            cities_list = []
            for city_id, city in models.storage.all(City).items():
                if self.id == city.state_id:
                    cities_list.append(city)
            return cities_list
