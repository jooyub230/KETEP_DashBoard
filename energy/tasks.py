from __future__ import absolute_import

from KETEP_DashBoard.celery_old import app

@app.task
def say_hello():
    print("hellow world!")