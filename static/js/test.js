var today = new Date();
var hour = today.getHours();
var strHour = hour.toString();
var currentUsage = [300, 280, 250, 260, 270, 300, 550, 500, 400, 390, 380, 390, 400, 500, 600, 750, 800, 700, 600, 400, 500, 600, 600, 400];
var oneDay = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'];
var nowHourIndex = oneDay.findIndex(nowHour => nowHour == strHour);
var dataJsonArray = new Array();

for(var i = 0; i < currentUsage.length; i++){
    var dataJson = new Object();
    dataJson.value = currentUsage[i];
    dataJson.itemStyle = new Object();
    if(i <= nowHourIndex){
        <!--dataJson.itemStyle.color = 'rgba(0, 210, 211,1.0)';-->
        dataJson.itemStyle.color = '#2f4554';
    } else {
        dataJson.itemStyle.color = 'rgba(99, 110, 114,0.3)';
    }
    dataJsonArray.push(dataJson);
}

var dom = document.getElementById("EchartsSample");
var myChart = echarts.init(dom);
var app = {};
option = null;
option = {
    title: {
        text: '실시간 에너지 사용량'
    },
    color: ['#2f4554'],
    <!--color: ['rgba(0, 210, 211,1.0)', 'rgba(99, 110, 114,0.3)', 'rgba(255, 107, 107,1.0)'],-->
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            crossStyle: {
                color: '#999'
            }
        },
        formatter: function (params) {
            var colorSpan = color => '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + color + '"></span>';
            let rez = '<p>' + params[0].axisValue + ':00시 기준' + '</p>';
            //console.log(params); //quite useful for debug
            <!--params.forEach(item => {-->
                <!--//console.log(item); //quite useful for debug-->
                <!--var xx = '<p>' + colorSpan(item.color) + ' ' + item.seriesName + ': ' + item.data + 'kW' + '</p>'-->
                <!--rez += xx;-->
            <!--});-->
            var xx = '<p>' + colorSpan(params[0].color) + ' ' + params[0].seriesName + ': ' + params[0].value + 'kW' + '</p>';
            xx += '<p>' + colorSpan(params[1].color) + ' ' + params[1].seriesName + ': ' + params[1].value + '℃' + '</p>';
            rez += xx;

            return rez;
        }
    },
    legend: {
      data:['실사용량', '예측사용량', '실외온도']
    },
    toolbox: {
      show: true,
      feature: {
          saveAsImage: {}
      }
    },
    xAxis: {
      type: 'category',
      data: oneDay
    },
    axisPointer: {
        value: '06',
        snap: true,
        lineStyle: {
          color: '#004E52',
          opacity: 0.5,
          width: 1
        },
        label: {
          show: true,
          backgroundColor: '#004E52'
        },
        handle: {
          show: false,
          color: '#004E52'
        }
    },
    yAxis: [
      {
          type: 'value',
          name: '전력량',
          min: 0,
          max: 800,
          interval: 100,
          axisLabel: {
            formatter: '{value} kW'
          }
      },
      {
          type: 'value',
          name: '온도',
          min: -40,
          max: 40,
          interval: 10,
          axisLabel: {
              formatter: '{value} °C'
          }
      }
    ],
    grid: {
      left: '5%',
      right: '5%',
      bottom: 40
    },
    series: [
        {
            name:'실사용량',
            type:'bar',
            smooth: true,
            data: dataJsonArray,
            color: '#1b2a49',
            markArea: {
              data: [
                [{}, {xAxis: hour}]
              ],
              itemStyle: {
                color: 'rgba(99, 110, 114, 0.2)' //회색
              }
            }
        },
        {
            name:'예측사용량',
            type:'bar',
            smooth: true,
            // color: 'rgba(99, 110, 114,0.3)',
            color: '#c9d1d3',
            barGap: '-100%'
        },
        {
            name:'실외온도',
            type:'line',
            smooth: true,
            data: [-3, -2, -1, -1, 0, 1, 1, 2, 3, 3, 4, 5, 6, 5, 3, 1, 0, -2, -3, 0, 4, 4, 3, 4],
            yAxisIndex: 1,
            // color: 'rgba(255, 107, 107,1.0)'
            color: '#00909e'
        }
    ]
};
if (option && typeof option === "object") {
    myChart.setOption(option, true);
};

