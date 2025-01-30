import requests
import json


resp = requests.post(
    "http://localhost:9999/v1/User/register",
    json={
        "username": "test-user1",
        "password": "super secret",
        "email": "test@example1.com",
        "birthday": "1997-07-13",
    },
)
resp = requests.post(
    "http://localhost:9999/v1/User/register",
    json={
        "username": "test-user2",
        "password": "super secret",
        "email": "test@example2.com",
        "birthday": "1997-07-13",
    },
)
resp = requests.post(
    "http://localhost:9999/v1/User/register",
    json={
        "username": "test-user3",
        "password": "super secret",
        "email": "test@example3.com",
        "birthday": "1997-07-13",
    },
)
print("#### Show all Users")
resp = requests.get("http://localhost:9999/v1/User")

resp_json = resp.json()
print(json.dumps(resp_json, indent=4))

first_user = list(resp_json["users"].keys())[0]
print(f"\n#### show user with id {first_user}")
resp = requests.get(f"http://localhost:9999/v1/User/{first_user}")
print(resp.text)
resp_json = resp.json()
print(json.dumps(resp_json, indent=4))