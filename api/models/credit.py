from api import db
from monthdelta import monthdelta
import datetime

class CreditModel(db.Model):
    __tablename__ = 'credit_model'
    date = db.Column(db.Date(), unique=False, nullable=False, primary_key=True)
    periods = db.Column(db.Integer, unique=False, nullable=False)
    amount = db.Column(db.Integer, unique=False, nullable=False)
    rate = db.Column(db.Float(10), unique=False, nullable=False)
    amount_with_rate = db.Column(db.Float, unique=False)

    def amount_calc(self):
        self.amount_with_rate = self.amount*(1+(self.rate/12)/100) # Формула подсчета суммы с учетом % ставки
        self.amount_with_rate = int(round(self.amount_with_rate/50)*50) # Округление до 50 рублей
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"[{self.date}: {self.amount}]"