import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tu_llave_secreta_muy_segura')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:@localhost/sistema_usuarios'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False