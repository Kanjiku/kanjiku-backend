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

# get avatar
user_resp = session.get("http://localhost:9999/v1/User/me")
print(user_resp.json()["id"])
avatar_uid = user_resp.json()["avatar"]
print(avatar_uid)

img_resp = session.get(f"http://localhost:9999/v1/Image/{avatar_uid}")
#print(img_resp._content)