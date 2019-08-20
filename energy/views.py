from selenium import webdriver
from bs4 import BeautifulSoup as bs
import datetime
import json
from django.core import serializers
from .models import EnergyUsage
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from energy.forms import GetQueryForm
from django.db.models import Q
from django.shortcuts import render
from django.db import connection
import calendar

# Create your views here.
# class SearchFormView(FormView):
#     print("searchFormView")
#     from_class = GetQueryForm
#     template_name = 'energy_analysis.html'
#
#     def form_valid(self, form):
#         query_date = '%s' % self.request.POST['query_date']
#         print(query_date)
@csrf_exempt
def getUsage(request):
    # year = int(request.GET.get('year'))
    # month = int(request.GET.get('month'))
    # day = int(request.GET.get('day'))
    # queryDate = datetime.date(year, month, day)
    term = request.GET.get('term')
    form_data_dict = {}
    form_data_list = json.loads(request.GET.get('formData'))
    for field in form_data_list:
        form_data_dict[field["name"]] = field["value"]
    print(term)
    print(form_data_dict)
    if term == 'times':
        str_date = form_data_dict['date']
        start_date = datetime.datetime.strptime(str_date, "%Y-%m-%d").date()
        ismart_dic = list(EnergyUsage.objects.all().filter(dateTime__year=start_date.year, dateTime__month=start_date.month, dateTime__day=start_date.day).values('peak', 'use_amt', 'dateTime').order_by('dateTime'))
        for idx, item in enumerate(ismart_dic):
            ismart_dic[idx]['dateTime'] = int(item['dateTime'].strftime("%H"))
        ismart_dic[0]['dateTime'] = 24
        ismart_dic.append(ismart_dic[0])
        del ismart_dic[0]

        return JsonResponse(ismart_dic, safe=False)
    elif term == 'days':
        month = form_data_dict['month']
        year = form_data_dict['year']
        cursor = connection.cursor()
        cursor.execute(
            "SELECT " +
            "DATE_FORMAT(E.dateTime, '%%Y-%%m-%%d') AS date, " +
            "MAX(E.peak) max_peak, ROUND(SUM(E.use_amt), 2) sum_use_amt " +
            "FROM test.energy_energyusage E " +
            "WHERE year(E.dateTime)=%s AND month(E.dateTime)=%s " +
            "GROUP BY date", [year, month])
        rows = list(cursor.fetchall())
        print("rows length : ", len(rows))
        print(calendar.monthrange(int(year), int(month))[1])

        for i in range(len(rows)):
            rows[i] = list(rows[i])

        for idx, item in enumerate(rows):
            rows[idx][0] = int((rows[idx][0]).split('-')[2])
        print(rows)
        return JsonResponse(rows, safe=False)
    elif term == 'months':
        year = form_data_dict['year']
        cursor = connection.cursor()
        cursor.execute(
            "SELECT " +
            "DATE_FORMAT(E.dateTime, '%%Y-%%m') AS date, " +
            "MAX(E.peak) max_peak, ROUND(SUM(E.use_amt), 2) sum_use_amt " +
            "FROM test.energy_energyusage E " +
            "WHERE year(E.dateTime)=%s " +
            "GROUP BY date", [year])
        rows = list(cursor.fetchall())
        for i in range(len(rows)):
            rows[i] = list(rows[i])

        for idx, item in enumerate(rows):
            rows[idx][0] = int((rows[idx][0]).split('-')[1])
        print(rows)
        return JsonResponse(rows, safe=False)
    else:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT " +
            "DATE_FORMAT(E.dateTime, '%Y') AS date, " +
            "MAX(E.peak) max_peak, ROUND(SUM(E.use_amt), 2) sum_use_amt " +
            "FROM test.energy_energyusage E " +
            "GROUP BY date")
        rows = list(cursor.fetchall())
        for i in range(len(rows)):
            rows[i] = list(rows[i])

        print(rows)
        return JsonResponse(rows, safe=False)

    # baseTime = datetime.time(1, 0, 0)
    # start_date = datetime.datetime.combine(queryDate, baseTime)
    # end_date = start_date + datetime.timedelta(days=1) - datetime.timedelta(hours=1)
    #
    # ismart_dic = list(EnergyUsage.objects.all().filter(dateTime__range=(start_date, end_date)).values('usage', 'dateTime').order_by('dateTime'))
    # for idx, item in enumerate(ismart_dic):
    #     ismart_dic[idx]['dateTime'] = int(item['dateTime'].strftime("%H"))
    # return JsonResponse(ismart_dic, safe=False)

def iSmartWebCrawler(today):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
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

    html = driver.page_source # 페이지의 elements모두 가져오기
    soup = bs(html, 'html.parser') # BeautifulSoup사용하기
    # table = soup.select('#printArea > div.hori_table1 > table.basic_table > tbody > tr')
    table = soup.select('#printArea > div > table.basic_table > tbody > tr')
    driver.quit()

    data_dic = {}
    data_dic['data'] = []
    for idx, val in enumerate(table):
        data = list(val.text.strip().split('\n'))
        # print("idx : ", idx, "data : ", data)
        if idx != 0 and idx != 13:
            # data_dic['data'].append([float(i) for i in data])
            data_dic['data'].append(data)
        # else:
        #     del data
        # elif idx > 12:
        #     if idx is 13:
        #         del data
        #     else:
        #         data_dic['data'][idx-1] = [float(i) for i in data]

        # print(idx, data, type(data))

    # d = datetime.date(2019, 2, 1)
    # for i in dataList:
    #     if i > 0:
    #         dataList[i][0] = int(dataList[i][0])
    #         try:
    #             if dataList[i][0] is 24:
    #                 dataList[i][0] = 00
    #             t = datetime.time(dataList[i][0], 00, 00)
    #             dt = datetime.datetime.combine(today, t)
    #             # print(dataList[i][0], dt)
    #             # EnergyUsage.objects.create(condo_id='오션벨리', use_amt=dataList[i][1], dateTime=dt)
    #         except Exception as ex:  # 에러 종류
    #             print('에러가 발생 했습니다', ex)  # ex는 발생한 에러의 이름을 받아오는 변수
        # print(dataList[i])
    # for i in dataList:
    #     EnergyUsage(condo_id=dataList[i][0], use_amt=dataList[i][1]).save()
    print(data_dic)
    return data_dic