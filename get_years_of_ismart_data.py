from selenium import webdriver
from bs4 import BeautifulSoup as bs
import datetime
import calendar
import os
import django
from django.db import transaction

# django setting 파일 설정하기 및 장고 셋업
cur_dir = os.path.dirname(__file__)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KETEP_DEV.settings")
django.setup()

# 모델 임포트는 django setup이 끝난 후에 가능하다. 셋업 전에 import하면 에러난다. db connection 정보가 없어서......
from energy.models import EnergyUsage

@transaction.atomic
def iSmartWebCrawler(driver, year, month, day):
    driver.find_element_by_name('year').send_keys(year)
    driver.find_element_by_name('month').send_keys(month)
    driver.find_element_by_name('day').send_keys(day)
    driver.find_element_by_xpath('//*[@class="btn_search"]').click()

    html = driver.page_source  # 페이지의 elements모두 가져오기
    soup = bs(html, 'html.parser')  # BeautifulSoup사용하기
    # table = soup.select('#printArea > div.hori_table1 > table.basic_table > tbody > tr')
    table = soup.select('#printArea > div > table.basic_table > tbody > tr')
    # print(table)

    dataList = {}
    data = {}
    # table > tr > td 리스트로 분리
    for idx, val in enumerate(table):
        data = val.text.strip().split('\n') # 5개 항목 분리
        dataList[idx] = data
        if idx > 0 and idx < 13:
            dataList[idx] = [float(i) for i in data]
        elif idx > 12:
            if idx is 13:
                del data
            else:
                dataList[idx - 1] = [float(i) for i in data]
    del dataList[25]

    month_data_dic = {}

    queryDate = datetime.date(int(year), int(month), int(day))
    for i in dataList:
        if i > 0:
            dataList[i][0] = int(dataList[i][0])
            try:
                if dataList[i][0] is 24:
                    dataList[i][0] = 00
                baseTime = datetime.time(dataList[i][0], 00, 00)
                queryDate = datetime.datetime.combine(queryDate, baseTime)

                minusOneDay = queryDate - datetime.timedelta(days=1)
                try:
                    # key = dataList[i][0]
                    # month_data_dic[key] = {}
                    # month_data_dic[key][0] = {"condo_id":"오션벨리", "usage":dataList[i][2], "dateTime":minusOneDay}
                    # month_data_dic[key][1] = {"condo_id": "오션벨리", "usage": dataList[i][1], "dateTime": queryDate}
                    # print(queryDate.strftime("%Y-%m-%d %H:%M"))
                    # print(month_data_dic[key])
                    EnergyUsage.objects.create(condo_id='OVYY', usage=dataList[i][2], dateTime=minusOneDay)
                    EnergyUsage.objects.create(condo_id='OVYY', usage=dataList[i][1], dateTime=queryDate)
                    # month_data_dic[i] = []
                    # hour_data_list[i] = {}
                    # hour_data_list[i] = {"condo_id":"오션벨리", "usage":dataList[i][2], "dateTime":minusOneDay}
                    # hour_data_list[i] = {"condo_id": "오션벨리", "usage": dataList[i][1], "dateTime": queryDate}
                    # print(month_data_dic)

                    # print(dataList[i][0], dataList[i][2], minusOneDay)
                    # print(dataList[i][0], dataList[i][1], queryDate) # 시간, 당일, 전일, 날짜시간
                    # EnergyUsage.objects.create(condo_id='오션벨리', usage=dataList[i][1], dateTime=dt)
                except Exception as ex:  # 에러 종류
                    print('딕트타입 에러가 발생 했습니다', ex)  # ex는 발생한 에러의 이름을 받아오는 변수
            except Exception as ex:  # 에러 종류
                print('에러가 발생 했습니다', ex)  # ex는 발생한 에러의 이름을 받아오는 변수

if __name__ == "__main__":
    # options = webdriver.ChromeOptions()
    # # options.add_argument('headless')
    # # options.add_argument('window-size=1920x1080')
    # # options.add_argument("disable-gpu")
    # # 혹은 options.add_argument("--disable-gpu")
    #
    # # Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
    # driver = webdriver.Chrome('/Users/jooyu/Downloads/chromedriver_win32/chromedriver', chrome_options=options)
    # # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    # driver.implicitly_wait(3)
    # # url에 접근한다.
    # driver.get('https://pccs.kepco.co.kr/iSmart/jsp/cm/login/main.jsp')
    # # 아이디/비밀번호를 입력해준다.
    # driver.find_element_by_name('userId').send_keys('0710006240')
    # driver.find_element_by_name('password').send_keys('sm009200**')
    # # 로그인 버튼을 눌러주자.
    # driver.find_element_by_xpath('//*[@class="login_btn"]').click()
    # driver.get('https://pccs.kepco.co.kr/iSmart/pccs/usage/readTrendTimeList.do')
    #
    today = datetime.datetime.now()
    # strToday = today.strftime("%Y-%m-%d %H:%M")
    strToday = today.strftime("%Y-%m-%d")
    #
    # # 최근 몇년의 데이터를 가져올지 설정
    # latelyYear = 2 # 전일, 당일 데이터 동시에 크롤링
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
    #                 # print("당일 데이터만 처리")
    #                 # print(year, "년 ", month, "월 ", day, "일")
    #                 iSmartWebCrawler(driver, year, month, day)
    #             else:
    #                 day = str(2*d).zfill(2)
    #                 iSmartWebCrawler(driver, year, month, day)
    #
    # driver.quit()

    # 날짜별 조회 test
    # start_date = datetime.date(2019, 4, 1)
    # end_date = datetime.date(2019, 4, 2)
    # queryset = EnergyUsage.objects.all().filter(dateTime__range=(start_date, end_date)).values('usage', 'dateTime').order_by('dateTime')
    # for i in queryset:
    #     print(i)