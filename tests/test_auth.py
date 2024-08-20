import io

from faker import Faker
from fastapi.testclient import TestClient
from main import app
from PIL import Image

client = TestClient(app)

fake = Faker()


def test_user_register(override_get_db):
    email = fake.email()
    response = client.post('/users_app/register', json={
        "email": email,
        "password": fake.password()
        })

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email

def test_user_login(override_get_db, create_user, user_password):
    responce = client.post('/users_app/token', data={
        "username": create_user.email,
        "password": user_password
    })
    assert responce.status_code == 201
    data = responce.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_email_validation(override_get_db, token, create_user):
    responce = client.post(f'/users_app/verify_email?token={token}')
    data = responce.json()
    assert responce.status_code == 200
    assert data['msg'] == "Email verified successfully"


def test_update_avatar(override_get_db, auth_headers, create_user):
    img = Image.new("RGB", (100, 100), color=(73, 109, 137))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    response = client.patch(
        "/users_app/avatar", headers=auth_headers,
        files={"file": ("test.jpg", img_byte_arr, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
