from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from evrnmt.config import DevelopmentConfig as Conf
from forms.SignInForm import SignInForm
from forms.SignUpForm import SignUpForm
from flaskext.mysql import MySQL
from main.DBControl import DBControl as Db
from main.AWSControl import AWSControl as Ac
from flask_mail import Mail, Message

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

### email
@app.route("/send-email")
def send_email():
    msg = Message("Send Mail Tutorial!",
      sender=app.config.get("MAIL_USERNAME"),
      recipients=["firadazer@gmail.com"],
      body="This is a test email I sent with Gmail and Python!")
    mail.send(msg)
    return 'Mail sent!'

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
            flash("User created successfully!", "success")
        else:
            flash("Enter the required fields", "warning")

        return redirect(url_for("/"))
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
        if db.user_athentication(account=account, pwd=pwd):
            aws = Ac(account=account)

            ### create new instance
            result = aws.create_new_instance(region_name=Conf.AWS_REGION_NAME,
                                             image_id=Conf.AWS_IMAGE_ID,
                                             machine=machine,
                                             sg_id=Conf.AWS_SECURITY_GROUP_ID,
                                             disk_size=disk_size,
                                             key_name=Conf.AWS_KEY_NAME)

            return render_template('result.html', input=make_result(account=account, ip=result[0], pwd=result[1]))

        else:
            return "Enter the right information."
    else:
        return render_template('sign_in.html', form=form1)

### Run the app
if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=80, debug=Conf.DEBUG)
    app.run(host="127.0.0.1", port=5000, debug=Conf.DEBUG)
