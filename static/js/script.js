document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       AUTO-HIDE ALERTS
       ===================================================== */

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach((alert) => {

        setTimeout(() => {
            alert.classList.add("fade");
        }, 3500);

    });


    /* =====================================================
       DASHBOARD CHARTS
       ===================================================== */

    const labelsElement = document.getElementById("chart-labels");
    const totalsElement = document.getElementById("chart-totals");

    if (!labelsElement || !totalsElement || typeof Chart === "undefined") {
        return;
    }

    const labels = JSON.parse(labelsElement.textContent);
    const totals = JSON.parse(totalsElement.textContent);


    /* =====================================================
       MONTHLY EXPENSE CHART
       ===================================================== */

    const expenseCanvas = document.getElementById("expenseChart");

    if (expenseCanvas) {

        new Chart(expenseCanvas, {

            type: "bar",

            data: {
                labels: labels,

                datasets: [
                    {
                        label: "Expenses",
                        data: totals,

                        backgroundColor: "rgba(109, 93, 252, 0.75)",
                        borderColor: "#6d5dfc",
                        borderWidth: 1,

                        borderRadius: 8,
                        borderSkipped: false
                    }
                ]
            },

            options: {

                responsive: true,
                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false
                    },

                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return " Rs. " + context.parsed.y;
                            }
                        }
                    }
                },

                scales: {

                    x: {
                        grid: {
                            display: false
                        },

                        ticks: {
                            color: "#94a3b8",
                            font: {
                                size: 11
                            }
                        }
                    },

                    y: {

                        beginAtZero: true,

                        grid: {
                            color: "#eef2f7"
                        },

                        ticks: {
                            color: "#94a3b8",
                            font: {
                                size: 11
                            },

                            callback: function (value) {
                                return "Rs. " + value;
                            }
                        }
                    }
                }
            }

        });

    }


    /* =====================================================
       CATEGORY DISTRIBUTION
       ===================================================== */

    const categoryCanvas = document.getElementById("categoryChart");

    if (categoryCanvas) {

        new Chart(categoryCanvas, {

            type: "doughnut",

            data: {

                labels: labels,

                datasets: [
                    {
                        data: totals,

                        backgroundColor: [
                            "#6d5dfc",
                            "#818cf8",
                            "#60a5fa",
                            "#38bdf8",
                            "#a78bfa",
                            "#c084fc",
                            "#6366f1",
                            "#4f46e5"
                        ],

                        borderWidth: 0,

                        hoverOffset: 8
                    }
                ]
            },

            options: {

                responsive: true,
                maintainAspectRatio: false,

                cutout: "68%",

                plugins: {

                    legend: {
                        position: "bottom",

                        labels: {
                            usePointStyle: true,
                            pointStyle: "circle",

                            padding: 18,

                            color: "#64748b",

                            font: {
                                size: 11
                            }
                        }
                    },

                    tooltip: {
                        callbacks: {
                            label: function (context) {

                                return (
                                    " " +
                                    context.label +
                                    ": Rs. " +
                                    context.parsed
                                );

                            }
                        }
                    }
                }
            }

        });

    }

});