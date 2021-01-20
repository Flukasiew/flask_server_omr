from pathlib import Path
from os import remove, stat, path, scandir
from time import time

from app import crontab


@crontab.job(minute="10")
def cleanup(cycle=10):
    """
    Deletes entreis in static directory to get rid of useless files
    """

    deleted_files_count = 0
    data_dir = "~/app/app/static"
    seconds = time() - (60 * cycle)

    if path.exists(data_dir):
        for entry in scandir(data_dir):
            if seconds >= stat(entry).st_ctime and entry.is_file():
                remove(entry)
                if not path.exists(entry.path):
                    deleted_files_count += 1

    return deleted_files_count
