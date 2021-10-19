import os
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

base_dir = os.path.dirname(os.path.abspath(__file__))
ma_plugin = MarshmallowPlugin()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir, 'base.db')
    TEST_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True #Включаем режим логирования
    DEBUG = True
    PORT = 5000
    RESTFUL_JSON = {
        'ensure_ascii': False
    }
    APISPEC_SPEC = APISpec(
        title='Notes Project',
        version='v1',
        plugins=[ma_plugin],
        security=[],
        openapi_version='2.0.0'
    )
    APISPEC_SWAGGER_URL = '/swagger'  # URI API Doc JSON
    APISPEC_SWAGGER_UI_URL = '/swagger-ui/'  # URI UI of API Doc