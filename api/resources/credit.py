from api import api, db
from monthdelta import monthdelta
from api.models.credit import CreditModel
from api.schemas.credit import CreditSchema, CreditCreateSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from flask_restful import abort
from math import ceil

@api.resource('/credit')
@doc(tags=['Deposits'])
class CreditResource(MethodResource):
    @doc(description='Get all deposits', summary="Get deposits")
    @marshal_with(CreditSchema(many=True))
    def get(self):
        credits = CreditModel.query.all() # Просмотр истории запросов на расчеты
        return credits, 200

    @doc(description="Post new deposits", summary="Post deposits")
    @use_kwargs(CreditCreateSchema)
    def post(self, **kwargs):
        credit = CreditModel(**kwargs) # Объект класса CreditModel на основе введенных данных
        if credit.periods > 60 or credit.periods < 1 or credit.rate > 8 or credit.rate < 1 or credit.amount < 10000 or credit.amount > 3000000:
            abort(400, error="Incorrect data") # Проверка валидности введенных данных
        credit.amount_calc() # Подсчет суммы с учетом % ставки и запись в соответствующую ячейку
        credit.save() # Запись в БД историю запросов по расчетам вкладов
        amount = str(ceil(credit.amount_with_rate*100)/100) # Записываем в переменную значение посчитанной суммы
        date = str(credit.date.strftime('%d/%m/%Y')) # Записываем дату депозита и переводим в строчный формат
        credits = {}
        credits[date] = amount
        i = 1
        while i < credit.periods: # Далее расчет сумм по следующим месяцам и запись в словарь для последующего возрата ответа
            amount = float(amount)*(1+(credit.rate/12)/100)
            amount = str(ceil(amount*100)/100) # Округление до 2х знаков после запятой, как в примере excel
            date = credit.date + monthdelta(+i)
            date = str(date.strftime('%d/%m/%Y'))
            credits[date] = amount
            i += 1
        return credits, 200

    @doc(description='Delete all deposits data', summary="Delete deposits")
    @marshal_with(CreditSchema(many=True))
    def delete(self):
        credits = CreditModel.query.all()
        db.session.query(CreditModel).delete()
        db.session.commit()
        return credits, 200