var dom2 = document.getElementById("EchartsSample2");
var myChart2 = echarts.init(dom2);
var app = {};
option = null;
option = {
  title : {
      text: '에너지원별 사용량'
  },
  tooltip : {
      trigger: 'item',
      formatter: "{a} <br/>{b} : {c} ({d}%)"
  },
  legend: {
      orient: 'vertical',
      x: 'left',
      top: 30,
      data: ['가스', '전기']
  },
  series : [
      {
          name: '에너지원별',
          type: 'pie',
          radius : '75%',
          center: ['50%', '60%'],
          color: ['#1b2a49', '#00909e'],
          data:[
              {value:300, name:'가스'},
              {value:700, name:'전기'}
          ],
          itemStyle: {
              emphasis: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
          }
      }
  ]
};
if (option && typeof option === "object") {
    myChart2.setOption(option, true);
};

var dom3 = document.getElementById("EchartsSample3");
var myChart3 = echarts.init(dom3);
var app = {};
option = null;
option = {
    title : {
      text: '전력 피크'
    },
    tooltip : {
        formatter: "{a} <br/>{b} : {c}%"
    },
    series: [
        {
            name: '전력피크치',
            type: 'gauge',
            startAngle: 180,
            endAngle: 0,
            radius: '100%',
            center : ['50%', '90%'],
            axisTick: {length},
            color: ['#1b2a49', '#00909e'],
            axisLine: {
                show: true,
                lineStyle: {
                    color: [
                        [1/6, 'rgba(165, 177, 194,1.0)'],
                        [2/6, 'rgba(38, 222, 129,1.0)'],
                        [3/6, 'rgba(75, 123, 236,1.0)'],
                        [4/6, 'rgba(247, 183, 49,1.0)'],
                        [5/6, 'rgba(250, 130, 49,1.0)'],
                        [1, 'rgba(235, 59, 90,1.0)']
                    ],
//                    color: [
//                        [1/5, '#c9d1d3'],
//                        [2/5, '#4ecdc4'],
//                        [3/5, '#00909e'],
//                        [4/5, '#465881'],
//                        [1, '#1b2a49']
//                    ],
                    width: 50
                }
            },
            max: 10,
            splitNumber: 10,
            splitLine: {
              show: false
            },
            axisLabel: {
                formatter: function(value){
                    return (value % 2 == 0 ? '' : Math.ceil(value/2)-1);
                },
                textStyle: {
                    color: 'white'
                },
                padding: -15,
                fontSize: 20
            },
            pointer: {
                width:'5%',
                length: '50%',
                color: 'black'
            },
            detail: {
                show: false,
                formatter:'{value}'
            },
            data: [{
                value: 1,
//                name: '전력피크수치'
            }]
        }
    ]
};
//setInterval(function () {
//    option.series[0].data[0].value = (Math.random() * 100).toFixed(2) - 0;
//    myChart3.setOption(option, true);
//},2000);
if (option && typeof option === "object") {
    myChart3.setOption(option, true);
};



