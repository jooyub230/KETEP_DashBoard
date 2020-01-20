from selenium import webdriver
from bs4 import BeautifulSoup as bs
import datetime
import calendar
import os
import django
from django.db import transaction
from datetime import timedelta, date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.db import connection

# django setting 파일 설정하기 및 장고 셋업
cur_dir = os.path.dirname(__file__)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KETEP_DashBoard.settings")
django.setup()

# 모델 임포트는 django setup이 끝난 후에 가능하다. 셋업 전에 import하면 에러난다. db connection 정보가 없어서......
from energy.models import EnergyUsage


@transaction.atomic
def iSmartWebCrawler(driver, current_dt, start_dt, end_dt):
    # 날짜 입력
    driver.find_element_by_name('year').send_keys(current_dt.year)
    driver.find_element_by_name('month').send_keys(str(current_dt.month).zfill(2))
    driver.find_element_by_name('day').send_keys(str(current_dt.day).zfill(2))

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
        data = val.text.strip().split('\n')  # 5개 항목 분리
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

    queryDate = current_dt
    for i in dataList:
        if i > 0:
            dataList[i][0] = int(dataList[i][0])
            try:
                if dataList[i][0] is 24:
                    dataList[i][0] = 00
                baseTime = datetime.time(dataList[i][0], 00, 00)
                queryDate = datetime.datetime.combine(queryDate, baseTime)
                minusOneYear = datetime.datetime.combine(date(queryDate.year-1, queryDate.month, queryDate.day), baseTime)
                minusOneDay = queryDate - datetime.timedelta(days=1)
                try:
                    if current_dt.year == start_dt.year:
                        # print(queryDate, dataList[i][1])
                        # print(minusOneYear, dataList[i][3])
                        # EnergyUsage.objects.create(condo_id='OVYY', peak=dataList[i][1], dateTime=queryDate)
                        # EnergyUsage.objects.create(condo_id='OVYY', peak=dataList[i][3], dateTime=minusOneYear)
                        EnergyUsage.objects.create(condo_id='OVYY', usage=dataList[i][1], dateTime=queryDate)
                        EnergyUsage.objects.create(condo_id='OVYY', usage=dataList[i][3], dateTime=minusOneYear)
                    else:
                        # if current_dt.year == end_dt.year-2:
                            # print(minusOneYear, dataList[i][3])
                            # EnergyUsage.objects.create(condo_id='OVYY', peak=dataList[i][3], dateTime=minusOneYear)
                        print(queryDate, dataList[i][1])
                        print(minusOneDay, dataList[i][2])
                        # EnergyUsage.objects.create(condo_id='OVYY', peak=dataList[i][1], dateTime=queryDate)
                        # EnergyUsage.objects.create(condo_id='OVYY', peak=dataList[i][2], dateTime=minusOneDay)
                except Exception as ex:  # 에러 종류
                    print('딕트타입 에러가 발생 했습니다', ex)  # ex는 발생한 에러의 이름을 받아오는 변수
            except Exception as ex:  # 에러 종류
                print('에러가 발생 했습니다', ex)  # ex는 발생한 에러의 이름을 받아오는 변수


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")
    # 혹은 options.add_argument("--disable-gpu")

    # Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
    driver = webdriver.Chrome('/Users/jooyu/Downloads/chromedriver_win32/chromedriver', chrome_options=options)
    # 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
    driver.implicitly_wait(3)
    # url에 접근한다.
    driver.get('https://pccs.kepco.co.kr/iSmart/jsp/cm/login/main.jsp')
    # 아이디/비밀번호를 입력해준다.
    driver.find_element_by_name('userId').send_keys('0710006240')
    driver.find_element_by_name('password').send_keys('sm009200**')
    # 로그인 버튼을 눌러주자.
    driver.find_element_by_xpath('//*[@class="login_btn"]').click()
    driver.get('https://pccs.kepco.co.kr/iSmart/pccs/usage/readTrendTimeList.do')
    # ------------------------------------------------------------------------------------------------------#
    # 사용량 조회(Default: 최대 수요)
    # driver.find_element_by_xpath('//*[@id="txt"]/div[3]/div/div[1]/label[2]').click()
    # ------------------------------------------------------------------------------------------------------#
    today = datetime.datetime.now()
    # start_dt = date(today.year - 2, 1, 1)
    start_dt = date(2018, 8, 1)
    end_dt = date.today()
    current_dt = start_dt - timedelta(days=1)
    print("start_dt : ", start_dt, "end_dt : ", end_dt, "current_dt : ", current_dt)
    for dt in range(0, (end_dt - start_dt).days + 1):
        if dt <= 365:
            current_dt += timedelta(days=1)
            print("current_dt : ", current_dt)
            # iSmartWebCrawler(driver, current_dt, start_dt, end_dt)
        else:
            if dt % 2 == 0:
                current_dt += timedelta(days=2)
                print("current_dt : ", current_dt)
                # iSmartWebCrawler(driver, current_dt, start_dt, end_dt)
        print("dt : ", dt)
    driver.quit()

    # 날짜별 조회 test
    # start_date = datetime.date(2016, 1, 10)
    # end_date = datetime.date(2016, 1, 11)
    # queryset = EnergyUsage.objects.all().filter(dateTime__range=(start_date, end_date)).values('usage', 'dateTime').order_by('dateTime')
    # for i in queryset:
    #     print(i)