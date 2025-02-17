import pytest
from app import app
from app import tasks  # Import the tasks list from app.py


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
#to check the working of home page
def test_home_page(client):
    response = client.get("/")
    print(response.data.decode())
    assert response.status_code == 200
    assert b"Enter a new task" in response.data  # Check if tasks list is present in response

#to check the working of add task
def test_add_task(client):
    response = client.post("/add", data={"task": "Test Task"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Task" in response.data  # Verify task appears in response

#to check if any empty input is taken
def test_add_empty_task(client):
    response = client.post("/add", data={"task": ""}, follow_redirects=True)
    assert response.status_code == 200
    assert b"" in response.data  # Empty task should not be added

#to check the deletion of the task
def test_delete_task(client):
    from app import tasks  # Ensure access to tasks
    
    # Reset the task list before testing
    tasks.clear()

    # Ensure the task list is empty before test
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Delete Me" not in response.data  # Ensure no leftovers

    # Add a task
    client.post("/add", data={"task": "Delete Me"}, follow_redirects=True)

    # Verify task is added
    response = client.get("/", follow_redirects=True)
    assert b"Delete Me" in response.data  # Task should be present

    # Delete the first task (index 0)
    response = client.get("/delete/0", follow_redirects=True)

    # Verify task is deleted
    assert response.status_code == 200
    assert b"Delete Me" not in response.data  # Task should be gone



