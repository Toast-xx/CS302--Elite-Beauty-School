window.addEventListener('load', function() {
    renderPieChart();
    renderBarChart();
});
function renderBarChart() {
    const chartDom = document.getElementById('barChart');
    const myChart = echarts.init(chartDom);

    const dataSets = [
        { name: 'Chart 1', data: [40, 70, 55, 90, 100], color: '#59a14f' },
        { name: 'Chart 2', data: [60, 80, 40, 75, 100], color: '#f28e2b' },
        { name: 'Chart 3', data: [30, 45, 70, 85, 100], color: '#e15759' },
        { name: 'Chart 4', data: [55, 65, 50, 95, 100], color: '#4e79a7' }
    ];

    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' },
            textStyle: { color: '#000', fontSize: 14, fontFamily: 'sans-serif' }
        },
        legend: {
            top: 'top',
            data: dataSets.map(d => d.name),
            textStyle: { color: '#000', fontSize: 14, fontFamily: 'sans-serif' }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            boundaryGap: [0, 0.01],
            axisLabel: { color: '#000', fontSize: 14, fontFamily: 'sans-serif' }
        },
        yAxis: {
            type: 'category',
            data: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5'],
            axisLabel: { color: '#000', fontSize: 14, fontFamily: 'sans-serif' }
        },
        series: dataSets.map(ds => ({
            name: ds.name,
            type: 'bar',
            data: ds.data,
            itemStyle: { color: ds.color },
            barGap: 0,
            barCategoryGap: '40%',
            label: {
                show: false,
                color: '#000',
                fontSize: 14,
                fontFamily: 'sans-serif'
            }
        }))
    };

    myChart.setOption(option);
}

function renderPieChart() {
    const data = [
        { value: 40, name: 'Product A', itemStyle: { color: '#f28e2b' } },
        { value: 25, name: 'Product B', itemStyle: { color: '#e15759' } },
        { value: 35, name: 'Product C', itemStyle: { color: '#59a14f' } }
    ];

    const chartDom = document.getElementById('pieChart');
    const myChart = echarts.init(chartDom);

    const option = {
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)',
            textStyle: { color: '#000', fontSize: 14, fontFamily: 'sans-serif' }
        },
        legend: {
            orient: 'horizontal',
            top: 'top',
            textStyle: { color: '#000', fontSize: 14, fontFamily: 'sans-serif' }
        },
        series: [
            {
                name: 'Products',
                type: 'pie',
                radius: '50%',
                data: data,
                label: {
                    color: '#000',
                    fontSize: 14,
                    fontFamily: 'sans-serif'
                },
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0,0,0,0.5)'
                    }
                }
            }
        ]
    };

    myChart.setOption(option);
}
