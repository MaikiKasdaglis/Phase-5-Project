/* eslint-disable react/prop-types */
import { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

const MonthBarGraph = ({ betterPairings }) => {
  console.log(`these are pairings`, betterPairings);
  const labelsArray = betterPairings.map((pairing) => pairing.pairing_name);
  console.log(`these are pairings name`, labelsArray);
  const payArray = betterPairings.map((pairing) => pairing.pairing_total_pay);
  console.log(`these are pairings pay`, payArray);
  const chartRef = useRef(null);

  useEffect(() => {
    const ctx = chartRef.current.getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: labelsArray,
        datasets: [
          {
            label: "Bar Graph",
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

export default MonthBarGraph;
