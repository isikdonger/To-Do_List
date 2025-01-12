import os
from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.simple import SubmitField

app = Flask(__name__)
app.secret_key = os.environ.get("secret_key")
Bootstrap5(app)


class TaskForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired()])
    submit = SubmitField("Submit Task")


def initialize_tasks_from_file():
    """Read tasks from the text file and initialize the tasks."""
    global Tasks  # Ensure we update the global `Tasks` list
    if not os.path.exists("tasks.txt"):  # Create file if it doesn't exist
        Tasks = []
    else:
        with open("tasks.txt", "r") as file:
            Tasks = [line.strip() for line in file.readlines()]


def update_tasks_to_file():
    """Write the current tasks to the text file."""
    global Tasks
    with open("tasks.txt", "w") as file:
        file.write("\n".join(Tasks))


Tasks = []
initialize_tasks_from_file()




@app.route("/")
def home():
    return render_template("index.html", tasks=Tasks)


@app.route("/delete", methods=["POST"])
def delete_task():
    data = request.get_json()
    item = data.get("item")
    if item in Tasks:
        Tasks.remove(item)
        update_tasks_to_file()  # Save changes to the text file
        return redirect(url_for("home"))
    else:
        return jsonify({"error:" "Item not found"}), 400


@app.route("/edit_js", methods=["POST"])
def edit_js():
    data = request.get_json()
    item = data.get("item")  # Get the item from query parameters
    if item in Tasks:
        form = TaskForm()  # Initialize the form
        return render_template("edit_form.html", form=form, item=item)
    else:
        return jsonify({"error": "Item not found"}), 400


@app.route("/edit", methods=["POST"])
def edit_item():
    data = request.get_json()  # Get JSON data from the request
    item = data.get("item")  # Get the item from the request data
    task = data.get("task")

    if item in Tasks:
        index = Tasks.index(item)
        Tasks[index] = task  # Update the task in the list
        update_tasks_to_file()  # Save changes to the text file
        return jsonify({"redirect": url_for("home")})  # Return a redirect to the home page
    else:
        return jsonify({"error": "Item not found"}), 400


@app.route("/add", methods=["GET", "POST"])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = form.task.data
        Tasks.append(task)
        update_tasks_to_file()  # Save changes to the text file
        return redirect(url_for("home"))
    else:
        return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5001)