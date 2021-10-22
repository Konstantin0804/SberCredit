from api import api, app, docs, db
from config import Config
from api.resources.credit import CreditResource

docs.register(CreditResource) # Регистрируеми в docs ресурс для проверки через Swagger

@app.before_first_request # Создание БД когда запускаем через gunicorn
def setup():
     db.create_all()

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
