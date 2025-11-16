const API_URL = "https://elite-emporium.onrender.com";
window.addEventListener('load', function () {
});

function dashboardRequest() {
    const start_date = document.getElementById("startdate").value;
    const end_date = document.getElementById("enddate").value;
    let campus = document.getElementById("campus-name").textContent;
    const admin=document.getElementById('superstatus');
    if(admin.checked)
    {
        const temp=document.getElementById('campus').value;
        document.getElementById('campus-name').textContent=temp;
        campus=temp;
    }
    fetch(`${API_URL}/dashboard_request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ start_date, end_date, campus })
    })
    .then(response => response.json())
    .then(data => {
        updateDashboard(data);
    })
    .catch(err => console.error("Dashboard request failed:", err));
}

function updateDashboard(data) {
    // Update numeric dashboard elements
    document.getElementById("dashboardTotal").textContent = `$${data.dashboard.total_sales.toFixed(2)}`;
    document.getElementById("dashboardCompleted").textContent = data.dashboard.orders_completed || 0;
    document.getElementById("dashboardReturn").textContent = data.dashboard.refunds || 0;
    document.getElementById("dashboardAverage").textContent = `$${data.dashboard.average_order_value.toFixed(2)}`;
    document.getElementById("dashboardTop").textContent = data.dashboard.top_product || "N/A";

    // Render charts
    renderBarChart(data.dataSetsBar || [], data.week_labels || []);
    renderPieChart(data.dataSetsPie || []);
}

function renderBarChart(dataset, categories) {
    const chartDom = document.getElementById('barChart');

    // Dispose previous chart instance if exists
    if (echarts.getInstanceByDom(chartDom)) {
        echarts.dispose(chartDom);
    }
    const myChart = echarts.init(chartDom);

    const option = {
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, textStyle: { color: '#000', fontSize: 14 } },
        legend: { top: 'top', data: dataset.map(d => d.name), textStyle: { color: '#000', fontSize: 14 } },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'value', boundaryGap: [0, 0.01], axisLabel: { color: '#000', fontSize: 14 } },
        yAxis: { type: 'category', data: categories, axisLabel: { color: '#000', fontSize: 14 } },
        series: dataset.map(ds => ({
            name: ds.name,
            type: 'bar',
            data: ds.data,
            itemStyle: { color: ds.color },
            barGap: 0,
            barCategoryGap: '40%',
            label: { show: false, color: '#000', fontSize: 14 }
        }))
    };

    myChart.setOption(option);
}

function renderPieChart(data) {
    const chartDom = document.getElementById('pieChart');

    // Dispose previous chart instance if exists
    if (echarts.getInstanceByDom(chartDom)) {
        echarts.dispose(chartDom);
    }
    const myChart = echarts.init(chartDom);

    const option = {
        tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)', textStyle: { color: '#000', fontSize: 14 } },
        legend: { orient: 'horizontal', top: 'top', textStyle: { color: '#000', fontSize: 14 } },
        series: [{
            name: 'Products',
            type: 'pie',
            radius: '50%',
            data: data,
            label: { color: '#000', fontSize: 14 },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0,0,0,0.5)'
                }
            }
        }]
    };

    myChart.setOption(option);
}
