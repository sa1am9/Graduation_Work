from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
import os
from config import Config
from flask_script import Manager


project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates/')

db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=True, template_folder=template_path)
app.config.from_object(Config)
app.config.from_object("config")
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
ma = Marshmallow(app)
from models.models import *

from models.empl import emp
from main import main
from models.dep import dep
from api.views import api

app.register_blueprint(main)
app.register_blueprint(emp)
app.register_blueprint(dep)
app.register_blueprint(api)
