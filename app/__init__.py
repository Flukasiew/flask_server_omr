from flask import Flask
from flask_crontab import Crontab
from os import remove, stat, path, scandir
from time import time


app = Flask(__name__)
crontab = Crontab(app)


if app.config["ENV"] == "production":

    app.config.from_object("config.ProductionConfig")

elif app.config["ENV"] == "development":

    app.config.from_object("config.DevelopmentConfig")

else:

    app.config.from_object("config.ProductionConfig")


from app import file_cleanup
from app import views
