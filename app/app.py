from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from models.empl import emp
from main import main
from models.dep import dep
from api.views import api

app.register_blueprint(main)
app.register_blueprint(emp)
app.register_blueprint(dep)
app.register_blueprint(api)