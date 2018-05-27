import os
import logging

from sqlalchemy.engine.url import URL


class Config(object):
    # controls whether web interfance users are in Flask debug mode
    # (e.g. Werkzeug stack trace console, unminified assets)
    DEBUG = False

    # Encryption key used to sign Flask session cookies
    # Generate a random one using os.urandom(24)
    if os.environ.get('APP_KEY') is not None:
        SECRET_KEY = os.environ.get('APP_KEY')
    else:
        SECRET_KEY = "secret"

    # Loggging
    APP_LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_LOG_LEVEL = logging.WARN
    STDERR_LOG_FORMAT = ('%(asctime)s %(levelname)s %(message)s', '%m/%d/%Y %I:%M:%S %p')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Useful directories
    APP_DIR = os.path.dirname(os.path.abspath(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    STATIC_DIR = os.path.join(APP_DIR, 'static')

    ELASTICSEARCH_URL = "localhost"
    DATABASE_URI_FMT = 'postgresql://{username}:{password}@{hostname}:{port}/{dbname}'
    DB_HOST = '35.200.148.88'
    DB_NAME = 'postgres'
    DB_PASS = 'dev-instance'
    DB_PORT = '5432'
    #DB_SCHEMA = 'skeleton_schema'
    #DB_ADMIN = 'skeleton_dba'
    DB_USER = 'postgres'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI_FMT.format(**
                                                      {'username': DB_USER,
                                                       'password': DB_PASS,
                                                       'hostname': DB_HOST,
                                                       'port': DB_PORT,
                                                       'dbname': DB_NAME,
                                                       #'schema': DB_SCHEMA,
                                                       })


class DevelopmentConfig(Config):
    ENV = 'dev'
    DEBUG = True
    ELASTICSEARCH_URL = "https://h58gvkn3ht:equba7co4t@arp-contactbook-3855353482.ap-southeast-2.bonsaisearch.net"


class ProductionConfig(Config):
    ENV = 'prod'
    # Don't need to see debug messages in production
    APP_LOG_LEVEL = logging.INFO

config_dict = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}

app_config = config_dict[os.getenv('APP_ENV') or 'default']

