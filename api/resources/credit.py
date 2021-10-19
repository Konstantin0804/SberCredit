from api import api, db
import datetime
from monthdelta import monthdelta
from api.models.credit import CreditModel
from api.schemas.credit import CreditSchema, CreditCreateSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from flask_restful import abort

@api.resource('/credit')
@doc(tags=['Credits'])
class CreditResource(MethodResource):
    @doc(description='Get all credits', summary="Get credits")
    @marshal_with(CreditSchema(many=True))
    def get(self):
        credits = CreditModel.query.all() # Просмотр истории запросов на расчеты
        return credits, 200

    @doc(description="Post new credit", summary="Post credit")
    @use_kwargs(CreditCreateSchema)
    def post(self, **kwargs):
        credit = CreditModel(**kwargs) # Объект класса CreditModel на основе введенных данных
        if credit.periods > 60 or credit.rate > 8 or credit.amount < 10000 or credit.amount > 3000000:
            abort(400, error="Incorrect data") # Проверка валидности введенных данных
        credit.amount_calc() # Подсчет суммы с учетом % ставки
        credit.save() # Запись в БД историю запросов по расчетам кредитов
        i = 1
        amount = credit.amount_with_rate # Записываем в переменную значение посчитанной суммы
        credits = {}
        while i <= credit.periods: # Далее расчет сумм по следующим месяцам и записаь их в словарь для последующего возрата ответа
            amount = int(amount)*(1+(credit.rate/12)/100)
            amount = int(round(amount / 50) * 50)
            amount = str(amount)
            date = credit.date
            date += monthdelta(+i)
            date = str(date.strftime('%m/%d/%Y'))
            credits[date] = amount
            i += 1
        return credits, 200

    @marshal_with(CreditSchema(many=True))
    @doc(description='Delete credit data', summary="Delete credits")
    def delete(self):
        credits = CreditModel.query.all()
        db.session.query(CreditModel).delete()
        db.session.commit()
        return credits, 200