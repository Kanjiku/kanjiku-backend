import requests

session = requests.Session()
print("\n##### Register")
resp = session.post(
    "http://localhost:9999/v1/User/register",
    json={
        "username": "test-user",
        "password": "super secret",
        "email": "test@example.com",
        "birthday": "1997-07-13",
    },
)
print(resp.text)

#### Login
print("\n##### Login")
resp = session.post(
    "http://localhost:9999/v1/Session/login",
    json={
        "username": "test-user",
        "password": "super secret",
    },
)

print(resp.text)
print(resp.cookies.get_dict())

print("\n##### Session Info")
resp = session.get("http://localhost:9999/v1/Session")

print(resp.text)

print("\n##### Refresh Session")
resp = session.get("http://localhost:9999/v1/Session/refresh")
print(resp.text)
print(resp.cookies.get_dict())

print("\n##### Session Info")
resp = session.get("http://localhost:9999/v1/Session")

print(resp.text)
