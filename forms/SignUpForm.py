from wtforms import StringField, validators, SubmitField, PasswordField
from flask_wtf import FlaskForm

class SignUpForm(FlaskForm):
    ### ID
    account = StringField("ID", validators=[
        validators.InputRequired()
    ])

    ### Password
    pwd1 = PasswordField("Password", validators=[
        validators.input_required()
    ])

    ### Password check
    pwd2 = PasswordField("Confirm Password", validators=[
        validators.input_required(),
        validators.equal_to(pwd1, message='Passwords must match')
    ])

    ### name
    name = StringField("Name", validators=[
        validators.input_required()
    ])

    ### email
    email = StringField("Email", validators=[
        validators.input_required()
    ])

    ### phone
    pNum = StringField("Phone", validators=[
        validators.input_required()
    ])

    ### Submit button
    submit2 = SubmitField("Submit")
