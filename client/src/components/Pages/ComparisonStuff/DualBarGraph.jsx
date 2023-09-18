/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
import { Bar } from "react-chartjs-2";
import {
  Container,
  Row,
  Col,
  Navbar,
  DropdownButton,
  Dropdown,
  ButtonGroup,
  Button,
} from "react-bootstrap";
import { useState, useEffect } from "react";

export default function DualBarGraph({ leftSelect, rightSelect }) {
  //============comparison category stuff
  const [display, setDisplay] = useState("month_total_pay");
  const [buttonTitle, setButtonTitle] = useState();

  useEffect(() => {
    if (display === "month_a_pay") {
      setButtonTitle("A-Position Pay");
    } else if (display === "month_double_half_pay") {
      setButtonTitle("Double & Half Pay");
    } else if (display === "month_double_time_pay") {
      setButtonTitle(" Double Time Pay");
    } else if (display === "month_holiday_pay") {
      setButtonTitle("Holiday Pay");
    } else if (display === "month_tafb_pay") {
      setButtonTitle("TAFB Pay");
    } else if (display === "month_int_tafb_pay") {
      setButtonTitle("Int. TAFB Pay");
    } else if (display === "month_overrides_pay") {
      setButtonTitle("Overrides Pay");
    } else if (display === "month_reserve_no_fly_pay") {
      setButtonTitle("Reserve No-Fly Pay");
    } else if (display === "month_tfp_pay") {
      setButtonTitle("Reg TFP Pay");
    } else if (display === "month_time_half_pay") {
      setButtonTitle("Overtime Pay");
    } else if (display === "month_total_pay") {
      setButtonTitle("Total Pay");
    } else if (display === "month_triple_pay") {
      setButtonTitle("Triple Time Pay");
    } else if (display === "month_vacation_sick_pay") {
      setButtonTitle("Vacation/Sick Pay");
    } else if (display === "month_vja_pay") {
      setButtonTitle("V.J.A Pay");
    }
  }, [display]);
  //=====================DISPLAY YEAR STUFF
  //   console.log("left year", leftSelect?.months_field);
  //   console.log("right year", rightSelect?.months_field);
  let leftData = [];
  leftSelect?.months_field.map((month) => leftData.push(month[display]));
  console.log("this is leftData", leftData, leftSelect);
  let rightData = [];
  rightSelect?.months_field.map((month) => rightData.push(month[display]));
  console.log("this is rightData", rightData, rightSelect);

  //========================GRAPH STUFF
  const year1Data = leftData;
  const year2Data = rightData;
  const labels = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  const data = {
    labels: labels,

    datasets: [
      {
        label: leftSelect?.year,
        data: year1Data,
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1,
      },
      {
        label: rightSelect?.year,
        data: year2Data,
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <>
      <div>
        <Container className="d-flex justify-content-start">
          <Dropdown as={ButtonGroup}>
            <Button className="rounded-0" variant="dark">
              {buttonTitle}
            </Button>

            <Dropdown.Toggle
              split
              className="rounded-0"
              variant="dark"
              id="dropdown-split-basic"
            />

            <Dropdown.Menu>
              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_a_pay")}
              >
                A-Pay
              </Button>
              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_double_half_pay")}
              >
                Double & Half Pay
              </Button>
              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_double_time_pay")}
              >
                Double Time Pay
              </Button>
              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_holiday_pay")}
              >
                Holiday Pay
              </Button>
              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_tafb_pay")}
              >
                TAFB Pay
              </Button>
              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_int_tafb_pay")}
              >
                Int. TAFB Pay
              </Button>
              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_overrides_pay")}
              >
                Overrides Pay
              </Button>
              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_reserve_no_fly_pay")}
              >
                Reserve No-Fly Pay
              </Button>

              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_tfp_pay")}
              >
                Reg TFP Pay
              </Button>
              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_time_half_pay")}
              >
                Overtime Pay
              </Button>
              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_total_pay")}
              >
                Total Pay
              </Button>
              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_triple_pay")}
              >
                Triple Time Pay
              </Button>
              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_vacation_sick_pay")}
              >
                Vacation/Sick Pay
              </Button>
              <Button
                className="dropdown-item"
                onClick={() => setDisplay("month_vja_pay")}
              >
                V.J.A Pay
              </Button>
            </Dropdown.Menu>
          </Dropdown>
        </Container>
        <Bar data={data} options={options} />
      </div>
    </>
  );
}
