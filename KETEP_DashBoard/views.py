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
from django.db import connection
import pymysql

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def getRoomAvrTrend(request):
    key = request.GET.get('key')
    formData = json.loads(request.GET.get('formData'))
    print(formData)
    conn = pymysql.connect(host='112.216.18.149', user='root', password='tlavmf',
                           db='ems_db_thezone', charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = ("SELECT * " +
            "FROM ( " +
                    "SELECT FROM_UNIXTIME(CurTime, '%%Y-%%m-%%d %%H:%%i') AS timestamp, " +
                            "ROUND(AVG(HeatingCnt), 1) AS HeatingCnt, " +
                            "ROUND(AVG(HeatingRoomCnt), 1) AS HeatingRoomCnt, " +
                            "ROUND(AVG(Tsurf_avg), 1) AS Tsurf_avg, " +
                            "ROUND(AVG(Troom_avg), 1) AS Troom_avg, " +
                            "ROUND(AVG(Tout), 1) AS Tout " +
                    "FROM ocean.floor_rad_stat " +
                    "WHERE CurTime >= UNIX_TIMESTAMP(%s) " +
                    "AND CurTime < UNIX_TIMESTAMP(%s) " +
                    "GROUP BY CurTime DIV %s " +
                    "ORDER BY CurTime DESC " +
                    ") TMP " +
            "ORDER BY timestamp")
    curs.execute(sql, (formData['startTime'], formData['endTime'], formData['time']))
    ahuAvrData = curs.fetchall()

    dict_obj = {}
    dict_obj[key] = ahuAvrData
    print(dict_obj[key])
    return JsonResponse(dict_obj[key], safe=False)

@csrf_exempt
def getAhuAvrTrend(request):
    key = request.GET.get('key')
    formData = json.loads(request.GET.get('formData'))

    conn = pymysql.connect(host='112.216.18.149', user='root', password='tlavmf',
                           db='ems_db_thezone', charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = ("SELECT * " +
            "FROM ( " +
                    "SELECT FROM_UNIXTIME(CurTime, '%%Y-%%m-%%d %%H:%%i') AS timestamp, " +
                            "ROUND(AVG(HCOnCnt), 1) AS HCOnCnt, " +
                            "ROUND(AVG(HCOffCnt), 1) AS HCOffCnt, " +
                            "ROUND(AVG(VentilationCnt), 1) AS VentilationCnt, " +
                            "ROUND(AVG(Tzone), 1) AS Tzone, " +
                            "ROUND(AVG(Rdamp), 1) AS Rdamp, " +
                            "ROUND(AVG(PPMco2), 1) AS PPMco2 " +
                    "FROM ocean.solbeach_stat " +
                    "WHERE CurTime >= UNIX_TIMESTAMP(%s) " +
                    "AND CurTime < UNIX_TIMESTAMP(%s) " +
                    "GROUP BY CurTime DIV %s " +
                    "ORDER BY CurTime DESC" +
                    ") TMP " +
            "ORDER BY timestamp")
    curs.execute(sql, (formData['startTime'], formData['endTime'], formData['time']))
    ahuAvrData = curs.fetchall()

    dict_obj = {}
    dict_obj[key] = ahuAvrData
    print(dict_obj[key])
    return JsonResponse(dict_obj[key], safe=False)

@csrf_exempt
def getAhuTrend(request):
    key = request.GET.get('key')
    formData = json.loads(request.GET.get('formData'))

    conn = pymysql.connect(host='112.216.18.149', user='root', password='tlavmf',
                           db='ems_db_thezone', charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = ("SELECT zone.*, env.fTout " +
            "FROM " +
                "("+
                    "SELECT timestamp, " +
                            "TEMP.cMode_auto_manual, " +
                            "TEMP.cMode_auto_mode+3 AS cMode_auto_mode, " +
                            "TEMP.cMode_manual_mode+6 AS cMode_manual_mode, " +
                            "TEMP.cState_supplay_fan+9 AS cState_supplay_fan, " +
                            "TEMP.cMode_damper_auto_manual+12 AS cMode_damper_auto_manual, " +
                            "TEMP.nPPMco2_cur, TEMP.fData_damper_manual_set, TEMP.fData_temp_supply, " +
                            "TEMP.fData_hc_set_temp, TEMP.fData_temp_return, TEMP.fData_damper_outer_set " +
                    "FROM ( " +
                            "SELECT FROM_UNIXTIME(nLastUpdateTime, '%%Y-%%m-%%d %%H:%%i') AS '" + "timestamp', " +
                                    "cMode_auto_manual, cMode_auto_mode, cMode_manual_mode, cState_supplay_fan, cMode_damper_auto_manual, " +
                                    "ROUND(AVG(nPPMco2_cur), 1) AS nPPMco2_cur, " +
                                    "ROUND(AVG(fData_damper_manual_set), 1) AS fData_damper_manual_set, " +
                                    "ROUND(AVG(fData_temp_supply), 1) AS fData_temp_supply, " +
                                    "ROUND(AVG(fData_hc_set_temp), 1) AS fData_hc_set_temp, " +
                                    "ROUND(AVG(fData_temp_return), 1) AS fData_temp_return, " +
                                    "ROUND(AVG(fData_damper_outer_set), 1) AS fData_damper_outer_set " +
                            "FROM ocean.solbeach_zone_record " +
                            "WHERE nZoneIdx = %s " +
                                "AND nLastUpdateTime >= UNIX_TIMESTAMP(%s) " +
                                "AND nLastUpdateTime < UNIX_TIMESTAMP(%s) " +
                            "GROUP BY nLastUpdateTime DIV %s " +
                            "ORDER BY nLastUpdateTime DESC " +
                            ") TEMP " +
                ") zone JOIN " +
                    "("	+
                        "SELECT FROM_UNIXTIME(nLastUpdateTime, '%%Y-%%m-%%d %%H:%%i') AS timestamp2, ROUND(AVG(fTout), 1) AS fTout " +
                        "FROM ocean.site_env_record " +
                        "WHERE nSiteIdx = 2 " +
                            "AND nLastUpdateTime >= UNIX_TIMESTAMP(%s) " +
                            "AND nLastUpdateTime < UNIX_TIMESTAMP(%s) " +
                        "GROUP BY nLastUpdateTime DIV %s " +
                        "ORDER BY nLastUpdateTime DESC " +
                    ") env ON zone.timestamp = env.timestamp2 " +
            "ORDER BY zone.timestamp")
    curs.execute(sql, (formData['nZoneIdx'], formData['startTime'], formData['endTime'], formData['time'], formData['startTime'], formData['endTime'], formData['time']))
    ahuGraphData = curs.fetchall()

    dict_obj = {}
    dict_obj[key] = ahuGraphData
    print(dict_obj[key])
    return JsonResponse(dict_obj[key], safe=False)

@csrf_exempt
def getAhuStatus(request):
    key = request.GET.get('key')
    conn = pymysql.connect(host='112.216.18.149', user='root', password='tlavmf',
                           db='ems_db_thezone', charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = ("SELECT ahu.ahu_id, ahu.ahu_name, ahu.ahu_desc, zone.* " +
           "FROM ocean.solbeach_zone AS zone, ocean.ahu_info AS ahu " +
           "WHERE zone.nZoneIdx = ahu.ahu_id " +
           "AND ahu.ahu_id IN (1, 6, 7, 15, 11, 12, 13, 14, 2, 3, 4, 5, 8, 9, 10, 18, 16, 17, 19, 20) " +
           "ORDER BY FIELD(ahu.ahu_id, 1, 6, 7, 15, 11, 12, 13, 14, 2, 3, 4, 5, 8, 9, 10, 18, 16, 17, 19, 20)")
    curs.execute(sql)
    ahuList = curs.fetchall()

    dict_obj = {}
    dict_obj[key] = ahuList
    print(dict_obj[key])
    return JsonResponse(dict_obj[key], safe=False)

# @require_POST
@csrf_exempt
def getRoomTrend(request):
    key = request.GET.get('key')
    formData = json.loads(request.GET.get('formData'))
    conn = pymysql.connect(host='112.216.18.149', user='root', password='tlavmf',
                           db='ems_db_thezone', charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = ("SELECT " +
           "FROM_UNIXTIME(TEMP.nSetLastTime, '%%Y-%%m-%%d %%H:%%i') AS '" + "timestamp', " +
           "TEMP.ucRoomState + 4 AS ucRoomState, TEMP.ucSetStatus, TEMP.ucCurStatus + 2 AS ucCurStatus, TEMP.fTset, " +
           "TEMP.fTsurf_set, TEMP.fTroom_set, TEMP.fTsurf_cur, TEMP.fTroom_cur " +
           "FROM( " +
           "SELECT " +
           "nSetLastTime, ucRoomState, ucSetStatus, ucCurStatus, " +
           "ROUND(AVG(fTset), 1) AS fTset, " +
           "ROUND(AVG(fTsurf_set), 1) AS fTsurf_set, " +
           "ROUND(AVG(fTroom_set), 1) AS fTroom_set, " +
           "ROUND(AVG(fTsurf_cur), 1) AS fTsurf_cur, " +
           "ROUND(AVG(fTroom_cur), 1) AS fTroom_cur " +
           "FROM ocean.floor_rad_room_record " +
           "WHERE usRoomNo = %s " +
           "AND nSetLastTime >= UNIX_TIMESTAMP(%s) " +
           "AND nSetLastTime < UNIX_TIMESTAMP(%s) " +
           "GROUP BY nSetLastTime DIV %s " +
           "ORDER BY nSetLastTime DESC " +
           ") TEMP " +
           "ORDER BY TEMP.nSetLastTime")
    curs.execute(sql, (formData['usRoomNo'], formData['startTime'], formData['endTime'], formData['time']))
    roomGraphData = curs.fetchall()

    dict_obj = {}
    dict_obj[key] = roomGraphData
    print(dict_obj[key])
    return JsonResponse(dict_obj[key], safe=False)

    # form_data_list = json.loads(request.POST.get('formData'))
    # print(form_data_list)
    # for field in form_data_list:
    #     form_data_dict[field["name"]] = field["value"]
    # print(form_data_dict)

    # conn = pymysql.connect(host='localhost', user='root', password='duzon',
    #                        db='ketep', charset='utf8')
    # curs = conn.cursor(pymysql.cursors.DictCursor)
    # filterArgu = '' + '%'
    # curs.execute("SELECT * FROM ocean.floor_rad_room WHERE usRoomNo LIKE '%s' ORDER BY usRoomNo DESC" % filterArgu)
    # roomList = curs.fetchall()
    #
    # dict_obj = {}
    # dict_obj['roomList'] = roomList
    # return render(request, 'room_management.html', {'dict_obj': json.dumps(dict_obj)})

def getRoomInfo(request):
    conn = pymysql.connect(host='localhost', user='root', password='duzon',
                           db='ketep', charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    filterArgu = ''+'%'
    curs.execute("SELECT * FROM ocean.floor_rad_room WHERE usRoomNo LIKE '%s' ORDER BY usRoomNo DESC" % filterArgu)
    roomList = curs.fetchall()
    dict_obj = {}
    dict_obj['roomList'] = roomList
    return render(request, 'room_management.html', {'dict_obj': json.dumps(dict_obj)})

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


# def goControl(request):
#     return render(request, 'room_management.html')
#
# def goTarget(request):
#     return render(request, 'target_management.html')
#
# def goRooms(request):
#     return render(request, 'room_test.html')
#
# def goSuperAdmin(request):
#     return render(request, 'super_admin.html')


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
