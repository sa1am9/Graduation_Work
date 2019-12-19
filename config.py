"""Settings database for server and tests"""


class ApiConfiguration:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://LiJZRTlglU:joXboKoL07@remotemysql.com:3306/LiJZRTlglU'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfiguration:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://G7PajAyxic:BA2aYVjUJ6@remotemysql.com:3306/G7PajAyxic'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DEBUG = True