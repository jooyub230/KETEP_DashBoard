from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
import datetime
# from energy.models import EnergyUsage
# from energy.models import EnergyUsage

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
driver.find_element_by_name('month').send_keys('02')
driver.find_element_by_xpath('//*[@class="btn_search"]').click()
html = driver.page_source  # 페이지의 elements모두 가져오기
soup = bs(html, 'html.parser')  # BeautifulSoup사용하기
# table = soup.select('#printArea > div.hori_table1 > table.basic_table > tbody > tr')
table = soup.select('#printArea > div > table.basic_table > tbody > tr')
# driver.quit()

# for n in notices:
#     print(n.text.strip())
dataList = {}
data = {}
for idx, val in enumerate(table):
    data = val.text.strip().split('\n')
    dataList[idx] = data
    if idx > 0 and idx < 13:
        dataList[idx] = [float(i) for i in data]
    elif idx > 12:
        if idx is 13:
            del data
        else:
            dataList[idx - 1] = [float(i) for i in data]
del dataList[25]
# print(idx, data, type(data))

d = datetime.date(2019, 2, 1)
for i in dataList:
    if i > 0:
        dataList[i][0] = int(dataList[i][0])
        try:
            if dataList[i][0] is 24:
                dataList[i][0] = 00
            t = datetime.time(dataList[i][0], 00, 00)
            dt = datetime.datetime.combine(d, t)
            print(dataList[i][0], dataList[i][1], dt)
            # EnergyUsage.objects.create(condo_id='오션벨리', usage=dataList[i][1], dateTime=dt)
        except Exception as ex:  # 에러 종류
            print('에러가 발생 했습니다', ex)  # ex는 발생한 에러의 이름을 받아오는 변수
