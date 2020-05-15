from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from evrnmt.config import DevelopmentConfig as Conf
from forms.SignInForm import SignInForm
from forms.SignUpForm import SignUpForm
from flaskext.mysql import MySQL
from main.DBControl import DBControl as Db
from main.AWSControl import AWSControl as Ac
from flask_mail import Mail, Message
from main.EmailControl import EmailControl as Ec
from evrnmt.token import generate_confirmation_token, confirm_token

### Create a Flask app
app = Flask(__name__,
            instance_relative_config=False,
            template_folder="../templates",
            static_folder="../static")
### configure set up from the config file
app.config.from_object('evrnmt.config.ProductionConfig')
### csrf
csrf = CSRFProtect(app)
csrf.init_app(app)
### initiate mysql
mysql = MySQL()
### mysql configurations
app.config['MYSQL_DATABASE_USER'] = Conf.MYSQL_DATABASE_USER
app.config['MYSQL_DATABASE_PASSWORD'] = Conf.MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = Conf.MYSQL_DATABASE_DB
### start mysql app
mysql.init_app(app)
mail = Mail(app)

### a test page - successful
@app.route("/success/<name>")
def success(name):
    return "Hi %s. Your AWS machine has been started." % name

### any test functions that needs to be tested
@app.route("/test/<account>")
def test(account):
    ### get cursor of the DB
    cursor = mysql.connect().cursor()
    db = Db(cursor=cursor)

    if db.is_user_confirmed(account):
        return f"Hey {account}. Your account is confirmed and ready to go."
    else:
        return f"Hey {account}. You are not confirmed. Get the f#$% out of here."

### email test2
@app.route("/test2")
def test2():
    email="firadazer@gmail.com"
    account="user1"
    ec = Ec(mail=mail)
    token = generate_confirmation_token(account=account, secret_key=app.config['SECRET_KEY'], security_pwd_salt=app.config['SECURITY_PASSWORD_SALT'])
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('user_activation.html', confirm_url=confirm_url)
    subject = "AWS Cloud System Account Activation"
    ec.send_email(sender=app.config.get("MAIL_USERNAME"),
                  recipients=[email],
                  subject=subject,
                  content=None,
                  html=html)

    return f"A sign-up confirmation email sent to {email}."

### email
@app.route("/send-email")
def send_email():
    ec = Ec(mail=mail)
    ec.send_email(sender=app.config.get("MAIL_USERNAME"),
                  recipients=["firadazer@gmail.com"],
                  subject="Test email",
                  content="Test email sent. Do not reply to this email.")

    return 'Mail sent!'

### new user verification
@app.route("/confirm/<token>")
def confirm_email(token):
    try:
        account = confirm_token(token=token, secret_key=app.config['SECRET_KEY'], security_pwd_salt=app.config['SECURITY_PASSWORD_SALT'])
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')

    ### get cursor of the DB
    cursor = mysql.connect().cursor()
    db = Db(cursor=cursor)
    result = db.is_user_confirmed(account=account)

    if result[0] == 1:
        flash('Account already confirmed. Please sign in.', 'success')
    else:
        data = db.update_confirmed(account=account, userNum=result[1])
        if len(data) == 0:
            cursor.connection.commit()
            flash('Your email is verified. Thanks!', 'success')
        else:
            flash('Something is wrong. Confirmation failed.')

    return redirect(url_for('home'))

