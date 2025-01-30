# Kanjiku Backend

This is a Backend service using `Sanic` and `tortoise-orm`

## Installation

This project requires `pipenv`.
On Ubuntu or Debian you can install it by the following command

``` bash
sudo apt-get install pipenv
```
or via pip

``` bash
python3 -m pip install pipenv
alias pipenv="python3 -m pipenv"
```

For the next step we want to clone the repository and change into it's directory

``` bash
git clone https://github.com/Kanjiku/kanjiku-backend.git
cd kanjiku_backend
# if you have python 3.13
pipenv install
# or if you don't have python 3.13 installed use the following command to use your currently installed python3
pipenv install --python python3
```
## Dev Stuff

if you want to do the example requests via the provided python files you should also install the dev dependencies
(or install `requests` any other way you find ok).

Here is the command to install the dev dependencies into the pipenv

```bash
pipenv install -d
```

## Running it

Assuming we have cloned the Repository we can run it by issuing the following command

``` bash
pipenv run python3 -m kanjiku_api
```

If we installed it as a service we can also start it using `systemd` by issuing the following command
``` bash
sudo systemctl start kanjiku_backend
```
## Tokens
This API uses a OAUTH inspired auth system. Basically it uses 2 kinds of JWT tokens.

The `IdentityToken` gives informations about a User and his groups. This token is required for all Endpoints requiring auth.
The following json is an example of the JWT body:
```json
{
  "iss": "kanjiku_backend",
  "iat": 1738013008.445015,
  "nbf": 1738013008.445018,
  "exp": 1738016608.443126,
  "user": {
    "uid": "6a0bbf41-c0f2-4364-b1fa-d5aedea9901c",
    "username": "test-user",
    "groups": [],
    "permissions": {
      "admin": false,
      "early_access": false,
      "manage_projects": false,
      "upload_chapters": false,
      "moderate_avatars": false,
      "view_hidden": false
    }
  }
}
```

The `RefreshToken` is used to refresh an `IdentityToken` and has a longer lifetime compared to the `IdentityToken`. The `RefreshToken` body looks as follows:
```json
{
  "iss": "kanjiku_backend",
  "iat": 1738013008.445839,
  "nbf": 1738013008.445841,
  "exp": 1738099408.445116,
  "id_token": "f0facebb-0608-43af-b3b6-16e70265dbc7"
}
```

A `User` can have multiple `IdentityToken` s and each `IdentityToken` has exactly 1 `RefreshToken`. At logout a user can select the option to sign out all devices. On a password change this happens automatically.

## Changelog

### 0.0.1
* Started working on basic routes
* added data models