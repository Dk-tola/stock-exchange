from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp,
    InputRequired,
)


class ContactForm(FlaskForm):
    name = StringField("Name", [DataRequired("Please enter your name !")])
    email = StringField(
        "Email", [DataRequired("Please enter you email address !"), Email()]
    )
    subject = StringField("Subject", [DataRequired("Please enter a Subject !")])
    message = StringField("Message", [DataRequired("Enter a message !")])
    submit = SubmitField("Submit")


class GmailCode(FlaskForm):
    code = StringField("Code", [DataRequired("Please enter your code her!")])
    submit = SubmitField("Submit")
