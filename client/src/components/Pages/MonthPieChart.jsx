/* eslint-disable react/prop-types */
import { Pie } from "react-chartjs-2";

export default function MonthPieChart({ betterMonth }) {
  const {
    month,
    month_a_pay,
    month_double_half_pay,
    month_double_time_pay,
    month_holiday_pay,
    month_tafb_pay,
    month_int_tafb_pay,
    month_overrides_pay,
    month_reserve_no_fly_pay,
    month_tfp_pay,
    month_time_half_pay,
    month_triple_pay,
    month_vacation_sick_pay,
    month_vja_pay,
  } = betterMonth;
  const data = {
    labels: [
      `A Pay $${month_a_pay}`,
      `Double & Half Pay $${month_double_half_pay}`,
      `Double Time $${month_double_time_pay}`,
      `Holiday Pay $${month_holiday_pay}`,
      `TAFB Pay $${month_tafb_pay}`,
      `Int. TAFB Pay $${month_int_tafb_pay}`,
      `Overrides Pay $${month_overrides_pay}`,
      `No Fly Reserve Pay $${month_reserve_no_fly_pay}`,
      `Regular TFP $${month_tfp_pay}`,
      `Overtime $${month_time_half_pay}`,
      `Triple Time $${month_triple_pay}`,
      `Vacation/Sick $${month_vacation_sick_pay}`,
      `VJA Pay $${month_vja_pay}`,
    ],
    datasets: [
      {
        data: [
          month_a_pay,
          month_double_half_pay,
          month_double_time_pay,
          month_holiday_pay,
          month_tafb_pay,
          month_int_tafb_pay,
          month_overrides_pay,
          month_reserve_no_fly_pay,
          month_tfp_pay,
          month_time_half_pay,
          month_triple_pay,
          month_vacation_sick_pay,
          month_vja_pay,
        ],
        backgroundColor: [
          "#FF6384", // Color for month_a_pay
          "#36A2EB", // Color for month_double_half_pay
          "#FFCE56", // Color for month_double_time_pay
          "#FF5733", // Color for month_holiday_pay
          "#00FF33", // Color for month_tafb_pay
          "#9900FF", // Color for month_int_tafb_pay
          "#FF00FF", // Color for month_overrides_pay
          "#FF9933", // Color for month_reserve_no_fly_pay
          "#33FFCC", // Color for month_tfp_pay
          "#FF3300", // Color for month_time_half_pay
          "#33CC33", // Color for month_triple_pay
          "#66FF99", // Color for month_vacation_sick_pay
          "#CC00CC", // Color for month_vja_pay
        ],
        hoverBackgroundColor: [
          "#FF6384",
          "#36A2EB",
          "#FFCE56",
          "#FF5733",
          "#00FF33",
          "#9900FF",
          "#FF00FF",
          "#FF9933",
          "#33FFCC",
          "#FF3300",
          "#33CC33",
          "#66FF99",
          "#CC00CC",
        ],
      },
    ],
  };
  const filteredData = {
    labels: data.labels.filter(
      (label, index) => data.datasets[0].data[index] !== 0
    ),
    datasets: [
      {
        data: data.datasets[0].data.filter((value) => value !== 0),
        backgroundColor: data.datasets[0].backgroundColor.filter(
          (_, index) => data.datasets[0].data[index] !== 0
        ),
        hoverBackgroundColor: data.datasets[0].hoverBackgroundColor.filter(
          (_, index) => data.datasets[0].data[index] !== 0
        ),
      },
    ],
  };

  const options = {
    title: {
      display: true,
      text: "Pie Chart",
    },
  };
  return (
    <div className="mt-3">
      <h4>{month} Income Distribution</h4>
      <Pie data={filteredData} options={options} />
    </div>
  );
}
