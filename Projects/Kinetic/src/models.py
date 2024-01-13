from __future__ import annotations
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey 
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class userprofile(db.Model):
    
    user_id = db.Column(db.Integer, primary_key = True)
    user_password = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False, unique=True) # add unique
    birth_date = db.Column(db.Date, nullable=False) #check db.Date not sure if thats right
    full_name = db.Column(db.String(255),nullable=False)
    country = db.Column(db.String(255),nullable=False)
    username = db.Column(db.String(255),nullable=False, unique=True)
    profile_path = db.Column(db.String(255),nullable=False)

class friendlist(db.Model):
    
    relationship_id = db.Column(db.Integer, primary_key = True)
    user_request = db.Column(db.Integer, ForeignKey("userprofile.user_id"))
    user_accept = db.Column(db.Integer, ForeignKey("userprofile.user_id"))
    accepted = db.Column(db.Boolean,nullable=False)

class post(db.Model):

    post_id = db.Column(db.Integer, primary_key = True)
    poster_id = db.Column(db.Integer, ForeignKey("userprofile.user_id"))
    post_datetime = db.Column(db.DateTime, nullable=False)
    post_entry = db.Column(db.String(255),nullable=False)
    poster_full_name = db.Column(db.String(255),nullable=False)

class comments(db.Model):

    comment_id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer, ForeignKey("post.post_id"))
    commenter_id = db.Column(db.Integer, ForeignKey("userprofile.user_id"))
    commenter_name = db.Column(db.String(255), nullable=False)
    comment_entry = db.Column(db.String(255),nullable=False)
    comment_datetime = db.Column(db.DateTime , nullable = False)

class chat(db.Model):
    
    chat_id = db.Column(db.Integer, primary_key = True)
    send_id = db.Column(db.Integer, ForeignKey("userprofile.user_id"))
    receive_id = db.Column(db.Integer, ForeignKey("userprofile.user_id"))
    send_name = db.Column(db.String(255), nullable=False)
    receive_name = db.Column(db.String(255), nullable=False)

class message(db.Model):
    
    message_id = db.Column(db.Integer, primary_key = True)
    chat_id = db.Column(db.Integer, ForeignKey("chat.chat_id"))
    message_entry = db.Column(db.String(255), nullable=False)
    sent_time = db.Column(db.DateTime, nullable=False)
    send_id = db.Column(db.Integer, ForeignKey("userprofile.user_id"))
    receive_id = db.Column(db.Integer, ForeignKey("userprofile.user_id"))
    send_name = db.Column(db.String(255), nullable=False)
    receive_name = db.Column(db.String(255), nullable=False)

class postlike(db.Model):

    postlike_id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer, ForeignKey("post.post_id"))
    like_name = db.Column(db.String(255), nullable=False)
    liker_id = db.Column(db.Integer, ForeignKey("userprofile.user_id"))

class commentlike(db.Model):

    commentlike_id = db.Column(db.Integer, primary_key = True)
    comment_id = db.Column(db.Integer, ForeignKey("comments.comment_id"))
    like_name = db.Column(db.String(255), nullable=False)
    liker_id = db.Column(db.Integer, ForeignKey("userprofile.user_id"))




