from api import api, app, docs
from config import Config
from api.resources.credit import CreditResource

docs.register(CreditResource) # Регистрируеми в docs ресурс для проверки через Swagger

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
