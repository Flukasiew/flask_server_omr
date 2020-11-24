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


# @crontab.job(minute="1")
# def cleanup(cycle=0):

#     deleted_files_count = 0

#     data_dir = "/home/fef/code/flask_server_omr/app/data"

#     seconds = time() - (60 * cycle)

#     if path.exists(data_dir):
#         for entry in scandir(data_dir):
#             if seconds >= stat(entry).st_ctime and entry.is_file():
#                 remove(entry)
#                 if not path.exists(entry.path):
#                     deleted_files_count += 1

#     return deleted_files_count


# @app.cli.command()
# def cleanup_XD(cycle=0):

#     deleted_files_count = 0

#     data_dir = "/home/fef/code/flask_server_omr/app"

#     seconds = time() - (60 * cycle)

#     if path.exists(data_dir):
#         for entry in scandir(data_dir):
#             if seconds >= stat(entry).st_ctime and entry.is_file():
#                 remove(entry)
#                 if not path.exists(entry.path):
#                     deleted_files_count += 1

#     return deleted_files_count


from app import file_cleanup
from app import views
