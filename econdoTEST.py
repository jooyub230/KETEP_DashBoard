import os
import django
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import timedelta
import datetime
from django.db import connection, transaction
import pymysql

# django setting 파일 설정하기 및 장고 셋업
cur_dir = os.path.dirname(__file__)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KETEP_DashBoard.settings")
django.setup()

def setCrawlingSite(type, column):
    params = [{
        'type': 'econdo',     # 웹사이트 구분 {'ismart', 'econdo'}
        'url': 'http://intra.econdo.net/login.html',      # 주소
        'user': {       # 사용자계정
            'id': 'saendog',
            'pw': '0115'
        },
        'xpath': {
            'id': 'id',
            'pw': 'passwd',
            'login': '//*[@class="adTB"]//tbody/tr/td/table/tbody/tr[2]/td[2]/img'
        },
        'strDt': '',    # 조회시작일자
        'endDt': ''     # 조회종료일자
    },{
        'type': 'ismart',
        'url': 'https://pccs.kepco.co.kr/iSmart/jsp/cm/login/main.jsp',
        'user': {
            'id': '0710006240',
            'pw': 'sm009200**'
        },
        'xpath': {
            'id': 'userId',
            'pw': 'password',
            'login': '//*[@class="login_btn"]'
        },
        'strDt': '',
        'endDt': ''
    }]
    option = ''
    for idx, val in enumerate(params):
        if params[idx]['type'] == type:
            option = params[idx]
    option["column"] = column
    return option
    # driver.get('https://pccs.kepco.co.kr/iSmart/pccs/usage/readTrendTimeList.do')
    # # ----------------------------------------- Query Condition Setting ------------------------------------------------ #
    # driver.find_element_by_xpath('//*[@id="txt"]/div[3]/div/div[1]/label[2]').click()
    # getCrawlingSite(params)

def getCrawlingSite(params):
    # --------------------------------------- ChromeDriver Option Setting ---------------------------------------------- #
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
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
    # driver.switch_to.frame(0)

    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
        print("alert accepted")
    except TimeoutException:
        print("no alert")

    if params['type'] == 'econdo':
        driver.switch_to.frame(0)
        driver.find_element_by_css_selector("a[href*='/condo_work/?right_url=reservation/reservation/reservation_list.php']").click()
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_css_selector("frame[name='f_main']"))
        driver.switch_to.frame(driver.find_element_by_css_selector("frame[name='right']"))
        ## 페이지 하나씩 크롤링 (처음부터 끝까지)
        print('page : ', 1)
        econdoWebCrawler(driver)
        pages = driver.find_elements_by_xpath('/html/body/table[3]/tbody/tr/td/a')
        for page in range(1, len(pages)+1):
            print('page : ', page+1)
            driver.find_element_by_xpath('/html/body/table[3]/tbody/tr/td/a[%s]' % page).click()
            econdoWebCrawler(driver)

    elif params['type'] == 'ismart':
        print('column = ', params['column'])
        driver.get('https://pccs.kepco.co.kr/iSmart/pccs/usage/readTrendTimeList.do')
        # ----------------------------------------- Query Condition Setting ------------------------------------------------ #
        if params['column'] == 'usage':
            driver.find_element_by_xpath('//*[@id="txt"]/div[3]/div/div[1]/label[2]').click()  # 사용량 조회(Default: 최대 수요)
        # ------------------------------------------------------------------------------------------------------------------ #
        # start_dt = getLastDate()
        # print('start_dt = ', start_dt, 'type = ', type(start_dt))

        today = datetime.datetime.now()
        start_dt = today.date()
        # start_dt = datetime.date(2020, 1, 18)
        end_dt = today.date()
        # end_dt = datetime.date(2019, 8, 1)
        cur_dt = start_dt - timedelta(days=0)
        while (cur_dt <= end_dt):
            print("cur_dt : ", cur_dt)
            getDataLastYear(driver, cur_dt, params['column'])
            cur_dt += timedelta(days=1)

        getDataYesterday(driver, end_dt, params['column'])        # 마지막은 오늘 날짜로 조회

    # driver.implicitly_wait(300000)
    driver.quit()

def econdoWebCrawler(driver):
    html = driver.page_source  # 페이지의 elements 모두 가져오기
    soup = bs(html, 'html.parser')  # BeautifulSoup 사용하기
    table = soup.select('body > table:nth-child(3) > tbody > tr')

    dataList = {}
    key = []
    for idx, val in enumerate(table):  # table row 리스트로 분리
        if idx <= 0:
            key = val.text.strip().split('\n')  # td 분리
            print('key : ', key)
        else:
            data = {}
            col = val.find_all('td')
            for i, txt in enumerate(col):
                text = txt.get_text().strip()
                data[key[i]] = text
            dataList[idx-1] = data
    print('dataList : ', dataList)

@transaction.atomic
def setCrawledData(condo_id, crawled_data, dateTime, colName):
    try:
        cursor = connection.cursor()
        cursor.callproc('ketep.SetEnergyData', [condo_id, crawled_data, dateTime, colName])
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

@transaction.atomic
def getLastDate():
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT " +
            "DATE_FORMAT(dateTime, '%Y-%m-%d') AS date " +
            "FROM ketep.energy_energyusage " +
            "ORDER BY datetime DESC LIMIT 1")
        row = cursor.fetchone()
        print(row)
        # print(row['dateTime'])
    except Exception as ex:  # 에러 종류
        print('sql error', ex)  # ex는 발생한 에러의 이름을 받아오는 변수
    # finally:
    #     # closing database connection.
    #     if (cursor.connection):
    #         cursor.close()
    #         print("connection is closed")
    return row

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

def getDataLastYear(driver, cur_dt, colName):
    dict_data = iSmartWebCrawler(driver, cur_dt)
    # print(dict_data)
    for i in dict_data['data']:
        setCrawledData('OVYY', dict_data['data'][i][1], dict_data['data'][i][0], colName)
        setCrawledData('OVYY', dict_data['data'][i][3], dict_data['data'][i][0] - datetime.timedelta(days=365), colName)

def getDataYesterday(driver, cur_dt, colName):
    dict_data = iSmartWebCrawler(driver, cur_dt)
    # print(dict_data)
    for i in dict_data['data']:
        setCrawledData('OVYY', dict_data['data'][i][1], dict_data['data'][i][0], colName)
        setCrawledData('OVYY', dict_data['data'][i][2], dict_data['data'][i][0] - datetime.timedelta(days=1), colName)

if __name__ == "__main__":
    option = setCrawlingSite(type='ismart', column='peak')
    print('option = ', option)
    getCrawlingSite(option)
    option = setCrawlingSite(type='ismart', column='usage')
    print('option = ', option)
    getCrawlingSite(option)
