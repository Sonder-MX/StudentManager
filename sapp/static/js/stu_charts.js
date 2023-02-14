$(function () {
    drawBar();
    drawRadar();
    drawPie();
    drawPlot();
})

// 添加文本信息
function addBarInfo(data1, data2) {
    let stud = data2[0]['data'];
    let sclas = data2[1]['data'];
    let aboveName = [];  // 高于平均分的科目
    let belowName = [];  // 低于平均分的科目
    for (let i = 0; i < data1.length; i++) {
        if (stud[i] > sclas[i]) {
            aboveName.push([data1[i], (stud[i] - sclas[i]).toFixed(1)]);
        } else {
            belowName.push([data1[i], (sclas[i] - stud[i]).toFixed(1)]);
        }
    }
    if (!aboveName.length) {
        return sname + '同学，你的所有科目的成绩均高于班级平均分，望今后的你，确立目标，树恒心与毅力，以勤奋刻苦的方式实现你的理想！';
    }
    if (!belowName.length) {
        return sname + '同学，你的成绩可能不是太理想，在下次考试的时候你应该多检查，细心一点。相信下次你会考出一个满意的成绩！';
    }
    let a = '', b = '';
    aboveName.forEach(function (value) {
        a += value[0] + '课程高出班级平均分' + value[1] + '分；';
    })
    belowName.forEach(function (value) {
        b += value[0] + '课程低于班级平均分' + value[1] + '分；';
    })
    let res = sname + '同学，你选修的' + a + b;
    res = res.substring(0, res.length - 1);
    return res + '。温故而知新，可以为师矣。预祝你在下次的考试中取得好成绩！';
}

function drawBar() {
    let option = {
        title: {
            text: '成绩柱状图',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        legend: {
            right: 'right'
        },
        grid: {
            show: true,
            top: '16%',
            left: '2%',
            right: '8%',
            bottom: '5%',
            containLabel: true
        },
        xAxis: {
            name: '科目',
            type: 'category',
            data: [],
            axisTick: {
                alignWithLabel: true
            }
        },
        yAxis: {
            name: '分数',
            type: 'value'
        },
        series: []
    };
    $.ajax({
        url: '/shome/get_exam_res',
        type: 'get',
        dataType: 'JSON',
        data: {'cn': 'bar'},
        success: function (res) {
            if (res.status) {
                option.xAxis.data = res.data['x_axis_data']
                option.series = res.data['series_data']
                let stuBarC = echarts.init(document.getElementById('stu_bar'));
                stuBarC.setOption(option);
                let tips = addBarInfo(res.data['x_axis_data'], res.data['series_data']);
                $('#bar_radar_text').text(tips);
            }
        }
    })
}

function drawRadar() {
    let option = {
        title: {
            text: sname + '的平均分 vs 班级平均分',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            right: 'right',
        },
        radar: {
            startAngle: 50,
            name: {
                textStyle: {
                    fontSize: 14,
                    color: '#2d2d2d'
                }
            },
            shape: 'circle',
            axisLine: {
                lineStyle: {
                    color: '#e3dcdc',
                    type: 'solid',
                }
            },
            indicator: []
        },
        series: {
            name: '班级平均分 vs ' + sname + '的平均分',
            type: 'radar',
            tooltip: {
                trigger: 'item'
            },
            emphasis: {
                lineStyle: {
                    width: 4
                }
            },
            data: []
        }
    };
    $.ajax({
        url: '/shome/get_exam_res',
        type: 'get',
        dataType: 'JSON',
        data: {'cn': 'radar'},
        success: function (res) {
            if (res.status) {
                option.radar.indicator = res.data['indicator_data']
                option.series.data = res.data['series_data']
                let stuPadar = echarts.init(document.getElementById('stu_radar'));
                stuPadar.setOption(option);
            }
        }
    })
}

function drawPie() {
    let option = {
        title: {
            text: '各项成绩比重',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            top: 'bottom',
            left: 'center'
        },
        series: {
            name: '成绩分布',
            type: 'pie',
            radius: ['18%', '62%'],
            center: ['48%', '50%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: 16,
                    fontWeight: 'bold'
                }
            },
            data: []
        }

    };

    $.ajax({
        url: '/shome/get_exam_res',
        type: 'get',
        dataType: 'JSON',
        data: {'cn': 'pie'},
        success: function (res) {
            if (res.status) {
                option.series.data = res.data
                let stuPieC = echarts.init(document.getElementById('stu_pie'));
                stuPieC.setOption(option);
                let minNum = 101, minName;
                res.data.forEach(function (v) {
                    if (minNum > v.value) {
                        minNum = v.value;
                        minName = v.name;
                    }
                })
                $('#pie_text').text('在你的所有的科目中 ' + minName + ' 科目的分数较低。做好查漏补缺，争取下次稳定发挥，取得理想成绩！');
            }
        }
    })
}

