# import calendar
# import datetime
# today = datetime.datetime.now()
# strToday = today.strftime("%Y-%m-%d %H:%M")
# 최근 몇 년의 데이터를 가져올지 설정

# latelyYear = 1 # 전일, 당일 데이터 동시에 크롤링
# for y in range(latelyYear):
#     for m in range(12):
#         year = today.year-y
#         month = today.month
#         if month - m <= 0: # i > 4
#             year = today.year - (y+1)
#             month = 12 + today.month - m
#         else:
#             month -= m
#         lastDay = calendar.monthrange(year, month)[1]
#         month = str(month).zfill(2)
#         plusOneDay = lastDay
#         print(year, "년 ", month, "월의 말일은 ", lastDay)
#         if lastDay % 2 is 1:
#             plusOneDay = lastDay + 1
#         half_lastDay = plusOneDay // 2
#         for d in range(1, half_lastDay + 1):
#             if (plusOneDay != lastDay) and (d == half_lastDay):
#                 day = lastDay
#                 print("당일 데이터만 처리")
#                 print(year, "년 ", month, "월 ", day, "일")
#             else:
#                 day = str(2*d).zfill(2)
#                 print(year, "년 ", month, "월 ", day, "일")

# from datetime import timedelta, date
# import datetime
#
# today = datetime.datetime.now()
# start_dt = datetime.date(2018, 8, 1)
# end_dt = today.date()
# cur_dt = start_dt - timedelta(days=0)
#
# while (cur_dt <= end_dt):
#     # for i in range(0, 24):
#     #     baseTime = datetime.time(i, 00, 00)
#     #     queryDate = datetime.datetime.combine(cur_dt, baseTime)
#     print("cur_dt :", cur_dt)
#     if cur_dt.year == start_dt.year:  # 시작일과 같은 해일 경우, 하루마다 조회하고 당일, 전년동일 데이터 저장
#         # minusOneYear = datetime.datetime.combine(date(queryDate.year-1, queryDate.month, queryDate.day), baseTime)
#         minusOneYear = datetime.date(cur_dt.year - 1, cur_dt.month, cur_dt.day)
#         cur_dt += timedelta(days=1)
#         print("minusOneYear :", minusOneYear)
#     else:  # 시작일과 같은 해가 아닌 경우, 이틀마다 조회하고 당일, 전일 데이터 저장
#         minusOneDay = cur_dt - datetime.timedelta(days=1)
#         cur_dt += timedelta(days=2)
#         print("minusOneDay :", minusOneDay)
    # cur_dt =- timedelta(days=1)

    # cur_dt -= timedelta(days=-1)
# def daterange(date1, date2):
#     days = {}
#     for n in range(int ((date2 - date1).days)+1):
#         yield date1 + timedelta(n)
#
# today = datetime.datetime.now()
# start_dt = date(today.year-2, 1, 1)
# end_dt = date(today.year, today.month, today.day)
# for dt in daterange(start_dt, end_dt):
#     print(dt.strftime("%Y-%m-%d"))

# today = datetime.datetime.now()
# start_dt = date(today.year-2, 1, 1)
# end_dt = date(today.year, today.month, today.day)
# current_dt = start_dt - timedelta(days=1)
# for dt in range(0, (end_dt-start_dt).days+1):
#     if dt <= 365:
#         current_dt += timedelta(days=1)
#         print(dt, current_dt)
#     else:
#         if dt % 2 == 0:
#             current_dt += timedelta(days=2)
#             print(dt, current_dt)

    # year = str(current_dt.year).zfill(2)
    # month = str(current_dt.month).zfill(2)
    # day = str(current_dt.day).zfill(2)
    # print(year, month, day)