### sign up page
@app.route("/sign-up", methods=['GET', 'POST'])
def signup():
    ### show sign up page
    form2 = SignUpForm(request.form)

    ### if all the required fields are filled out
    if form2.validate_on_submit():
        ### Extract information
        account = request.form["account2"]
        pwd = request.form["pwd1"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["pNum"]

        ### connect to the DB
        cursor = mysql.connect().cursor()
        db = Db(cursor=cursor)

        ### add new user
        data = db.add_new_user(account=account,
                               pwd=pwd,
                               name=name,
                               email=email,
                               phone=phone)

        ### if querying is successful
        if len(data) == 0:
            cursor.connection.commit()

            ### confirmation email
            ec = Ec(mail=mail)
            token = generate_confirmation_token(account=account, secret_key=app.config['SECRET_KEY'], security_pwd_salt=app.config['SECURITY_PASSWORD_SALT'])
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('user_activation.html', confirm_url=confirm_url)
            subject = "AWS Cloud System Account Activation"
            ec.send_email(sender=app.config.get("MAIL_USERNAME"),
                          recipients=[email],
                          subject=subject,
                          content=None,
                          html=html)

            flash("User created successfully!", "success")
        else:
            flash("Enter the required fields", "warning")

        return redirect(url_for('home'))
    else:
        return render_template('sign_up.html', form=form2)

### the result page
def make_result(account, ip, pwd):
    ### Create an HTML header
    def header(text, color='black', gen_text=None):
        if gen_text:
            raw_html = f'<h1 style="margin-top:16px;color: {color};font-size:54px"><center>' + str(
                text) + '<span style="color: red">' + str(gen_text) + '</center></h1>'
        else:
            raw_html = f'<h1 style="margin-top:12px;color: {color};font-size:54px"><center>' + str(
                text) + '</center></h1>'
        return raw_html

    ### Create an HTML box of text
    def box(text, gen_text=None):
        if gen_text:
            raw_html = '<div style="padding:8px;font-size:28px;margin-top:28px;margin-bottom:14px;">' + str(
                text) + '<span style="color: red">' + str(gen_text) + '</div>'

        else:
            raw_html = '<div style="border-bottom:1px inset black;border-top:1px inset black;padding:8px;font-size: 28px;">' + str(
                text) + '</div>'
        return raw_html

    ### Add html contents together
    def addContent(old_html, raw_html):
        old_html += raw_html
        return old_html

    ### HTML formatting
    result_html = ''
    result_html = addContent(result_html, header(
        f"""Hi {account}.<br />
            Your AWS machine has been set up.<br />
            Please log in with the following credentials:""",
        color='darkred'))
    result_html = addContent(result_html,
                           box(f"IP address: {ip}"))
    result_html = addContent(result_html,
                             box(f"""R Studio Server ID: rstudio<br />
                                     R Studio Server Password: {pwd}"""))

    return f'<div>{result_html}</div>'

### home page
@app.route("/", methods=['GET', 'POST'])
def home():
    ### show homepage
    form1 = SignInForm(request.form)

    ### if all the required fields are filled out
    if form1.validate_on_submit():
        ### Extract information
        account = request.form["account"]
        pwd = request.form["pwd"]
        machine = request.form["machine"]
        disk_size = request.form["disk_size"]
        time = request.form["time"]

        ### get cursor of the DB
        cursor = mysql.connect().cursor()
        db = Db(cursor=cursor)

        ### if user id and password are correct
        code = db.user_athentication(account=account, pwd=pwd)
        if code == 1:
            aws = Ac(account=account)

            ### create new instance
            result = aws.create_new_instance(region_name=Conf.AWS_REGION_NAME,
                                             image_id=Conf.AWS_IMAGE_ID,
                                             machine=machine,
                                             sg_id=Conf.AWS_SECURITY_GROUP_ID,
                                             disk_size=disk_size,
                                             key_name=Conf.AWS_KEY_NAME)

            return render_template('result.html', input=make_result(account=account, ip=result[0], pwd=result[1]))
        elif code == 2:
            flash("Your email is not verified. Please check your email.")
            return redirect(url_for('home'))
        else:
            flash("Your sign-in info is not right.")
            return redirect(url_for('home'))
    else:
        return render_template('sign_in.html', form=form1)

### Run the app
if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=80, debug=Conf.DEBUG)
    app.run(host="127.0.0.1", port=5000, debug=Conf.DEBUG)
