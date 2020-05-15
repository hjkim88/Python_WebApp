from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Regexp

class SignUpForm(FlaskForm):
    ### ID
    account2 = StringField("ID", validators=[
        InputRequired()
    ])

    ### Password
    pwd1 = PasswordField("Password", validators=[
        InputRequired(),
        Length(min=6, message='Password must be at least 6 lengths')
    ])

    ### Password check
    pwd2 = PasswordField("Confirm Password", validators=[
        EqualTo('pwd1', message='Passwords must match')
    ])

    ### name
    name = StringField("Name", validators=[
        InputRequired()
    ])

    ### email
    email = StringField("Email", validators=[
        InputRequired(),
        Regexp(regex='.@stjude.org$', message='It should be St Jude email')
    ])

    ### phone
    pNum = StringField("Phone", validators=[
        InputRequired()
    ])

    ### Submit button
    submit2 = SubmitField("Submit")
