/* eslint-disable react/prop-types */
import { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

const DaysBarGraph = ({ days }) => {
  console.log(`from bar graph`, days);
  const labelsArray = days.map((day) => day.date);
  console.log(`labels array`, labelsArray);

  function a_calc(a_hours) {
    return a_hours * 2;
  }
  console.log("this is the array im mapping on", days);
  const aPayArray = days?.map((day) => day.a_hours);
  console.log(`a pay array`, aPayArray);

  //==============DESTRUCTURED SINGLE DAY===============
  // {
  //   a_hours,
  //   a_position,
  //   comments,
  //   daily_duty_hours,
  //   date,
  //   double_half,
  //   double_time,
  //   holiday,
  //   overrides,
  //   pairing_id,
  //   reserve_no_fly,
  //   time_half,
  //   total_tfp,
  //   triple,
  //   type_of_day,
  //   vacation_sick,
  //   vja,
  // };
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
            data: [3, 6, 9],
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
