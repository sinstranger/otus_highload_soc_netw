Tested on python 3.10

Based on Django. All unused Django's features are turned off.

Postman collection is in root proj dir:
`socialnet.postman_collection.json`

Set up project:
```
python3 -m venv venv
source venv/bin/activate
pip install requirements.txt
```

Run db:
```
docker compose up -d
```

Run project:
```
./start.sh
```

# Homework 2

add users to db
```
cd src && python manage.py shell < scripts/load_users_from_scv.py
```

