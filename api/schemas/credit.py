from api import ma
from api.models.credit import CreditModel

class CreditSchema(ma.SQLAlchemySchema): # Схема для сериализации данных для ответа (GET и DEL запросы)
   class Meta:
       model = CreditModel

   date = ma.auto_field()
   amount_with_rate = ma.auto_field()

credit_schema = CreditSchema()
credits_schema = CreditSchema(many=True)

class CreditCreateSchema(ma.SQLAlchemySchema): # Схема для де-сериализации данных
   class Meta:
       model = CreditModel

   date = ma.auto_field()
   periods = ma.auto_field()
   amount = ma.auto_field()
   rate = ma.auto_field()