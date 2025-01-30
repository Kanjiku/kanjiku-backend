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