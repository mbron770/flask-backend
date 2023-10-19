from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from database import db


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)



class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    clerkID = db.Column(db.String)
    
    # def to_dict(self):
    #     return {
    #     'id': self.id,
    #     'name': self.name,
    #     'username': self.username,
    #     'clerkID': self.clerkID
    # }
    
    
    
    # def __repr__(self):
    #     return f'id: {self.id} name: {self.name} username: {self.username} clerkID: {self.clerkID}'
    