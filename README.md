# Развертывание на локальной машине
1. Создаем виртуальное окружение: python3 -m venv flask_venv
2. Активируем venv: source flask_venv/bin/activate
3. Устанавливаем зависимости: pip install -r requirements.txt
4. Создаем локальную БД: 
5. flask db init
6. flask db migrate -m "comment"
7. flask db upgrade
8. Запускаем приложение python app.py
9. Документация прописана в Swagger по адресу http://127.0.0.1:5000/swagger-ui/

# Миграции
1. Активировать миграции: flask db init
1. Создать миграцию: flask db migrate -m "comment"
1. Применить миграции: flask db upgrade