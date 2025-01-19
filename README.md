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
pipenv install .
# or if you don't have python 3.13 installed use the following command to use your currently installed python3
pipenv install . --python python3
```

## Running it

Assuming we have cloned the Repository we can run it by issuing the following command

``` bash
pipenv run python3 -m kanjiku_api
```

If we instaled it as a service we can also start it using `systemd` by issuing the following command
``` bash
sudo systemctl start kanjiku_backend
```

## Changelog

### 0.0.1
* Started working on basic routes
* added data models