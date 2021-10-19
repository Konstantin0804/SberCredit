import json
from api import db
from app import app
from unittest import TestCase
from config import Config

class TestCredit(TestCase):
    def setUp(self):
        self.app = app
        self.app.config.update({
            'SQLALCHEMY_DATABASE_URI': Config.TEST_DATABASE_URI
        })

        self.client = self.app.test_client()

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_credit_creation(self): # Тестирование создания кредитной заявки и вывода результата
        credit_data = {
            "date": '2021-04-22',
            "periods": 5,
            "amount": 400000,
            "rate": 4
        }
        res = self.client.post('/credit',
                               data=json.dumps(credit_data),
                               content_type='application/json')
        data = json.loads(res.data)
        print("data = ", data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('05/22/2021', data.keys())
        self.assertIn('402700', data.values())
        self.assertEqual(len(data), 5)

    def test_credit_validation(self): # Тестирование не корректного ввода данных (слишком длинный период)
        credit_data = {
            "date": '2021-04-22',
            "periods": 100,
            "amount": 400000,
            "rate": 4
        }
        res = self.client.post('/credit',
                               data=json.dumps(credit_data),
                               content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_delete_data(self): # Тестирование удаления данных из БД
        credit_data = {
                "date": '2021-04-22',
                "periods": 5,
                "amount": 400000,
                "rate": 4
            }
        self.client.post('/credit',
                               data=json.dumps(credit_data),
                               content_type='application/json')
        res = self.client.delete('/credit')
        self.assertEqual(res.status_code, 200)

    def test_get_data(self): # Тестирование запроса на получение данных ранее созданной заявки на расчет
        credit_data = {
                "date": '2021-04-22',
                "periods": 5,
                "amount": 400000,
                "rate": 4
            }
        self.client.post('/credit',
                               data=json.dumps(credit_data),
                               content_type='application/json')
        res = self.client.get('/credit')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data), 1)

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()