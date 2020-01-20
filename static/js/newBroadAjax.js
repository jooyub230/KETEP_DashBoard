function getNewBroadDB(key, url, formData) {
    console.log("newBroadAjax.js - formData = ", formData, "type = ", typeof(formData));
    var data = {};
    $.ajax({
        url: url,
        dataType:'json',
        type:'GET',
        data: {
            key: key,
            formData: formData
        },
        async: false,
        contentType: 'application/json',
        success:function(result){
            data[key] = result;
//            $.each(result, function(key, value){
//                $.each(value, function(key, value){
//                    console.log(key, value);
//                });
//            });
        },
        error:function(request,status,error){
            alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
        },
        complete : function() {
//            setPeakChart(term, peak_list, use_amt_list, term_list, chartTitle);
//            setTableContents(term, peak_list, use_amt_list, term_list);
        }
    });
    return data;
}

function ajaxPolling(key, url, param, info) {
    console.log('info = ', info);
    var API_url = 'http://112.216.18.149:8000/api/';
    if(info == '' || info == undefined || info == null){
//        var API_url = 'http://112.216.18.148:5000/api/'; // 더존테크윌
        API_url = 'http://112.216.18.148:4000/api/'; // 실제운용
    }else{
        if(info == 'room'){
            API_url = 'http://112.216.18.148:4000/api/'
            // API_url = 'http://112.216.18.148:5000/api/'; // 더존테크윌
        }
        if(info == 'ahu'){
            API_url = 'http://112.216.18.148:4000/api/'
            // API_url = 'http://112.216.18.149:3000/api/'; // 실제운용
        }
    }

    var jsonData = new Object();
    console.log(info, ' API_url = ', API_url + url);

    $.ajax({
        url: API_url + url,
        dataType:'json',
        type:'GET',
        async:false,
        data: param,
        contentType: 'application/json',
        success:function(result){
            console.log("데이터타입 = ", typeof(result));
            if(typeof(result) == 'string'){
                jsonData[key] = JSON.parse(result);
            }else {
                jsonData[key] = result;
            }
            console.log('jsonData = ', jsonData[key]);
            switch (url) {
                case 'rooms': refreshRoom(jsonData); break;
                case 'rooms/getAlarm': refreshAlarm(jsonData); break;
                default : break;
            }

        },
        error: function(status, errorMsg){
            alert(errorMsg);
        },
        timeout: 3000,
        complete: setTimeout(function() {
            ajaxPolling(key, url, param, info);
        }, 5000)
    });
}

