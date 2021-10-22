import json
from api import db
from app import app
import unittest
from config import Config

class TestCredit(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.update({
            'SQLALCHEMY_DATABASE_URI': Config.TEST_DATABASE_URI
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_deposit_creation(self):
        credit_data = {
            "date": '22.04.2021',
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
        self.assertIn('22.05.2021', data.keys())
        self.assertIn(402671.12, data.values())
        self.assertEqual(len(data), 5)

    def test_deposit_validation(self):
        credit_data = {
            "date": '22.04.2021',
            "periods": 100,
            "amount": 400000,
            "rate": 4
        }
        res = self.client.post('/credit',
                               data=json.dumps(credit_data),
                               content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_delete_data(self):
        credit_data = {
                "date": '22.04.2021',
                "periods": 5,
                "amount": 400000,
                "rate": 4
            }
        self.client.post('/credit',
                               data=json.dumps(credit_data),
                               content_type='application/json')
        res = self.client.delete('/credit')
        self.assertEqual(res.status_code, 200)

    def test_get_data(self):
        credit_data = {
                "date": '22.04.2021',
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

if __name__ == "__main__":
    unittest.main()