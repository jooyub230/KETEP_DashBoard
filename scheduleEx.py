import schedule
import time


def job():
    now = time.localtime()
    current = "%04d-%02d-%02d %02d:%02d:%02d" % \
              (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    print("Current time = ", str(current))


# schedule.every(2).seconds.do(job) # 10초에 한번씩 job 함수를 실행
    # schedule.every(10).minutes.do(job) # 10분에 한번씩 job 함수를 실행
    # schedule.every().hour.do(job) # 매 시간에 job 함수를 실행
    # schedule.every().day.at("10:30").do(job) # 매일 10:30분에 job함수를 실행

# 매초 schedule를 실행
# while 1:
#     schedule.run_pending()
#     time.sleep(1)