function refreshRoom(data) {
    var setStatusCnt = 0;                           // 보일러 ON 설정 개수
    var curStatusCnt = 0;                           // 보일러 ON 상태 개수

    var target = $('#roomContainer');
    var roomList = data.roomInfo;

    if($('.room').length > 0){
        for (var i = 0 ; i < roomList.length ; i++){
            var roomNo = roomList[i].usRoomNo;          // 객실 상태 - 방번호
            var roomState = roomList[i].ucRoomState;    // 객실 상태 - 재실모드(공실:0, 예비:1, 재실:2)
            var curStatus = roomList[i].ucCurStatus;    // 객실 상태 - 보일러현재상태
            var setStatus = roomList[i].ucSetStatus;    // 객실 상태 - 보일러설정상태
                                                        // 가동(ucCurStatus:1), 가동준비(ucSetStatus:1, ucCurStatus:0), 정지(ucCurStatus:0)
            var totalStatus = roomList[i].ucTotalStatus;// 객실 상태 - 제어기상태
            var tSurf = roomList[i].fTsurf_cur;         // 객실 상태 - 바닥온도
            var tRoom = roomList[i].fTroom_cur;         // 객실 상태 - 실내온도
            var mode = roomList[i].usManHeatingMode;    // 객실 상태 - 난방모드(자동:0, 수동:1, 정지:2)

            var oneRoom = $('.room').eq(i);

            if(roomState != 0){
                if(roomState == 2){                                                             //재실
                    oneRoom.find('.panel').addClass('border-primary');
                    oneRoom.find('.panel-heading').addClass('bg-primary text-white');
                    oneRoom.find('.panel-heading > .row > div:eq(1) > span').text("재실");
                }else{                                                                          //예비
                    oneRoom.find('.panel').addClass('border-warning');
                    oneRoom.find('.panel-heading').addClass('bg-warning text-white');
                    oneRoom.find('.panel-heading > .row > div:eq(1) > span').text("예비");
                }
            }else{
                oneRoom.find('.panel').removeClass('border-primary', 'border-warning');
                oneRoom.find('.panel-heading').removeClass('bg-primary', 'bg-warning', 'text-white');
                oneRoom.find('.panel-heading > .row > div:eq(1) > span').text("공실");
            }                                                                                   //Default: 공실
//            if(curStatus == 1 && setStatus == 1){                                                               // 보일러 가동
//                curStatusCnt += 1;
//                setStatusCnt += 1;
//                oneRoom.find('.flame').attr('src', "static/img/flame-active.svg");
//                oneRoom.find('.power').attr('src', "static/img/roomStatus/power-icon-active.svg");
//            }else if(curStatus == 0 && setStatus == 1) {
//                setStatusCnt += 1;
//                oneRoom.find('.flame').attr('src', "static/img/flame-pre.svg");
//                oneRoom.find('.power').attr('src', "static/img/roomStatus/power-icon-active.svg");
//            }else{
//                oneRoom.find('.flame').attr('src', "static/img/flame.svg");
//                oneRoom.find('.power').attr('src', "static/img/roomStatus/power-icon.svg");
//            }

            if(curStatus == 1){
                if(setStatus == 1){                                                         // 보일러 가동
                    curStatusCnt += 1;
                    setStatusCnt += 1;
                    oneRoom.find('.flame').attr('src', "static/img/flame-active.svg");
                    oneRoom.find('.power').attr('src', "static/img/roomStatus/power-icon-active.svg");
                }else{                                                                      // 보일러 정지중
                    oneRoom.find('.flame').attr('src', "static/img/flame-pre.svg");
                    oneRoom.find('.power').attr('src', "static/img/roomStatus/power-icon.svg");
                }
            }else {
                if(setStatus == 1){                                                         // 보일러 가동준비중
                    setStatusCnt += 1;
                    oneRoom.find('.flame').attr('src', "static/img/flame-pre.svg");
                    oneRoom.find('.power').attr('src', "static/img/roomStatus/power-icon-active.svg");
                }else{                                                                      // 보일러 정지
                    oneRoom.find('.flame').attr('src', "static/img/flame.svg");
                    oneRoom.find('.power').attr('src', "static/img/roomStatus/power-icon.svg");
                }
            }

            if(mode != 2){
                if(mode == 0){
                    oneRoom.find('.auto').attr('src', "static/img/roomStatus/auto-dial-active.svg");
                }else{
                    oneRoom.find('.manual').attr('src', "static/img/roomStatus/manual-dial-active.svg");
                }
            }else{
                oneRoom.find('.auto').attr('src', "static/img/roomStatus/auto-dial.svg");
                oneRoom.find('.manual').attr('src', "static/img/roomStatus/manual-dial.svg");
            }

            oneRoom.find('.panel-heading > .row > div:eq(0) > span:first-child').text(roomNo);       //방번호
            oneRoom.find('.panel-footer > .row > div:eq(1) > span:first-child').text(tRoom);         //실내온도
            if(tSurf != 255){
                oneRoom.find('.panel-footer > .row > div:eq(3) > span:first-child').text(tSurf);         //바닥온도
            }else {
                oneRoom.find('.panel-footer > .row > div:eq(3) > span:first-child').text('- ');
            };

            if((totalStatus & 8).toString(2) === "0" && (totalStatus & 16).toString(2) !== "0"){
                console.log(roomNo, ' = 정상');
                oneRoom.find('.plug').attr('src', "static/img/plug-active.svg");
            }else{
                if((totalStatus & 8).toString(2) !== "0"){
                    oneRoom.find('.wifi').attr('src', "static/img/wifi-off-active.svg");
                    oneRoom.find('.panel-body .row:first-child div:last-child').css({"background-color":"#6c5ce7"});
                }else{
                    oneRoom.find('.wifi').attr('src', "static/img/wifi-off.svg");
                    oneRoom.find('.panel-body .row:first-child div:last-child').css({"background": "none !important"});
                }
                if((totalStatus & 16).toString(2) !== "0"){
                    oneRoom.find('.plug').attr('src', "static/img/plug.svg");
                }
            }
        }
        console.log('setStatusCnt = ', setStatusCnt, 'curStatusCnt = ', curStatusCnt);
        $('.boilerStat').html('<h4>난방(보일러 on) : ' + setStatusCnt + '(' + curStatusCnt + ')' + '</h4>');
    }

}

