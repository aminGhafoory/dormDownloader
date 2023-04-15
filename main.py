from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import subprocess

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


import configparser

config = configparser.ConfigParser()
config.read("config.ini")

path = config["IDM"]["path"]


config["IDM"]


app = Flask(__name__)
import secrets

secret_key = secrets.token_urlsafe(16)
app.secret_key = secret_key

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)


class Linkform(FlaskForm):
    link = StringField(
        "Enter your links Here", validators=[DataRequired()], widget=TextArea()
    )
    submit = SubmitField("Submit")


def validate_url(url) -> bool:
    return True


def add_to_main_download_queue(url, path):
    subprocess.run(
        [
            rf"{path}",
            "/a",
            "/d",
            url,
        ]
    )


@app.route("/", methods=["GET", "POST"])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = Linkform()
    if form.validate_on_submit():
        links = form.link.data.split("\n")

        for link in links:
            print(link)
            if validate_url(link):
                add_to_main_download_queue(link, path=path)

        return render_template(
            "index.html",
            form=form,
            message=str(len(links)) + " Links added to main download queue.",
        )
    return render_template("index.html", form=form, message="")


if __name__ == "__main__":
    app.run(debug=True)
