#!/usr/bin/python3
"""This is the place class"""
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Table, Column, Integer, String, Float, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from os import environ

metadata = Base.metadata

'''This is the association table between place and amenity '''
place_amenity = Table('place_amenity', metadata, Column('place_id',
                      String(60), ForeignKey('places.id'),
                      primary_key=True, nullable=False),
                      Column('amenity_id', String(69),
                      ForeignKey('amenities.id'),
                      primary_key=True, nullable=False))


class Place(BaseModel, Base):
    '''
    This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    '''
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    glob_storage = environ.get('HBNB_TYPE_STORAGE')
    if glob_storage == 'db':
        reviews = relationship('Review', backref='places',
                               cascade='all, delete')
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")

    else:
        @property
        def reviews(self):
            '''Return all collected reviews for a state'''
            all_reviews = models.storage.all("Review")
            cust_reviews = []
            for value in all_reviews.values():
                if self.id == value.place_id:
                    cust_reviews.append(value)
            return cust_reviews

        @property
        def amenities(self):
            ''' Returns list of amenity ids '''
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            ''' Appends amenity id's to an attribute '''
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
