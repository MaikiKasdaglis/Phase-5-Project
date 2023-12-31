/* eslint-disable react/prop-types */
import { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

const DaysBarGraph = ({ days }) => {
  // console.log(`from bar graph`, days);
  const labelsArray = days.map((day) => day.date);
  // console.log(`labels array`, labelsArray);
  const payArray = days.map((day) => day.total_pay);

  const chartRef = useRef(null);

  useEffect(() => {
    const ctx = chartRef.current.getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: labelsArray,
        datasets: [
          {
            label: "Day Total Pay",
            data: payArray,
            backgroundColor: "rgba(75, 192, 192, 0.6)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }, []);

  return <canvas ref={chartRef} />;
};

export default DaysBarGraph;
