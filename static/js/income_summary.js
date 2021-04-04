const ctx = document.getElementById("myChart").getContext("2d");
const ctx2 = document.getElementById("myChart2").getContext("2d");

const loadIncomeChart = (data, labels) => {
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Income Summary For Last 6 Months (Source Wise)",
      },
    },
  });
};

const loadIncomeSummaryChart = (labels, data) => {
  new Chart(ctx2, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Total Amount",
          data: data,
          backgroundColor: "rgba(255, 99, 132, 0.6)",
          borderColor: "rgba(255, 99, 132, 0.6)",
          borderWidth: 5,
          fill: 1,
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
      title: {
        display: true,
        text: "Income Summary For Last 6 Months",
      },
    },
  });
};

const getChartData = () => {
  fetch("/income/income-summary")
    .then((res) => res.json())
    .then((data) => {
      let labels = Object.keys(data.income_summary);
      let expense_data = Object.values(data.income_summary);
      loadIncomeChart(expense_data, labels);
    });

  fetch("/income/monthly-income")
    .then((res) => res.json())
    .then((data) => {
      let income_summary_data = Object.entries(data.income_summary);
      console.log(income_summary_data);
      let chart_labels = income_summary_data.map((item) => item[1].month);
      let chart_data = income_summary_data.map((item) => item[1].amount);
      loadIncomeSummaryChart(chart_labels, chart_data);
    });
};

document.onload = getChartData();
