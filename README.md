# Развертывание на локальной машине
1. Создаем виртуальное окружение: python3 -m venv flask_venv
2. Активируем venv: source flask_venv/bin/activate
3. Устанавливаем зависимости: pip install -r requirements.txt
4. Локальная БД создается автоматически
5. Запускаем приложение python app.py
6. Документация прописана в Swagger по адресу http://127.0.0.1:5000/swagger-ui/
7. Запуск Unittest'ов доступен как из среды разработки, так и с командной строки командой python -m unittest
8. Запуск pytest доступен по команде pytest -rpP tests/test.py
9. Добавлен Procfile и возможность запуска с gunicorn командой gunicorn app:app. Можно далее переходить в браузере по адресу http://127.0.0.1:8000/credit 

# Миграции
1. Активировать миграции: flask db init
1. Создать миграцию: flask db migrate -m "comment"
1. Применить миграции: flask db upgrade