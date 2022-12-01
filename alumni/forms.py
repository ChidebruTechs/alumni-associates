import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, EqualTo, Length
from flask_ckeditor import CKEditorField


class BlogForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    # content = StringField('Content:', validators=[DataRequired()], widget=TextArea())
    content = CKEditorField('Content:',  validators=[DataRequired()])
    author = StringField('Author:', validators=[DataRequired()])
    slug = StringField('Slug:', validators=[DataRequired()])
    submit = SubmitField('Submit') 

class UserForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(), EqualTo('password', message='Passwords Must Match!')])
    confirm = PasswordField('Confirm Password:', validators=[DataRequired()])
    submit = SubmitField('Register') 


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login') 

class ContactForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    title = StringField('Title:', validators=[DataRequired()])
    message = StringField('Message:', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Submit') 


class MemberForm(FlaskForm):
    firstname = StringField('First Name:', validators=[DataRequired()])
    lastname = StringField('Last Name:', validators=[DataRequired()])
    gender = StringField('Gender:', validators=[DataRequired()])
    cohort = StringField('Cohort:', validators=[DataRequired()])
    profession = StringField('Profession:', validators=[DataRequired()])
    location = StringField('Location:', validators=[DataRequired()])
    submit = SubmitField('ADD') 

class ProfileForm(FlaskForm):
    status = StringField('Marital Status:', validators=[DataRequired()])
    profession = StringField('Profession:', validators=[DataRequired()])
    location = StringField('Location:', validators=[DataRequired()])
    phone = StringField('Phone:', validators=[DataRequired()])
    linkedin = StringField('Linkedin:', validators=[DataRequired()])
    youtube = StringField('YouTube:', validators=[DataRequired()])
    facebook = StringField('Facebook:', validators=[DataRequired()])
    twitter = StringField('Twitter:', validators=[DataRequired()])
    instagram = StringField('Instagram:', validators=[DataRequired()])
    tiktok = StringField('Tik Tok:', validators=[DataRequired()])
    submit = SubmitField('Update') 


class SearchForm(FlaskForm):
    searching = StringField('Searching:', validators=[DataRequired()])
    submit = SubmitField('Submit') 
