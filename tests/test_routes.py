
from app.extensions import db
from app.models import Task


def test_index_returns_success(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"My tasks" in response.data


def test_create_task(client, app):
    response = client.post(
        "/tasks",
        data={
            "title": "Test task",
            "description": "Task description",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Test task" in response.data

    with app.app_context():
        task = db.session.execute(
            db.select(Task).where(Task.title == "Test task")
        ).scalar_one()

        assert task.description == "Task description"
        assert task.completed is False


def test_create_task_requires_title(client):
    response = client.post(
        "/tasks",
        data={"title": "", "description": "No title"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Task title is required." in response.data


def test_edit_task(client, app):
    with app.app_context():
        task = Task(title="Old title", description="Old description")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.post(
        f"/tasks/{task_id}/edit",
        data={
            "title": "Updated title",
            "description": "Updated description",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Updated title" in response.data

    with app.app_context():
        task = db.session.get(Task, task_id)
        assert task.title == "Updated title"
        assert task.description == "Updated description"


def test_toggle_task(client, app):
    with app.app_context():
        task = Task(title="Task to complete")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    client.post(f"/tasks/{task_id}/toggle")

    with app.app_context():
        task = db.session.get(Task, task_id)
        assert task.completed is True


def test_delete_task(client, app):
    with app.app_context():
        task = Task(title="Task to delete")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.post(
        f"/tasks/{task_id}/delete",
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():
        assert db.session.get(Task, task_id) is None
