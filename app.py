import dotenv
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Load the .env file
dotenv.load_dotenv()

# Get the secret key from the .env file
app.secret_key = dotenv.get_key(".env", "SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  


db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, nullable=False, default=0)  # Added default value
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'

# Initialize the database inside the application context
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!", "success")  # Flash success message
            return redirect("/")
        except:
            flash("There was an issue adding your task.", "error")  # Flash error message
            return redirect("/")

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash("Task deleted successfully!", "success")  # Flash success message
        return redirect("/")
    except:
        flash("Error deleting task", "error")  # Flash error message
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