function refreshAlarm(data) {
    var alarm = data.alarm;
    if(!alarm.beChecked){
        var Time = Unix_timestamp(alarm.Time);
        var dataFilter = [Time, alarm.szContent, alarm.beChecked];
        $('#alarm .alarmInfo').each(function(index, object){
            $(this).text(dataFilter[index]);
        });

        $("#level-slider")
            .slider({
                value: alarm.Level
            });
        if(!$('#alarm').is(':visible')){
            $('#alarm').modal('show');
        }
    }
}

function getNewBroadAjax(key, url, param, info) {
    console.log('info = ', info);
    var API_url = 'http://112.216.18.149:8000/api/';
    if(info == '' || info == undefined || info == null){
//        var API_url = 'http://112.216.18.148:5000/api/'; // 더존테크윌
        API_url = 'http://112.216.18.149:8000/api/'; // 실제운용
    }else{
        if(info == 'room'){
            API_url = 'http://112.216.18.148:5000/api/'; // 더존테크윌
        }
        if(info == 'ahu'){
            API_url = 'http://112.216.18.149:3000/api/'; // 실제운용
        }
    }

    var jsonData = new Object();
    console.log(info, ' API_url = ', API_url + url);

    $.ajax({
        url: API_url + url,
        dataType:'json',
        type:'GET',
        async:false,
        data: param,
        contentType: 'application/json',
        success:function(result){
            console.log("데이터타입 = ", typeof(result));
            if(typeof(result) == 'string'){
                jsonData[key] = JSON.parse(result);
            }else {
                jsonData[key] = result;
            }
        },
        error: function(status, errorMsg){
          alert(errorMsg);
        },
        complete : function() {

        }
    });
    console.log(jsonData[key]);
    return jsonData;
}

function setParsedJson(data) {
    $.each(data, function(key, value){
        // console.log('step1-', key, ': ', value, 'length: ', Object.keys(value).length, 'type: ', typeof(value));
        $.fn.setValue(key, value);
        if(typeof(value)=='object'){
            $.each(value, function(key2, value2) {
                // console.log('step2-', key+'.'+key2, ': ', value2);
                $.fn.setValue(key+'.'+key2, value2);
                if(typeof(value2)=='object'){
                    $.each(value2, function(key3, value3) {
                        // console.log('step3-', key+'.'+key2+'.'+key3, ': ', value3);
                        $.fn.setValue(key+'.'+key2+'.'+key3, value3);
                    });
                }
            });
        }
    });
}

var alarmPolling = new function(){
    var xmlHttp     = new XMLHttpRequest();
    var finalDate   = '';
 
    // Ajax Setting
    xmlHttp.onreadystatechange = function()
    {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
        {
            // JSON 포맷으로 Parsing
            res = JSON.parse(xmlHttp.responseText);
            finalDate = res.date;
            console.log('res = ', res);
            // 채팅내용 보여주기
            alarmPolling.show(res);
 
            // 채팅내용 가져오기 [추가]
            alarmPolling.getAlarm();
        }
    }
 
    // 채팅내용 가져오기
    this.getAlarm = function()
    {
        // Ajax 통신
        xmlHttp.open("GET", 'http://112.216.18.148:5000/api/rooms/getAlarm', true);
        xmlHttp.send();

    }
 
    // 채팅내용 보여주기
    this.show = function(data)
    {
          console.log('show = ', data);
//
    }
 
    
}
 
// 페이지 로딩을 끝마치면 채팅내용 가져오기 시작 [추가]
//window.onload = function()
//{
//    alarmPolling.getAlarm();
//}

