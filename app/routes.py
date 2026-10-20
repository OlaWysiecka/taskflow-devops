
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from .extensions import db
from .models import Task

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    tasks = db.session.execute(
        db.select(Task).order_by(Task.created_at.desc())
    ).scalars().all()

    return render_template("index.html", tasks=tasks)


@bp.post("/tasks")
def create_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        flash("Task title is required.", "error")
        return redirect(url_for("main.index"))

    if len(title) > 200:
        flash("Task title cannot exceed 200 characters.", "error")
        return redirect(url_for("main.index"))

    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()

    flash("Task created successfully.", "success")
    return redirect(url_for("main.index"))


@bp.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()

        if not title or len(title) > 200:
            flash("Enter a title containing 1–200 characters.", "error")
            return render_template("edit.html", task=task), 400

        task.title = title
        task.description = description
        db.session.commit()

        flash("Task updated successfully.", "success")
        return redirect(url_for("main.index"))

    return render_template("edit.html", task=task)


@bp.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    task = db.get_or_404(Task, task_id)
    task.completed = not task.completed
    db.session.commit()

    return redirect(url_for("main.index"))


@bp.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully.", "success")
    return redirect(url_for("main.index"))


@bp.get("/health")
def health():
    return jsonify(status="ok"), 200
