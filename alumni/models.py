from alumni import  db
from flask_login import UserMixin
from datetime import datetime




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180))
    status = db.Column(db.Integer, default=1, nullable=False)
    # profile = db.Column(db.String(180), unique=False, nullable=False, default='profile.jpg')


    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    def __repr__(self):
        return f"User('{self.id }' , '{self.email }' , '{ self.username }',  '{ self.password }' , '{self.status}')"


class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80),  nullable=False)
    gender = db.Column(db.String(80),  nullable=False)
    cohort = db.Column(db.String(80),  nullable=False)
    profession = db.Column(db.String(80),  nullable=False)
    location = db.Column(db.String(80),  nullable=False)

    def __init__(self, firstname, lastname, gender, cohort, profession, location):
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.cohort = cohort
        self.profession = profession
        self.location = location

    def  __repr__(self) :
        return f"Members('{self.id }' , '{self.firstname }' , '{ self.lastname }' , '{ self.cohort}' , '{self.profession}' , '{self.location}' , '{self.gender}')"


class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text,  nullable=False)
    author = db.Column(db.String(80),  nullable=False)
    blog_date = db.Column(db.DateTime,  default=datetime.now)
    slug = db.Column(db.String(80),  nullable=False)

    def __init__(self, title, content, author, slug):
        self.title = title
        self.content = content
        self.author = author
        self.slug = slug

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(80), nullable=False)
    profession = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    youtube = db.Column(db.String(80), nullable=False)
    linkedin = db.Column(db.String(80), nullable=False)
    facebook = db.Column(db.String(80), nullable=False)
    twitter = db.Column(db.String(80), nullable=False)
    instagram = db.Column(db.String(80), nullable=False)
    tiktok = db.Column(db.String(80), nullable=False)

    def __init__(self, status, profession, location,  phone, youtube, linkedin, facebook, twitter, instagram, tiktok):
        self.status = status
        self.profession = profession
        self.location = location
        self.phone = phone
        self.youtube = youtube
        self.linkedin = linkedin
        self.facebook = facebook
        self.twitter = twitter
        self.instagram = instagram
        self.tiktok = tiktok
