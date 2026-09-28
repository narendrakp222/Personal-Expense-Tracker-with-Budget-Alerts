document.addEventListener('DOMContentLoaded', () => {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.classList.add('fade');
    }, 3500);
  });
});
document.addEventListener("DOMContentLoaded", () => {

    const labelsElement = document.getElementById("chart-labels");
    const totalsElement = document.getElementById("chart-totals");

    if (labelsElement && totalsElement) {

        const labels =
            JSON.parse(labelsElement.textContent);

        const totals =
            JSON.parse(totalsElement.textContent);

        const expenseChart =
            document.getElementById("expenseChart");

        if (expenseChart) {

            new Chart(expenseChart, {
                type: "bar",

                data: {
                    labels: labels,

                    datasets: [{
                        label: "Expenses",

                        data: totals
                    }]
                },

                options: {
                    responsive: true,

                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });

        }

        const categoryChart =
            document.getElementById("categoryChart");

        if (categoryChart) {

            new Chart(categoryChart, {

                type: "doughnut",

                data: {

                    labels: labels,

                    datasets: [{
                        data: totals
                    }]
                },

                options: {
                    responsive: true
                }

            });

        }

    }

});