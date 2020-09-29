from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

import logging
import os
from logging.handlers import SMTPHandler

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)

def getCreds():

    # Get creds required for use in the applications
    # Returns: dictonary: credentials needed globally

    creds = dict()

    creds['graph_domain'] = 'https://graph.facebook.com/'
    creds['graph_version'] = 'v6.0'
    creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/' 
    creds['debug'] = 'no'

    creds['access_token'] = os.getenv('memanalytics_access_token')
    creds['client_id'] = os.getenv('memanalytics_client_id')
    creds['client_secret'] = os.getenv('memanalytics_client_secret')
    creds['page_id'] = os.getenv('memanalytics_page_id')
    creds['instagram_account_id'] = os.getenv('memanalytics_ig_id')
    creds['ig_username'] = os.getenv('memanalytics_ig_username')

    return creds

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

from app import routes, models