# weather_data_capture

# Local dev setup

```
## setup a venv inside this project
python -m venv .
## enter your venv
source bin/activate
## install the dependencies
python -m pip install -r requirements.txt
## do the db migrations
python manage.py migrate
```

# Local server start

```shell
## run django server
python manage.py runserver
```

Do your first data collection

```shell
curl 127.0.0.1:8000/get_data/ -s -o /dev/null
curl 127.0.0.1:8000/create_demo_sources/ -s -o /dev/null
```

Then open your browser in [localhost:8000](http://127.0.0.1:8000)

# Local test runner

```shell
python manage.py test
```
