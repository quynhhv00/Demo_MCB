let myChart;
const maxLabels = 10; // Số nhãn trên trục x
let startingValue = 0; // Giá trị bắt đầu cho trục x

function updateChart() {
    fetch('/get_data1')
        .then(response => response.json())
        .then(data => {
            const temperatures = data.map(item => item.temperature).reverse(); // Đảo ngược dữ liệu
            const humidities = data.map(item => item.humidity).reverse();
            const lights = data.map(item => item.light / 10).reverse(); // Chia giá trị ánh sáng cho 10 và đảo ngược

            // Tạo nhãn cho trục x
            const hourLabels = Array.from({ length: maxLabels }, (_, i) => (startingValue + i) % 24) // Đảo ngược nhãn

            // Cập nhật biểu đồ
            if (myChart) {
                myChart.data.labels = hourLabels;
                myChart.data.datasets[0].data = temperatures.slice(-maxLabels);
                myChart.data.datasets[1].data = humidities.slice(-maxLabels);
                myChart.data.datasets[2].data = lights.slice(-maxLabels);
                myChart.update();
            } else {
                const ctx = document.getElementById('myChart').getContext('2d');
                myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: hourLabels,
                        datasets: [{
                            label: 'Temperature',
                            data: temperatures.slice(-maxLabels),
                            borderColor: 'rgba(255, 99, 132, 1)',
                            fill: false
                        }, {
                            label: 'Humidity',
                            data: humidities.slice(-maxLabels),
                            borderColor: 'rgba(54, 162, 235, 1)',
                            fill: false
                        }, {
                            label: 'Light',
                            data: lights.slice(-maxLabels),
                            borderColor: 'rgba(255, 206, 86, 1)',
                            fill: false
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            }

            // Tăng giá trị bắt đầu sau mỗi lần cập nhật
            startingValue = (startingValue + 1) % 24; // Đảm bảo giá trị quay lại 0 sau 23
        });
}
updateChart();
// Gọi hàm cập nhật biểu đồ mỗi 10 giây
setInterval(updateChart, 10000);
