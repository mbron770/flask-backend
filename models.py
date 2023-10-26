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
    clerkID = db.Column(db.String, unique=True)
    
    messages_sent = db.relationship(
        'Message', primaryjoin="User.clerkID == foreign(Message.sender)", back_populates='message_sender'
    )

    messages_received = db.relationship(
        'Message', primaryjoin="User.clerkID == foreign(Message.recipient)", back_populates='message_recipient'
    )
    
    serialize_rules = ('messages_sent', 'messages_received',)

class Message(db.Model, SerializerMixin): 
    __tablename__ = 'messages' 
    
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String, db.ForeignKey('users.clerkID'))
    recipient = db.Column(db.String, db.ForeignKey('users.clerkID'))
    dateTime = db.Column(db.DateTime)
    content = db.Column(db.String)
    
    message_sender = db.relationship('User', foreign_keys=[sender], back_populates='messages_sent')
    message_recipient = db.relationship('User', foreign_keys=[recipient], back_populates='messages_received')

    
    # serialize_rules = ('message_sender','message_recipient',)