# api_final
api final
### Как запустить проект:

Описание:

```
Финальное задание 10 спринта
```

Установка:

```
git clone https://github.com/RavusiNbO/api_final_yatube
python3 -m venv env
. venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

Примеры:

POST http://127.0.0.1:8000/api/v1/jwt/create/ - получение токена
```
{
    "username" : "rava",
    "password" : "1"
}
```

GET http://127.0.0.1:8000/api/v1/posts/ - получение списка постов
