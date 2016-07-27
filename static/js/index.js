NProgress.start();
setTimeout(function() { NProgress.done(); $('.fade').removeClass('out'); }, 1000);

$(function () {
    $.get('/api/charts', function (data) {
        var chartDatas = data.faceRecognitionCounts;
        var timesX = _.uniq(_.pluck(chartDatas, 'time'));

        var failSumList = [];
        var successSumList = [];
        _.each(timesX, function(data) {
            var someData = _.where(chartDatas, {'time':data});            
            var failList = _.pluck(someData, 'fail');
            var successList = _.pluck(someData, 'success');

            var failSum = _.reduce(failList, function(memo, num){ return memo + num; }, 0);
            var successSum = _.reduce(successList, function(memo, num){ return memo + num; }, 0);

            failSumList.push(failSum);
            successSumList.push(successSum);
        });


        console.log(timesX)
        console.log(failSumList)
        console.log(successSumList)


        $('.charts').highcharts({
            chart: {
                type: 'line'
            },
            title: {
                text: '人脸识别统计图'
            },
            subtitle: {
                text: '识别次数折线图'
            },
            xAxis: {
                categories: timesX
            },
            yAxis: {
                title: {
                    text: '识别次数(次)'
                }
            },
            tooltip: {
                enabled: false,
                formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+this.x +': '+ this.y +'°C';
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: false
                }
            },
            series: [{
                name: '成功',
                color: '#58d68d',
                data: successSumList
            }, {
                name: '失败',
                color: '#ec7063',
                data: failSumList
            }]
        });

    });
});             
