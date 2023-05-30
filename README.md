# Social Media API

API service for Social Media management

## Installation

Python3 must be already installed

```shell
git clone https://github.com/U-Ra-All/social_media_api
cd social_media_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver # starts Django Server
```

Create a file called .env in the same folder as the settings file.
Make sure to have the following development-specific values in there.
You can find the example in [.env_sample](.env_sample)

```shell
SECRET_KEY = "Your_Super_Secret_Key"
```

## Getting access

- create user via /api/user/register/
- create user profile via /api/profiles/create
- get access token via /api/user/token/

## Features

* JWT authenticated
* Admin panel /admin/
* Documentation is located at /api/doc/swagger/
* Managing user profiles, posts comments and likes

# social_media_api
