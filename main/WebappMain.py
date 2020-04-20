from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from main.config import ProductionConfig as CONF
from main.SignInForm import SignInForm
from main.SignUpForm import SignUpForm

### Create a Flask app
app = Flask(__name__,
            instance_relative_config=False,
            template_folder="templates",
            static_folder="static")
app.config.from_object('config.ProductionConfig')
csrf = CSRFProtect(app)
csrf.init_app(app)


@app.route("/success")
def success(name):
    return "Hi %s. Your AWS machine has started." % name

@app.route("/sign-up")
def signup():
    ### show sign up page
    form = SignUpForm(request.form)

    if form.validate_on_submit():
        ### Extract information
        account = request.form["account"]
        pwd = request.form["pwd1"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["pNum"]

        flash("You were successfully signed up")
        return redirect(url_for("success", name=account))
    else:
        return render_template('sign_up.html', form=form)

@app.route("/", methods=['GET', 'POST'])
def home():
    ### show homepage
    form = SignInForm(request.form)
    flash("hi Welcome!")
    if form.validate_on_submit():
        ### Extract information
        account = request.form["account"]
        pwd = request.form["pwd"]
        machine = request.form["machine"]
        disk_size = request.form["disk_size"]
        time = request.form["time"]

        return redirect(url_for("success", name=account))
    else:
        return render_template('sign_in.html', form=form)


if __name__ == '__main__':
    ### Run the app
    app.run(debug=CONF.DEBUG)