var dom4 = document.getElementById("EchartsSample4");
var myChart4 = echarts.init(dom4);
var app = {};
option = null;
option = {
    title : {
      text: '에너지 용도별 사용량'
    },
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b}: {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        x: 'left',
        y: 30,
        data:['난방','냉방']
    },
    label: {
                normal: {
                    textStyle: {
                        color: 'black'
                    }
                }
            },
            labelLine: {
                normal: {
                    lineStyle: {
                        color: 'rgba(255, 255, 255, 0.3)'
                    },
                    smooth: 0.2,
                    length: 10,
                    length2: 20
                }
            },
    series: [
        {
            name:'용도별',
            type:'pie',
            center: ['50%', '60%'],
            radius: ['40%', '75%'],
            color: ['#1b2a49', '#00909e'],
            avoidLabelOverlap: false,
            label: {
                normal: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    show: true,
                    textStyle: {
                        fontSize: '25',
                        fontWeight: 'bold'
                    }
                }
            },
            labelLine: {
                show: false
            },

            itemStyle: {
              emphasis: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            data:[
                {value:310, name:'냉방'},
                {value:550, name:'난방'}
            ].sort(function (a, b) { return a.value - b.value; }),
        }
    ]
};
if (option && typeof option === "object") {
    myChart4.setOption(option, true);
};

var dom5 = document.getElementById("EchartsSample5");
var myChart5 = echarts.init(dom5);
var app = {};
option = null;
option = {
    title: {
        text: '전월 대비 사용량'
//        subtext: '목표 사용량 vs 실제 사용량'
    },
    tooltip: {
        trigger: 'axis',
        // axisPointer: {
        //     type: 'cross',
        //     crossStyle: {
        //         color: '#999'
        //     }
        // },
        formatter: function (params) {
            var colorSpan = color => '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + color + '"></span>';
            let rez = '<p>' + params[0].axisValue + '</p>';
            //console.log(params); //quite useful for debug

            var xx = '<p>' + colorSpan(params[1].color) + ' ' + params[1].seriesName + ': ' + params[1].value + 'kWh' + '</p>';
            rez += xx;

            return rez;
        }
    },
    xAxis: {
        data: ['전월사용량', '당월사용량'],
        axisLabel: {
            inside: true,
            textStyle: {
                color: '#fff'
            }
        },
        axisTick: {
            show: false
        },
        axisLine: {
            show: false
        },
        z: 10
    },
    yAxis: {
        show: false,
        axisLine: {
            show: false
        },
        axisTick: {
            show: false
        },
        axisLabel: {
            textStyle: {
                color: '#999'
            }
        }
    },
    dataZoom: [
        {
            type: 'inside'
        }
    ],
    grid: {
      left: '5%',
      right: '5%',
      bottom: 10
    },
    series: [
        { // For shadow
            type: 'bar',
            itemStyle: {
                normal: {color: 'rgba(0,0,0,0.05)'}
            },
            barGap:'-100%',
            barCategoryGap:'40%',
            data: [500, 500],
            animation: false
        },
        {
            name: '사용량',
            type: 'bar',
            itemStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(
                        0, 0, 0, 1,
                        [
//                            {offset: 0, color: '#83bff6'},
//                            {offset: 0.5, color: '#188df0'},
//                            {offset: 1, color: '#188df0'}
                            {offset: 0, color: '#4ecdc4'},
                            {offset: 0.5, color: '#34A4AE'},
                            {offset: 1, color: '#00909e'}
                        ]
                    )
                },
                emphasis: {
                    // color: new echarts.graphic.LinearGradient(
                    //     0, 0, 0, 1,
                    //     [
                    //         {offset: 0, color: '#2378f7'},
                    //         {offset: 0.7, color: '#2378f7'},
                    //         {offset: 1, color: '#83bff6'}
                    //     ]
                    // )
                }
            },
            data: [
                {
                    value: 500,
                    itemStyle: {
                        color: '#999'
                    }
                },
                {
                    value: 300,
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(
                        0, 0, 0, 1,
                        [
                            {offset: 0, color: '#4ecdc4'},
                            {offset: 0.5, color: '#34A4AE'},
                            {offset: 1, color: '#00909e'}
                        ]
                        )
                    }
                }
            ]
        }
    ]
};
if (option && typeof option === "object") {
    myChart5.setOption(option, true);
};
// Enable data zoom when user click bar.
// var zoomSize = 6;
// myChart.on('click', function (params) {
//     console.log(dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)]);
//     myChart.dispatchAction({
//         type: 'dataZoom',
//         startValue: dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)],
//         endValue: dataAxis[Math.min(params.dataIndex + zoomSize / 2, data.length - 1)]
//     });
// });

