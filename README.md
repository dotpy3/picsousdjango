# Picsous

## Installation

1. Create a `picsous/local_settings.py` to configure your own local settings (DATABASES settings, Ginger key, Payutc key)
2. (Recommended) Create a virtual python environment with `virtualenv env` then `source env/bin/activate`. If virtualenv isn't installed yet, install it with `sudo pip install virtualenv`.
3. Install requirements with `pip install -r requirements.txt`.
4. Launch migrations with `python manage.py migrate`.
5. Run server with `python manage.py runserver 0.0.0.0:8090` (for port 8090).

## Launch interactive shell

To launch the Django interactive shell to interact with the database, type `python manage.py shell_plus`.
