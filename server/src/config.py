import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://{}:{}@{}/{}'.format(os.getenv('DB_USER', 'backend'), os.getenv('DB_PASSWORD', 'test'),
                                             os.getenv('DB_HOST', 'mysql'), os.getenv('DB_NAME', 'flask_db'))
    ADMINS = ['admin@example.com']