var dom6 = document.getElementById("EchartsSample6");
var myChart6 = echarts.init(dom6);
var app = {};
option = null;
option = {
    title: {
        text: '목표 대비 사용량'
//        subtext: '목표 사용량 vs 실제 사용량'
    },
    tooltip: {
        trigger: 'axis',
        // axisPointer: {
        //     type: 'cross',
        //     crossStyle: {
        //         color: '#999'
        //     }
        // },
        formatter: function (params) {
            var colorSpan = color => '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:9px;height:9px;background-color:' + color + '"></span>';
            let rez = '<p>' + params[0].axisValue + '</p>';
            //console.log(params); //quite useful for debug

            var xx = '<p>' + colorSpan(params[1].color) + ' ' + params[1].seriesName + ': ' + params[1].value + 'kWh' + '</p>';
            rez += xx;

            return rez;
        }
    },
    xAxis: {
        data: ['목표사용량', '당월사용량'],
        axisLabel: {
            inside: true,
            textStyle: {
                color: '#fff'
            }
        },
        axisTick: {
            show: false
        },
        axisLine: {
            show: false
        },
        z: 10
    },
    yAxis: {
        show: false,
        axisLine: {
            show: false
        },
        axisTick: {
            show: false
        },
        axisLabel: {
            textStyle: {
                color: '#999'
            }
        }
    },
    dataZoom: [
        {
            type: 'inside'
        }
    ],
    grid: {
      left: '5%',
      right: '5%',
      bottom: 10
    },
    series: [
        { // For shadow
            type: 'bar',
            itemStyle: {
                normal: {color: 'rgba(0,0,0,0.05)'}
            },
            barGap:'-100%',
            barCategoryGap:'40%',
            data: [500, 500],
            animation: false
        },
        {
            name: '사용량',
            type: 'bar',
            itemStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(
                        0, 0, 0, 1,
                        [
//                            {offset: 0, color: '#83bff6'},
//                            {offset: 0.5, color: '#188df0'},
//                            {offset: 1, color: '#188df0'}
                            {offset: 0, color: '#4ecdc4'},
                            {offset: 0.5, color: '#34A4AE'},
                            {offset: 1, color: '#00909e'}
                        ]
                    )
                },
                emphasis: {
                    // color: new echarts.graphic.LinearGradient(
                    //     0, 0, 0, 1,
                    //     [
                    //         {offset: 0, color: '#2378f7'},
                    //         {offset: 0.7, color: '#2378f7'},
                    //         {offset: 1, color: '#83bff6'}
                    //     ]
                    // )
                }
            },
            data: [
                {
                    value: 500,
                    itemStyle: {
                        color: '#999'
                    }
                },
                {
                    value: 300,
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(
                        0, 0, 0, 1,
                        [
                            {offset: 0, color: '#4ecdc4'},
                            {offset: 0.5, color: '#34A4AE'},
                            {offset: 1, color: '#00909e'}
                        ]
                        )
                    }
                }
            ]
        }
    ]
};
if (option && typeof option === "object") {
    myChart6.setOption(option, true);
};

//$('.dial').knob();
//$(".range_min_max").ionRangeSlider({
//			  type: "double",
//			  min: 0,
//			  max: 100,
//			  from: 30,
//			  to: 70,
//			  max_interval: 50
//});
window.onresize = function() {
    myChart.resize();
    myChart2.resize();
    myChart3.resize();
    myChart4.resize();
    myChart5.resize();
    myChart6.resize();
}