function drawPlot() {
    let option = {
        title: {
            text: '整体水平',
            left: '45%'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            bottom: '8%',
            right: 'right'
        },
        grid: {
            show: true,
            top: '8%',
            bottom: '5%',
        },
        toolbox: {
            show: true,
            feature: {
                magicType: {type: ['line', 'bar']},
                restore: {},
            }
        },
        xAxis: {
            name: '科目',
            type: 'category',
            boundaryGap: false,
            data: []
        },
        yAxis: {
            name: '分数',
            type: 'value',
            min: function (value) {
                return value.min - 10;
            },
        },
        series: [
            {
                name: '',
                type: 'line',
                data: [],
            },
            {
                name: '',
                type: 'line',
                data: [],
                markPoint: {
                    data: [
                        {type: 'max', name: 'Max'},
                        {type: 'min', name: 'Min'}
                    ]
                },
                markLine: {
                    data: [{type: 'average', name: 'Avg'}]
                }
            },
            {
                name: '',
                type: 'line',
                data: [],
            }
        ]
    };
    $.ajax({
        url: '/shome/get_exam_res',
        type: 'get',
        dataType: 'JSON',
        data: {'cn': 'plot'},
        success: function (res) {
            if (res.status) {
                option.xAxis.data = res.data['x_axis_data'];
                option.series[0].name = '最高分线';
                option.series[0].data = res.data['max_sc'];
                option.series[1].name = '你的成绩';
                option.series[1].data = res.data['the_stu_sc'];
                option.series[2].name = '最低分线';
                option.series[2].data = res.data['min_sc'];
                let stuPlotC = echarts.init(document.getElementById('stu_plot'));
                stuPlotC.setOption(option);
                let equalArr = [];
                let smallerArr = [];
                let scGap;
                let infoTips = '你选修的课程';
                for (let i = 0; i < res.data['x_axis_data'].length; i++) {
                    scGap = res.data['max_sc'][i] - res.data['the_stu_sc'][i];
                    if (scGap) {
                        smallerArr.push([res.data['x_axis_data'][i], scGap]);
                    } else {
                        equalArr.push(res.data['x_axis_data'][i]);
                    }
                }
                if (equalArr.length > 0) {
                    let st = '';
                    equalArr.forEach(function (value) {
                        st += value + '、';
                    });
                    st = st.substring(0, st.length - 1);
                    infoTips += st + '取得了不错的成绩哦！';
                }
                if (smallerArr.length > 0) {
                    let st = '';
                    smallerArr.forEach(function (value) {
                        st += value[0] + '科程相差班级最高分' + value[1] + '分；';
                    });
                    st = st.substring(0, st.length - 1);
                    infoTips += st;
                }
                infoTips += '。再接再厉，继续加油！';
                let firstName = sname.substring(0, 1);
                $('#plot_text').prepend("<i class=\"far fa-grin-beam\"></i> " + firstName + "同学，" + infoTips);
            }
        }
    })
}
