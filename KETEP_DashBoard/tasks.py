from __future__ import absolute_import

from KETEP_DashBoard.celery_old import app
# from scheduled_crawler.crawler import setCrawlingSite
# from scheduled_crawler.crawler_20200117 import setCrawlingSite

@app.task
def crawlingScheduler():     # 실제 백그라운드에서 작업할 내용을 task로 정의한다.
    print("celery beat TEST")
#     # setCrawlingSite(params)
#     setCrawlingSite(type='ismart', column='peak')
#     setCrawlingSite(type='ismart', column='usage')

@app.task
def say_hello():
    print("ggg")