from api import ma
from api.models.credit import CreditModel
from flask import abort
import datetime
from marshmallow import Schema, fields, pre_load, ValidationError
from flask_restful import abort

class CreditSchema(ma.SQLAlchemySchema): # Схема для сериализации данных для ответа (GET и DEL запросы)
   class Meta:
       model = CreditModel

   date = ma.auto_field()
   amount_with_rate = ma.auto_field()

credit_schema = CreditSchema()
credits_schema = CreditSchema(many=True)

class CreditCreateSchema(ma.SQLAlchemySchema): # Схема для де-сериализации данных

   @pre_load
   def validating(self, in_data, **kwargs): # Проверка данных о введенной дате
      check_date = in_data["date"]
      try:
         datetime.datetime.strptime(check_date, '%d.%m.%Y')
         return in_data
      except:
         abort(400, error="Incorrect date format")

   class Meta:
      model = CreditModel

   date = ma.Date('%d.%m.%Y', example="15.03.2020")
   periods = ma.auto_field()
   amount = ma.auto_field()
   rate = ma.auto_field()


