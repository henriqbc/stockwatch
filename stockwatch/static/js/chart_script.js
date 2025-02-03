document.addEventListener("DOMContentLoaded", function () {
    var ctx = document.getElementById("stockChart").getContext("2d");

    var chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: timestamps,
            datasets: [
                {
                    label: "Stock Price",
                    data: prices,
                    borderColor: "yellow",
                    backgroundColor: "rgba(255, 255, 0, 0.2)",
                    fill: false
                },
                {
                    label: "Upper Tunnel Bound",
                    data: timestamps.map(() => upperTunnelBound),
                    borderColor: "lightgray",
                    borderDash: [10, 5],
                    fill: false
                },
                {
                    label: "Lower Tunnel Bound",
                    data: timestamps.map(() => lowerTunnelBound),
                    borderColor: "lightgray",
                    borderDash: [10, 5],
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: "Time" } },
                y: { title: { display: true, text: "Price" } }
            }
        }
    });
});
