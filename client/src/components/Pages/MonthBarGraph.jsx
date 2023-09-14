/* eslint-disable react/prop-types */
import { Bar } from "react-chartjs-2";
// import { useEffect } from "react";

export default function MonthBarGraph({ betterMonth, refresh }) {
  const betterPairings = betterMonth.pairings_field;
  const labelsArray = betterPairings.map((pairing) => pairing.pairing_name);
  const payArray = betterPairings.map((pairing) => pairing.pairing_total_pay);
  const data = {
    labels: labelsArray,
    datasets: [
      {
        label: "Pairing Total Pay",
        data: payArray,
        backgroundColor: [
          // "#FF6384", // Color for month_a_pay
          // "#36A2EB", // Color for month_double_half_pay
          // "#FFCE56", // Color for month_double_time_pay
          // "#FF5733", // Color for month_holiday_pay
          // "#00FF33", // Color for month_tafb_pay
          // "#9900FF", // Color for month_int_tafb_pay
          // "#FF00FF", // Color for month_overrides_pay
          // "#FF9933", // Color for month_reserve_no_fly_pay
          "#33FFCC", // Color for month_tfp_pay
          // "#FF3300", // Color for month_time_half_pay
          // "#33CC33", // Color for month_triple_pay
          // "#66FF99", // Color for month_vacation_sick_pay
          // "#CC00CC", // Color for month_vja_pay
        ],
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        beginAtZero: true,
      },
    },
  };
  // useEffect(() => {
  //   // This effect will be triggered whenever the refresh prop changes
  //   // You can perform any necessary actions here
  //   console.log("OtherComponent has been refreshed");
  // }, [refresh]);

  return (
    <div className="mt-3">
      <h2>Pairing Totals</h2>
      <Bar data={data} options={options} />
    </div>
  );
}