$.fn.setValue = function(key, value) {
    var $element = $('input[name="'+key+'"]');
    // setting <INPUT> value
    if ($element.length){
        if ($element.attr('type')=='number'){
            if(isNaN(value) == false && Number.isInteger(value)==false){
                value = value.toFixed(1);
            }
            $element.prop('value', value);
            $element.next().find('input[type="text"]').val(value);
        }else if ($element.attr('type')=='text'){
            if($element.parent().hasClass('date')){
                if(value!=0){
                    // 날짜 설정
                    var dateTime = Unix_timestamp(value).split(" ");
                    $element.val(dateTime[0]);
                    // 시간 설정
                    $element = $('div[name="'+key+'"]').find('div.bfh-timepicker-popover');
                    if ($element.length){
                        var hour = $.trim(dateTime[1].split(":")[0]);
                        var minute = $.trim(dateTime[1].split(":")[1]);
                        $element.prev().find('input[type="text"]').val(hour+':'+minute);
                        $element.find('td.hour').find('input[type="text"]').val(hour);
                        $element.find('td.minute').find('input[type="text"]').val(minute);
                    }else {
                        // console.log('미설정 = ', key, ' : ', value);
                    }
                }else{
                    $element.val('');
                    $element = $('div[name="'+key+'"]').find('div.bfh-timepicker-popover');
                    if ($element.length){
                        $element.prev().find('input[type="text"]').val('');
                        $element.find('td.hour').find('input[type="text"]').val('');
                        $element.find('td.minute').find('input[type="text"]').val('');
                    }else {
                        // console.log('미설정 = ', key, ' : ', value);
                    }
                }
                // console.log("키 = ", key, "날짜 = ", value);
            }else{
                console.log("키 = ", key, "값 = ", value);
                $element.val(value);
            }
        }else if ($element.attr('type')=='checkbox'){
            console.log('체크박스 = ', key, ' : ', value);
            var binNum = value.toString(2);
            binNum = pad(binNum, $element.length).split("");
            // console.log(binNum, typeof(binNum));
            $element.each(function(index){
                if(Number(binNum[index])){
                    this.checked = true;
                    var $switch = $element.closest('label.switch');
//                    console.log('className = ', $switch);
                    if($switch){
                        $element.parent().next().hide();
                        $element.parent().next().next().show();
//                        $element.closest('div').find('p').toggle();
                    }
                }else{
                    this.checked = false;
                    var $switch = $element.closest('label.switch');
//                    console.log('className = ', $switch);
                    if($switch){
                        $element.parent().next().show();
                        $element.parent().next().next().hide();
//                        $element.closest('div').find('p').toggle();
                    }
                }
            });
        }
    }else {
        // setting <SELECT> value
        $element = $('select[name="'+key+'"]');
        if ($element.length){
            $element.val(value);
        }else {
            // setting <DIV.bfh-timePicker> value
            $element = $('div[name="'+key+'"]').find('div.bfh-timepicker-popover');

            if ($element.length){
//                console.log('시간 = ', key, ' : ', value);
                if(value > 24){
                    var hour = parseInt(value/(60*60));
                    var minute = parseInt((value/60)%60);
                    $element.prev().find('input[type="text"]').val(pad(hour,2)+':'+ pad(minute,2));
                    $element.find('td.hour').find('input[type="text"]').val(pad(hour,2));
                    $element.find('td.minute').find('input[type="text"]').val(pad(minute,2));
                }else{
                    $element.prev().find('input[type="text"]').val(pad(value,2)+':00');
                    $element.find('td.hour').find('input[type="text"]').val(pad(value,2));
                    $element.find('td.minute').find('input[type="text"]').val('00');
                    $element.find('td.minute').find('input[type="text"]').attr("disabled",true);
                }
            }else {
                if(key == "SchState"){
                    console.log('미설정 = ', key, ' : ', value);
                }
            }
        }
    }
}
function Unix_timestamp(t){
    var date = new Date(t*1000);
    var year = date.getFullYear();
    var month = "0" + (date.getMonth()+1);
    var day = "0" + date.getDate();
    var hour = "0" + date.getHours();
    var minute = "0" + date.getMinutes();
    var second = "0" + date.getSeconds();
    return year + "-" + month.substr(-2) + "-" + day.substr(-2) + " " + hour.substr(-2) + ":" + minute.substr(-2) + ":" + second.substr(-2);
}
function pad(n, width) {
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join('0') + n;
}
//
function setAhuInfoChart(ahuNo, parseData){
    var $ahuInfoChart = document.getElementById("ahuInfoChart");
    var eChartObject = echarts.getInstanceByDom($ahuInfoChart);

    if(eChartObject==null || eChartObject==undefined){
        var resizeContainer = function(){
            var modalWidth = document.querySelector("#ahuGraph > div.modal-dialog").clientWidth;
            console.log('modalWidth : ', modalWidth);
            if (modalWidth != 0){
                $ahuInfoChart.style.width = modalWidth * 0.9 + 'px';
            }else{
                $ahuInfoChart.style.width = '900px';
            }
            console.log('#ahuGraph Width : ', $ahuInfoChart.style.width, '#ahuGraph Height : ', $ahuInfoChart.style.height);
        };
        resizeContainer();
        var eChart = echarts.init($ahuInfoChart);
        $(window).on('resize', function (){
            resizeContainer();
            eChart.resize();
        });
        var app = {};

        option = null;
        option = {
            title: [
                {text: '온도', padding: [5, 0]},
                {text: 'CO₂ 농도', padding: [210, 0]},
                {text: '설정상태', padding: [400, 0]}
            ],
            axisPointer: {
                link: {xAxisIndex: 'all'},
                label: {backgroundColor: '#777'}
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                },
                formatter: function (params) {
                    var tooltip = params[0].name + '<br>';
                    for(var i = 0; i < params.length; i++){
                        var co2Data = option.legend[1].data;
                        var stepData = option.legend[2].data;
                        if(stepData.includes(params[i].seriesName)){
                            var label = '';
                            switch (params[i].value) {
                                // 팬자동수동
                                case 0: label = "자동"; break;
                                case 1: label = "수동"; break;
                                // 자동팬설정
                                case 2: label = "미설정"; break;
                                case 3: label = "off"; break;
                                case 4: label = "on"; break;
                                // 수동팬설정
                                case 5: label = "미설정"; break;
                                case 6: label = "off"; break;
                                case 7: label = "on"; break;
                                // 공급팬상태
                                case 8: label = "미설정"; break;
                                case 9: label = "off"; break;
                                case 10: label = "on"; break;
                                // 댐퍼자동수동
                                case 11: label = "미설정"; break;
                                case 12: label = "자동"; break;
                                case 13: label = "수동"; break;
                            }
                            tooltip += params[i].marker + params[i].seriesName + ': ' + label + '<br>';
                        }else if(co2Data.includes(params[i].seriesName)){
                            tooltip += params[i].marker + params[i].seriesName + ': ' + params[i].value + 'ppm<br>';
                        }else{
                            tooltip += params[i].marker + params[i].seriesName + ': ' + params[i].value + '℃<br>';
                        }
                    }
                    return tooltip;
                }
            },
            legend: [
                {
                    right: 'center',
                    top: '3%',
                    data:['급기온도', '환기온도', '설정온도', '외부온도']
                }, {
                    right: 'center',
                    top: '40%',
                    data:['CO₂', '외기설정값', '외기현재값']
                }, {
                    right: 'center',
                    top: '68%',
                    data:['공급팬상태', '댐퍼자동수동', '수동팬설정', '자동팬설정', '팬자동수동']
                }
            ],
            grid: [
                {left: 50, right: 30, top: 50, bottom: '70%', containLabel: false},
                {left: 50, right: 30, top: '45%', bottom: '40%', containLabel: false},
                {left: 50, right: 30, top: '75%', bottom: 30, containLabel: false}
            ],
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            xAxis: [
                {type: 'category', gridIndex: 0, splitLine: {show: true, lineStyle:{type:'dashed'}}, data: parseData.timestamp},
                {type: 'category', gridIndex: 1, splitLine: {show: true, lineStyle:{type:'dashed'}}, data: parseData.timestamp},
                {type: 'category', gridIndex: 2, splitLine: {show: true, lineStyle:{type:'dashed'}}, data: parseData.timestamp}
            ],
            yAxis: [
                {
                    gridIndex: 0,
                    type: 'value',
                    name: '온도 (℃)',
                    nameGap: 10,
                    axisLabel: {
                        formatter: '{value}'
                    }
                }, {
                    gridIndex: 1,
                    type: 'value',
                    name: 'CO₂ (ppm)',
                    nameGap: 10,
                    axisLabel: {
                        formatter: '{value}'
                    }
                }, {
                    gridIndex: 1,
                    type: 'value',
                    name: '외기',
                    nameGap: 10,
                    axisLabel: {
                        formatter: '{value}'
                    }
                }, {
                    // type: 'category',
                    gridIndex: 2,
                    data: ['자동', '수동', '미설정', 'off', 'on', '미설정', 'off', 'on', '미설정', 'off', 'on', '미설정', '자동', '수동'],
                    type: 'value',
                    min: 0,
                    max: 13,
                    splitNumber: 14,
                    splitLine: {show: true},
                    axisLabel: {
                        interval: 0,
                        rotate: 30,
                        fontSize: 10,
                        formatter: function (value) {
                            var label = '';
                            switch (value) {
                                // 팬자동수동
                                case 0: label = "자동"; break;
                                case 1: label = "수동"; break;
                                // 자동팬설정
                                case 2: label = "미설정"; break;
                                case 3: label = "off"; break;
                                case 4: label = "on"; break;
                                // 수동팬설정
                                case 5: label = "미설정"; break;
                                case 6: label = "off"; break;
                                case 7: label = "on"; break;
                                // 공급팬상태
                                case 8: label = "미설정"; break;
                                case 9: label = "off"; break;
                                case 10: label = "on"; break;
                                // 댐퍼자동수동
                                case 11: label = "미설정"; break;
                                case 12: label = "자동"; break;
                                case 13: label = "수동"; break;
                            }
                            return label;
                        }
                    },
                    splitArea: {
                        show: true
                    }
                }
            ],
            series: [
                {
                    name:'급기온도',
                    type:'line',
                    smooth: true,
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    itemStyle: {
                        color: '#2f4554'
                    },
                    animationDelay: function (idx) {
                        return idx * 10;
                    },
                    // markPoint : {
                    //     data : [
                    //         {type : 'max', name: '설정온도'}
                    //     ]
                    // },
                    data: parseData.fData_temp_supply
                },
                {
                    name:'환기온도',
                    type:'line',
                    smooth: true,
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    itemStyle: {
                        color: '#00b894'
                    },
                    animationDelay: function (idx) {
                        return idx * 10;
                    },
                    data: parseData.fData_temp_return
                },
                {
                    name:'설정온도',
                    type:'line',
                    smooth: true,
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    itemStyle: {
                        color: '#ff5252'
                    },
                    animationDelay: function (idx) {
                        return idx * 10;
                    },
                    data: parseData.fData_hc_set_temp
                },
                {
                    name:'외부온도',
                    type:'line',
                    smooth: true,
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    itemStyle: {
                        color: 'rgba(46, 134, 222,1.0)'
                    },
                    animationDelay: function (idx) {
                        return idx * 10;
                    },
                    data: parseData.fTout
                },
                {
                    name:'CO₂',
                    type:'line',
                    smooth: true,
                    xAxisIndex: 1,
                    yAxisIndex: 1,
                    itemStyle: {
                        color: 'rgba(255, 82, 82, 1.0)'
                    },
                    animationDelay: function (idx) {
                        return idx * 10;
                    },
                    data: parseData.nPPMco2_cur
                },
                {
                    name:'외기설정값',
                    type:'line',
                    smooth: true,
                    xAxisIndex: 1,
                    yAxisIndex: 2,
                    itemStyle: {
                        color: 'rgba(64, 64, 122, 1.0)'
                    },
                    animationDelay: function (idx) {
                        return idx * 10;
                    },
                    data: parseData.fData_damper_manual_set
                },
                {
                    name:'외기현재값',
                    type:'line',
                    smooth: true,
                    xAxisIndex: 1,
                    yAxisIndex: 2,
                    itemStyle: {
                        color: 'rgba(33, 140, 116, 1.0)'
                    },
                    animationDelay: function (idx) {
                        return idx * 10;
                    },
                    data: parseData.fData_damper_outer_set
                },
                {
                    name:'팬자동수동',
                    type:'line',
                    step: 'middle',
                    xAxisIndex: 2,
                    yAxisIndex: 3,
                    data: parseData.cMode_auto_manual
                },
                {
                    name:'자동팬설정',
                    type:'line',
                    step: 'middle',
                    xAxisIndex: 2,
                    yAxisIndex: 3,
                    data: parseData.cMode_auto_mode
                },
                {
                    name:'수동팬설정',
                    type:'line',
                    step: 'middle',
                    xAxisIndex: 2,
                    yAxisIndex: 3,
                    data: parseData.cMode_manual_mode
                },
                {
                    name:'공급팬상태',
                    type:'line',
                    step: 'middle',
                    xAxisIndex: 2,
                    yAxisIndex: 3,
                    data: parseData.cState_supplay_fan
                },
                {
                    name:'댐퍼자동수동',
                    type:'line',
                    step: 'middle',
                    xAxisIndex: 2,
                    yAxisIndex: 3,
                    data: parseData.cMode_damper_auto_manual
                }
            ]
        };

        if (option && typeof option === "object") {
            eChart.setOption(option, true);
        };
        window.onresize = function() {
            <!--$('.eCharts').each(function(){-->
                <!--var id = $(this).attr('_echarts_instance_');-->
                <!--window.echarts.getInstanceById(id).resize();-->
            <!--});-->
            // alert("size variation");
            eChart.resize();
        }
    }else{
        var option = eChartObject.getOption();
        option.series[0].data = parseData.fData_temp_supply;
        option.series[1].data = parseData.fData_temp_return;
        option.series[2].data = parseData.fData_hc_set_temp;
        option.series[3].data = parseData.fTout;
        option.series[4].data = parseData.nPPMco2_cur;
        option.series[5].data = parseData.fData_damper_manual_set;
        option.series[6].data = parseData.fData_damper_outer_set;
        option.series[7].data = parseData.cMode_auto_manual;
        option.series[8].data = parseData.cMode_auto_mode;
        option.series[9].data = parseData.cMode_manual_mode;
        option.series[10].data = parseData.cState_supplay_fan;
        option.series[11].data = parseData.cMode_damper_auto_manual;
        option.xAxis[0].data = parseData.timestamp;
        option.xAxis[1].data = parseData.timestamp;
        option.xAxis[2].data = parseData.timestamp;
        eChartObject.setOption(option, true);
    }

}
function setFormData(idx){
    var startDate = $('input[name="startDate"]').val();
    var endDate = $('input[name="endDate"]').val();
    if(startDate == '' || endDate == ''){
        var today = new Date();
        var endDate = today.toISOString().slice(0,10);
        var startDate = today.setDate(today.getDate()-2);
        startDate = today.toISOString().slice(0,10);
        $('input[name="startDate"]').val(startDate);
        $('input[name="endDate"]').val(endDate);
    }
    var $time = $('select[name="time"]').val();
    var $startTime = $('.bfh-timepicker[name="startTime"]');
    var hour = $startTime.find('td.hour').find('input[type="text"]').val();
    var minute = $startTime.find('td.minute').find('input[type="text"]').val();
    var startTime = $startTime.find('div:first-child > input[type="text"]').val();
    var $endTime = $('.bfh-timepicker[name="endTime"]');
    hour = $endTime.find('td.hour').find('input[type="text"]').val();
    minute = $endTime.find('td.minute').find('input[type="text"]').val();
    var endTime = $endTime.find('div:first-child > input[type="text"]').val();
    var formData = {
            "usRoomNo": idx,
            "nZoneIdx": idx,
            "startTime": startDate + ' ' + startTime,
            "endTime": endDate + ' ' + endTime,
            "time": $time
    };
    return formData;
}