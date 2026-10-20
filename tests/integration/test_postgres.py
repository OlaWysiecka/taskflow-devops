
from app.extensions import db
from app.models import Task


def test_postgres_connection(postgres_app):
    with postgres_app.app_context():
        result = db.session.execute(db.text("SELECT 1")).scalar_one()

        assert result == 1


def test_create_and_read_task(postgres_client, postgres_app):
    response = postgres_client.post(
        "/tasks",
        data={
            "title": "PostgreSQL integration task",
            "description": "Saved in PostgreSQL",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"PostgreSQL integration task" in response.data

    with postgres_app.app_context():
        task = db.session.execute(
            db.select(Task).where(
                Task.title == "PostgreSQL integration task"
            )
        ).scalar_one()

        assert task.description == "Saved in PostgreSQL"
        assert task.completed is False


def test_edit_task(postgres_client, postgres_app):
    with postgres_app.app_context():
        task = Task(title="Original", description="Original description")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = postgres_client.post(
        f"/tasks/{task_id}/edit",
        data={
            "title": "Updated",
            "description": "Updated description",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with postgres_app.app_context():
        task = db.session.get(Task, task_id)

        assert task.title == "Updated"
        assert task.description == "Updated description"


def test_toggle_task(postgres_client, postgres_app):
    with postgres_app.app_context():
        task = Task(title="Toggle me")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = postgres_client.post(f"/tasks/{task_id}/toggle")

    assert response.status_code == 302

    with postgres_app.app_context():
        task = db.session.get(Task, task_id)
        assert task.completed is True


def test_delete_task(postgres_client, postgres_app):
    with postgres_app.app_context():
        task = Task(title="Delete me")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = postgres_client.post(f"/tasks/{task_id}/delete")

    assert response.status_code == 302

    with postgres_app.app_context():
        assert db.session.get(Task, task_id) is None
