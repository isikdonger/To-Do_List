import os
from flask import Flask, render_template, url_for, redirect, make_response
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = os.environ.get("secret_key")
Bootstrap5(app)

Tasks = []

for i in range(25):
    Tasks.append(f"Task {i+1}")


class TaskForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired()])
    submit = SubmitField("Submit Task")


@app.route("/")
def home():
    return render_template("index.html", tasks=Tasks)


@app.route("/add", methods=["GET", "POST"])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = form.task.data
        Tasks.append(task)
        return redirect(url_for("home"))
    else:
        return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
