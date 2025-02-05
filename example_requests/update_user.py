import requests
import json

session = requests.Session()
### registering a test user
resp = session.post(
    "http://localhost:9999/v1/User/register",
    json={
        "username": "test-user",
        "password": "super secret",
        "email": "test@example.com",
        "birthday": "1997-07-13",
    },
)

### login
resp = session.post(
    "http://localhost:9999/v1/Session/login",
    json={
        "username": "test-user",
        "password": "super secret",
    },
)

resp = session.get("http://localhost:9999/v1/User/me")

print(json.dumps(resp.json(), indent=4))

### Update Email
resp = session.patch(
    "http://localhost:9999/v1/User/me", json={"email": "test2@example.com"}
)

### login again
resp = session.post(
    "http://localhost:9999/v1/Session/login",
    json={
        "username": "test-user",
        "password": "super secret",
    },
)

print("\n### Updated Email")
resp = session.get("http://localhost:9999/v1/User/me")
print(json.dumps(resp.json(), indent=4))

### update birthday
resp = session.patch(
    "http://localhost:9999/v1/User/me", json={"birthday": "1999-03-25"}
)

### login again
resp = session.post(
    "http://localhost:9999/v1/Session/login",
    json={
        "username": "test-user",
        "password": "super secret",
    },
)

print("\n### Updated birthday")
resp = session.get("http://localhost:9999/v1/User/me")
print(json.dumps(resp.json(), indent=4))

### update password
resp = session.patch(
    "http://localhost:9999/v1/User/me", json={"password": "new secret", "old_password":"super secret"}
)

### login again
resp = session.post(
    "http://localhost:9999/v1/Session/login",
    json={
        "username": "test-user",
        "password": "new secret",
    },
)

print("\n### Updated password")
resp = session.get("http://localhost:9999/v1/User/me")
print(json.dumps(resp.json(), indent=4))
