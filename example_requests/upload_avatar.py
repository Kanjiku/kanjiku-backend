import requests
import json

session = requests.Session()
### registering a test user
resp = session.post(
    "http://localhost:9999/v1/User/register",
    json={
        "username": "avatar_test",
        "password": "super secret",
        "email": "avatar_test@example.com",
        "birthday": "1997-07-13",
    },
)

### login
print("login")
resp = session.post(
    "http://localhost:9999/v1/Session/login",
    json={
        "username": "avatar_test",
        "password": "super secret",
    },
)

print("uploading avatar")
resp = session.post(
    "http://localhost:9999/v1/User/me/avatar",
    files={"upload_file.png": open("./example_avatar.jpg", "rb")},
)

print(resp.text)