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


def iSmartWebCrawler(driver, cur_dt):
    # --------------------------------------- Query Date Condition Setting --------------------------------------------- #
    driver.find_element_by_name('year').send_keys(cur_dt.year)
    driver.find_element_by_name('month').send_keys(str(cur_dt.month).zfill(2))
    driver.find_element_by_name('day').send_keys(str(cur_dt.day).zfill(2))
    driver.find_element_by_xpath('//*[@class="btn_search"]').click()    # 조회 버튼 클릭
    html = driver.page_source                                           # 페이지의 elements 모두 가져오기
    soup = bs(html, 'html.parser')                                      # BeautifulSoup 사용하기
    table = soup.select('#printArea > div > table.basic_table > tbody > tr')
    # table = soup.select('#printArea > div.hori_table1 > table.basic_table > tbody > tr')
    # ------------------------------------------------------------------------------------------------------------------ #

    dataList = {}
    for idx, val in enumerate(table):           # table row 리스트로 분리
        data = val.text.strip().split('\n')     # td 분리
        dataList[idx] = data
        if idx > 0 and idx < 13:                # 두번째 table 컬럼명 제거/데이터 유형 변환(str -> float)
            dataList[idx] = [float(i) for i in data]
        elif idx > 12:
            if idx is 13:
                del data
            else:
                dataList[idx - 1] = [float(i) for i in data]
    del dataList[0]
    del dataList[25]

    dict_data = {}
    for i in dataList:
        if i > 0:
            dataList[i][0] = int(dataList[i][0])
            if dataList[i][0] is 24:
                dataList[i][0] = 00
            baseTime = datetime.time(dataList[i][0], 00, 00)
            dataList[i][0] = datetime.datetime.combine(cur_dt, baseTime)
    # print("dataList : ", dataList)
    dict_data['data'] = dataList
    return dict_data

@transaction.atomic
def setSqlProcedure():
    try:
        cursor = connection.cursor()
        sql_proc_stmt = ("DELIMITER $$ " +
                        "DROP PROCEDURE IF EXISTS test.SetEnergyData$$ " +
                        "CREATE PROCEDURE test.SetEnergyData(IN condo_id VARCHAR(4), " +
                                                            "IN crawled_data DOUBLE, IN dateTime DATETIME(6)) " +
                        "BEGIN " +
                            "IF EXISTS(" +
                                    "SELECT * FROM test.energy_energyusage E " +
                                    "WHERE E.condo_id = condo_id AND DATE_FORMAT(E.dateTime, '%%Y-%%m-%%d %%H:%%i:%%s') = dateTime " +
                                ") THEN " +
                                "UPDATE test.energy_energyusage E " +
                                "SET E.use_amt = crawled_data " +
                                "WHERE E.id = (SELECT A.id " +
                                                "FROM (" +
                                                        "SELECT E.id FROM test.energy_energyusage E " +
                                                        "WHERE E.condo_id = condo_id " +
                                                        "AND DATE_FORMAT(E.dateTime, '%%Y-%%m-%%d %%H:%%i:%%s') = dateTime" +
                                                        ") " +
                                                "A);" +
                            "ELSE " +
                                "INSERT INTO test.energy_energyusage (id, condo_id, peak, use_amt, dateTime) " +
                                "VALUES(NULL, condo_id, NULL, crawled_data, dateTime);" +
                        "END IF;" +
                        "END $$ " +
                        "DELIMITER;")

        cursor.execute(sql_proc_stmt)
        # print(sql_proc_stmt)
        print('Procedure SetEnergyData is Completed')
    except Exception as ex:  # 에러 종류
        print('sql error', ex)  # ex는 발생한 에러의 이름을 받아오는 변수


@transaction.atomic
def setCrawledData(condo_id, crawled_data, dateTime):
    try:
        cursor = connection.cursor()
        cursor.callproc('test.SetEnergyData', [condo_id, crawled_data, dateTime])
        # for result in cursor.stored_results():
        #     print(result.fetchall())
        # sql_stmt = ("CALL test.SetEnergyData(%s, %s, %s);")
        # cursor.execute(sql_stmt, (condo_id, use_amt, dateTime))
    except Exception as ex:  # 에러 종류
        print('sql error', ex)  # ex는 발생한 에러의 이름을 받아오는 변수
    # finally:
    #     # closing database connection.
    #     if (cursor.connection):
    #         cursor.close()
    #         print("connection is closed")



