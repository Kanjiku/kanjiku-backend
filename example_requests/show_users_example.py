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
print("#### Show 'all' Users (page 1 pagesize 25 by default)")
resp = requests.get("http://localhost:9999/v1/User")
resp_json = resp.json()
print(json.dumps(resp_json, indent=4))

print("#### Pagination example")
print("Page 1 pagesize 2")
resp = requests.get("http://localhost:9999/v1/User?page=1&pagesize=2")
resp_json = resp.json()
# small var for the user id of the first user we need later on
first_user = list(resp_json["users"].keys())[0]
print(json.dumps(resp_json, indent=4))

print("Page 2 pagesize 2")
resp = requests.get("http://localhost:9999/v1/User?page=2&pagesize=2")
resp_json = resp.json()
print(json.dumps(resp_json, indent=4))

print("Page 99999 pagesize 2")
resp = requests.get("http://localhost:9999/v1/User?page=99999&pagesize=2")
resp_json = resp.json()
print(json.dumps(resp_json, indent=4))


print(f"\n#### show user with id {first_user}")
resp = requests.get(f"http://localhost:9999/v1/User/{first_user}")
resp_json = resp.json()
print(json.dumps(resp_json, indent=4))