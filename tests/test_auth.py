import pytest
from client.api import API

USERNAME = "testuser1"
PASSWORD = "jeuf8jfqf2fqj..FNDF"


@pytest.fixture()
def admin():
    api = API.login("admin", "admin")

    api.delete(f"/users/{USERNAME}")

    yield api

    api.delete(f"/users/{USERNAME}")
    api.logout()


def test_user_password(admin):

    response = admin.put(f"/users/{USERNAME}")
    assert response

    response = admin.patch(f"/users/{USERNAME}/password", password=PASSWORD)
    assert response

    usr = API.login(USERNAME, PASSWORD + "wrong")
    assert not usr

    response = usr.get("/users/me")
    assert not response

    usr = API.login(USERNAME, PASSWORD)
    assert usr

    response = usr.get("/users/me")
    assert response
    assert response.data["name"] == USERNAME

    usr.logout()
