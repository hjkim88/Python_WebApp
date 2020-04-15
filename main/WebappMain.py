from flask import Flask, request, render_template, redirect, url_for
from wtforms import Form, StringField, validators, SubmitField, PasswordField, SelectField
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.csrf import CSRFProtect
from main.config import ProductionConfig as CONF

### Create a Flask app
app = Flask(__name__,
            instance_relative_config=False,
            template_folder="templates",
            static_folder="static")
app.config.from_object('config.ProductionConfig')
csrf = CSRFProtect(app)
csrf.init_app(app)


### make a web form
class SignInForm(FlaskForm):
    ### ID
    account = StringField("AWS ID", validators=[
        validators.InputRequired()
    ])

    ### Password
    pwd = PasswordField("Password", validators=[
        validators.input_required()
    ])

    ### AWS machine selection
    machine_list = [("t3a.medium", "[General Purpose] t3a.medium (2 vCPUs, 2.2 GHz, AMD EPYC 7571, 4 GB memory)"),
                    ("t3a.xlarge", "[General Purpose] t3a.xlarge (4 vCPUs, 2.2 GHz, AMD EPYC 7571, 16 GB memory)"),
                    ("t3a.2xlarge", "[General Purpose] t3a.2xlarge (8 vCPUs, 2.2 GHz, AMD EPYC 7571, 32 GB memory)"),
                    ("m5n.xlarge",
                     "[General Purpose] m5n.xlarge (4 vCPUs, 3.1 GHz, Intel Xeon Platinum 8259, 16 GB memory)"),
                    ("m5n.2xlarge",
                     "[General Purpose] m5n.2xlarge (8 vCPUs, 3.1 GHz, Intel Xeon Platinum 8259, 32 GB memory)"),
                    ("m5n.4xlarge",
                     "[General Purpose] m5n.4xlarge (16 vCPUs, 3.1 GHz, Intel Xeon Platinum 8259, 64 GB memory)"),
                    ("m5n.8xlarge",
                     "[General Purpose] m5n.8xlarge (32 vCPUs, 3.1 GHz, Intel Xeon Platinum 8259, 128 GB memory)"),
                    ("c5.2xlarge",
                     "[Compute Optimized] c5.2xlarge (8 vCPUs, 3.4 GHz, Intel Xeon Platinum 8124M, 16 GB memory)"),
                    ("c5.4xlarge",
                     "[Compute Optimized] c5.4xlarge (16 vCPUs, 3.4 GHz, Intel Xeon Platinum 8124M, 32 GB memory)"),
                    ("c5.9xlarge",
                     "[Compute Optimized] c5.9xlarge (36 vCPUs, 3.4 GHz, Intel Xeon Platinum 8124M, 72 GB memory)"),
                    ("c5.12xlarge",
                     "[Compute Optimized] c5.12xlarge (48 vCPUs, 3.6 GHz, 2nd Gen Intel Xeon Platinum 8275CL, 96 GB memory)"),
                    ("r5a.xlarge", "[Memory Optimized] r5a.xlarge (4 vCPUs, 2.5 GHz, AMD EPYC 7571, 32 GB memory)"),
                    ("r5a.2xlarge", "[Memory Optimized] r5a.2xlarge (8 vCPUs, 2.5 GHz, AMD EPYC 7571, 64 GB memory)"),
                    ("r5a.4xlarge", "[Memory Optimized] r5a.4xlarge (16 vCPUs, 2.5 GHz, AMD EPYC 7571, 128 GB memory)"),
                    ("r5a.8xlarge", "[Memory Optimized] r5a.8xlarge (32 vCPUs, 2.5 GHz, AMD EPYC 7571, 256 GB memory)")]
    machine = SelectField("AWS Machine", choices=machine_list, default=1)

    ### Disk size selection
    disk_size_list = [("gb20", "20GB"),
                      ("gb30", "30GB"),
                      ("gb50", "50GB"),
                      ("gb100", "100GB"),
                      ("gb200", "200GB"),
                      ("gb300", "300GB"),
                      ("gb500", "500GB"),
                      ("tb1", "1TB"),
                      ("tb2", "2TB"),
                      ("tb3", "3TB"),
                      ("tb5", "5TB")]
    disk_size = SelectField("Disk Size", choices=disk_size_list, default=1)

    ### Time selection
    time_list = [("hrs2", "2 Hours"),
                 ("hrs3", "3 Hours"),
                 ("hrs5", "5 Hours"),
                 ("hrs8", "8 Hours"),
                 ("hrs12", "12 Hours"),
                 ("hrs24", "24 Hours"),
                 ("hrs36", "36 Hours"),
                 ("hrs48", "48 Hours"),
                 ("hrs72", "72 Hours"),
                 ("hrs120", "120 Hours"),
                 ("hrs168", "168 Hours"),
                 ("hrs336", "336 Hours")]
    time = SelectField("Running Time", choices=time_list, default=1)

    ### Recaptcha
    recaptcha = RecaptchaField()

    ### Submit button
    submit = SubmitField("Submit")


@app.route("/success/<name>/")
def success(name):
    return "Hi %s. Your AWS machine has started." % name


@app.route("/", methods=['GET', 'POST'])
def home():
    ### Create homepage
    form = SignInForm(request.form)

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