def getDataLastYear(driver, cur_dt):
    dict_data = iSmartWebCrawler(driver, cur_dt)
    for i in dict_data['data']:
        # print('condo_id : ', 'OVYY', ', 당일 : ', dict_data['data'][i][1], ', 일시 : ', dict_data['data'][i][0])
        # print('condo_id : ', 'OVYY', ', 전년동일 : ', dict_data['data'][i][3], ', 일시 : ', dict_data['data'][i][0] - datetime.timedelta(days=365))
        setCrawledData('OVYY', dict_data['data'][i][1], dict_data['data'][i][0])
        setCrawledData('OVYY', dict_data['data'][i][3], dict_data['data'][i][0] - datetime.timedelta(days=365))

def getDataYesterday(driver, cur_dt):
    dict_data = iSmartWebCrawler(driver, cur_dt)
    for i in dict_data['data']:
        # print('condo_id : ', 'OVYY', ', 당일 : ', dict_data['data'][i][1], ', 일시 : ', dict_data['data'][i][0])
        # print('condo_id : ', 'OVYY', ', 전일 : ', dict_data['data'][i][3], ', 일시 : ', dict_data['data'][i][0] - datetime.timedelta(days=365))
        setCrawledData('OVYY', dict_data['data'][i][1], dict_data['data'][i][0])
        setCrawledData('OVYY', dict_data['data'][i][2], dict_data['data'][i][0] - datetime.timedelta(days=1))

def setCrawlingSite(params):
    print(params)
    # params = {
    #     'type': '',     # 웹사이트 구분 {'ismart', 'econdo'}
    #     'url': '',      # 주소
    #     'user': {       # 사용자계정
    #         'id': '',
    #         'pw': ''
    #     },
    #     'strDt': '',    # 조회시작일자
    #     'endDt': ''     # 조회종료일자
    # }
    # --------------------------------------- ChromeDriver Option Setting ---------------------------------------------- #
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")
    # 혹은 options.add_argument("--disable-gpu")
    driver = webdriver.Chrome('/Users/jooyu/Downloads/chromedriver_win32/chromedriver', chrome_options=options)
    # Chrome 의 경우, chrome driver 위치를 지정
    driver.implicitly_wait(3)                                           # 암묵적으로 웹 자원 로드를 위해 3초 delay

    # ----------------------------------------- Element Control Setting ------------------------------------------------ #

    driver.get(params['url']) # URL 접근
    driver.find_element_by_name(params['xpath']['id']).send_keys(params['user']['id'])       # 아이디/비밀번호 입력
    driver.find_element_by_name(params['xpath']['pw']).send_keys(params['user']['pw'])
    driver.find_element_by_xpath(params['xpath']['login']).click()     # 로그인 버튼을 클릭
    # driver.find_element_by_id('simpleAlert').click()
    driver.implicitly_wait(10)
    # driver.switch_to.frame(0)
    html = driver.page_source
    print(html)
    # driver.find_element_by_css_selector("a[href*='/condo_work/?right_url=reservation/reservation/reservation_list.php']").click()
    # driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/table/tbody/tr[2]/td[8]/a').send_keys('\n')
    # driver.get('https://pccs.kepco.co.kr/iSmart/pccs/usage/readTrendTimeList.do')
    # ----------------------------------------- Query Condition Setting ------------------------------------------------ #
    # driver.find_element_by_xpath('//*[@id="txt"]/div[3]/div/div[1]/label[2]').click()   # 사용량 조회(Default: 최대 수요)
    # ------------------------------------------------------------------------------------------------------------------ #
    today = datetime.datetime.now()
    start_dt = datetime.date(2018, 9, 1)
    end_dt = today.date()
    cur_dt = start_dt - timedelta(days=0)
    # setSqlProcedure()

    print(cur_dt)
    # 정책 수정 전
    # while (cur_dt <= end_dt):
    #     print(cur_dt)
    #     # 시작일과 같은 해일 경우, 하루마다 조회하고 당일, 전년동일 데이터 저장
    #     if cur_dt.year == start_dt.year:
    #         getDataLastYear(driver, cur_dt)
    #         cur_dt += timedelta(days=1)
    #     # 시작일과 같은 해가 아닌 경우, 이틀마다 조회하고 당일, 전일 데이터 저장
    #     else:
    #         getDataYesterday(driver, cur_dt)
    #         cur_dt += timedelta(days=2)

    # 정책 수정 후(1년)
    # while (cur_dt <= end_dt):
    #     print(cur_dt)
    #     getDataLastYear(driver, cur_dt)
    #     cur_dt += timedelta(days=1)
    # 
    # getDataYesterday(driver, end_dt)        # 마지막은 오늘 날짜로 조회
    # driver.quit()
