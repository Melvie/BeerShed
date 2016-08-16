import os


# default confit
class BaseConfig(object):
      DEBUG=False
      SECRET_KEY='\x84s\xdd\x83I\xe8\x0e<K\xc4u\xb7\xd5u\x9a\xecdF\x86O1\x85\x07q'
      SQLALCHEMY_TRACK_MODIFICATIONS= True
      #SQLALCHEMY_DATABASE_URI = 'sqlite:////media/mrt/HDD/Programs/FlaskLearns/posts.db'
      #production database different form local database
      #database uri needs to import poath and database farm environment and then sent path and name as environment var
      # 
      SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
      print SQLALCHEMY_DATABASE_URI


class TestConfig(BaseConfig):
      DEBUG = True
      TESTING = True
      WTF_CSRF_ENABLED = False
      SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
      DEBUG = True


class ProductionConfig(BaseConfig):
      DEBUG = False
