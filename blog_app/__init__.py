from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

from blog_app import routes, models
app.config.from_object(Config)
db = SQLALchemy(app)
migrate = Migrate(app, db)