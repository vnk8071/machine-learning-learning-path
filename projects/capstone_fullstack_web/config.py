from settings import DB_NAME, DB_USER, DB_PASSWORD

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
    DB_USER,
    DB_PASSWORD,
    'localhost:5432',
    DB_NAME
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
