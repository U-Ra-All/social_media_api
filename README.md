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

To test posting with delay feature you should run Celery worker server

```shell
celery -A social_media_api worker -l INFO
```

The project doesn't have media files(post and profile images). To test this feature add your own

Create a file called .env in the same folder as the settings file.
Make sure to have the following development-specific values in there.
You can find the example in [.env_sample](.env_sample)

```shell
SECRET_KEY = "Your_Super_Secret_Key"
```

## To get access to admin panel go to
- /admin

You can use the following superuser (or create another one by yourself):

```shell
Login: admin_user@mail.com
Password: 7QancRe2
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
