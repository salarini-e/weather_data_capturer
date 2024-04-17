# weather_data_capture

# Developing locally

First before start your app

```shell
## setup a venv inside this project
python -m venv .
## enter your venv
source bin/activate
## install the dependencies
python -m pip install -r requirements.txt
## do the db migrations
python manage.py migrate
```

Then start your app

```shell
## run django server
python manage.py runserver
```

Do your first data collection

```shell
curl 127.0.0.1:8000/get_data/ -s -o /dev/null
```

Then open your browser in [localhost:8000](http://127.0.0.1:8000)
