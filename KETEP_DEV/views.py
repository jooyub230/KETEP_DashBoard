from django.shortcuts import render
import datetime
import pytz
import urllib
import json
import urllib.request
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpRequest, JsonResponse
from json import dumps
from django.core import serializers
from energy.models import EnergyUsage
from energy.views import iSmartWebCrawler
from datetime import timedelta, date
import schedule
import time


def index(request):
    return render(request, 'index.html')

# @csrf_exempt
# def getUsage(request):
#
#     return JsonResponse(usage_dic, safe=False)
# def goQuery(request):
    # dic = {}
    # years = []
    # months = []
    # year = datetime.date.today().strftime("%Y")
    # for i in range(12):
    #     years.append(int(year) - i)
    #     months.append(i + 1)
    # dic["years"] = years
    # dic["months"] = months
    # print(dic)
    # print("KETEP_DEV/view.py loaded")
    # return render(request, 'energy_query.html')
@csrf_exempt
def getIsmartData(request):
    today = datetime.date.today()
    print("today : ", today)
    ismart_dic = {'ismart_dic' : iSmartWebCrawler(today)}
    # start_date = today
    # end_date = today + timedelta(days=1)
    # ismart_dic = list(EnergyUsage.objects.all().filter(dateTime__range=(start_date, end_date)).values('usage', 'dateTime').order_by('dateTime'))

    # response_data = {}
    # response_data = serializers.serialize('json', ismart_dic)
    return JsonResponse(ismart_dic, safe=False)
    # return HttpResponse(json.dumps(ismart_dic, ensure_ascii=False), "application/json")
    # return render(request, 'energy_analysis.html')

@csrf_exempt
def getWeatherInfo(request):
    weather_dic = {'weather_dic' : get_weather_data()}
    wd = json.dumps(weather_dic, ensure_ascii=False)
    print(wd)
    return HttpResponse(json.dumps(weather_dic, ensure_ascii=False), "application/json")

def goControl(request):
    return render(request, 'system_control.html')

def goTarget(request):
    return render(request, 'target_management.html')

def goRooms(request):
    return render(request, 'room_management.html')

def goSuperAdmin(request):
    return render(request, 'super_admin.html')


def get_api_date():
    # timeStamp = datetime.datetime(2018, 8, 21, 1, 40, 5)              # 테스트 날짜
    timeStamp = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))   # 현재날짜&시간
    timeStamp_str = timeStamp.strftime('%Y%m%d%H%M')                    # 'YYYYmmddHHMM'
    base_date = timeStamp_str[:8]                                       # 'YYYYmmdd'
    time_now = timeStamp_str[-4:]                                       # 'HHMM'
    base_time = time_now[-4:-2] + "30"                                  # 01시 이후 45분 이상일 경우, 시간 기준

    if int(time_now[-4:-2]) < 1:
        # 00시 45분 미만일 경우, 전날 23시 30분 기준
        if int(time_now[-2:]) < 45 :
            base_date = (timeStamp-datetime.timedelta(1)).strftime('%Y%m%d')
            base_time = "2330"
    else :
        # 01시 이후 45분 미만일 경우, 1시간 전의 30분 기준
        if int(time_now[-2:]) < 45:
            anHourAgo = int(time_now[-4:-2])-1
            base_time = str(anHourAgo).zfill(2) + "30"

    return (base_date, base_time)

def get_weather_data():
    base_date, base_time = get_api_date()
    url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastTimeData?"
    serviceKey = "serviceKey=" + "kVg9rLjnKf6okRjj1j0rwMcsAgqpYlKnQr%2FQKZ9y807YHzLZZfdkjT7I0n%2BfLsLyLLgBLdojNSEu0E%2FEeSauqw%3D%3D"
    date = "&base_date=" + base_date
    time = "&base_time=" + base_time
    # 경기도 하남시 풍산동
    # nx = "&nx=63"
    # ny = "&ny=126"
    # 강원도 양양군 양양읍
    nx = "&nx=88"
    ny = "&ny=138"
    numOfRows = "&numOfRows=1000"
    pageNo = "&pageNo=1"
    type = "&_type=json"
    api_url = url + serviceKey + date + time + nx + ny + numOfRows + pageNo + type
    data = urllib.request.urlopen(api_url).read().decode("utf-8")
    data_json = json.loads(data)

    print("api : "+api_url)
    parsed_json = data_json['response']['body']['items']['item']
    baseDate = parsed_json[0]['baseDate']
    baseTime = parsed_json[0]['baseTime']
    weather_dic = {'baseDate':baseDate, 'baseTime':str(baseTime)[0:4]}
    code_dic = {'T1H':'기온', 'RN1':'1시간 강수량', 'SKY':'하늘상태', 'UUU':'동서바람성분', 'VVV':'남북바람성분', 'REH':'습도',
                'PTY':'강수형태', 'LGT':'낙뢰', 'VEC':'풍향', 'WSD':'풍속'}
    forecast_data = []
    times = []

    for idx, target_data in enumerate(parsed_json) :
        codeName = code_dic[target_data['category']]    # 코드명 한글로 변환
        fcstTime = target_data['fcstTime']

        if fcstTime not in times:
            times.append(fcstTime)
            forecast_data.append({'fcstTime': fcstTime})
        index = times.index(fcstTime)

        forecast_data[index].update({codeName: target_data['fcstValue']})

    weather_dic['forecast_data'] = forecast_data
    return weather_dic

