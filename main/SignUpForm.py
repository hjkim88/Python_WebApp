from wtforms import Form, StringField, validators, SubmitField, PasswordField
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
        validators.equal_to(pwd1)
    ])

    ### name
    name = StringField("Name", validators=[
        validators.InputRequired()
    ])

    ### email
    email = StringField("Email", validators=[
        validators.InputRequired()
    ])

    ### phone
    pNum = StringField("Phone", validators=[
        validators.InputRequired()
    ])

    ### Submit button
    submit = SubmitField("Submit")
