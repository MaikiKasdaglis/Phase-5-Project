/* eslint-disable no-unused-vars */
import { useEffect, useState } from "react";
import { Col, Row, Container, Button, Modal, Form } from "react-bootstrap";
import useUserStore from "../../hooks/useStore";
import Carousel from "react-bootstrap/Carousel";
import PairingCard from "./PairingCard";
import Table from "react-bootstrap/Table";
import Dropdown from "react-bootstrap/Dropdown";
import ProgressBar from "react-bootstrap/ProgressBar";
import MonthPieChart from "./MonthPieChart";
import MonthBarGraph from "./MonthBarGraph";
export default function Dashboard() {
  //   const today = new Date();
  //   const start = today.getMonth() + 1;

  //================ZUSTAND STATE STUFF=================
  const { user } = useUserStore();
  //================sloppy shit
  const [usersYears, setUsersYears] = useState([]);
  const [monthId, setMonthId] = useState(0);
  const [usersMonths, setUsersMonths] = useState([]);
  const [displayYear, setDisplayYear] = useState();
  const [selectedMonthId, setSelectedMonthId] = useState(null);
  // console.log(monthId);
  //=============MODAL STUFF======================
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const [yearObj, setYearObj] = useState({
    user_id: user.id,
    year: 0,
    year_a_hours: 0,
    year_a_pay: 0,
    year_double_half: 0,
    year_double_half_pay: 0,
    year_double_half_rated: 0,
    year_double_time: 0,
    year_double_time_pay: 0,
    year_double_time_rated: 0,
    year_duty_hours: 0,
    year_holiday: 0,
    year_holiday_pay: 0,
    year_holiday_rated: 0,
    year_int_tafb_pay: 0,
    year_int_tafb_total: 0,
    year_overrides: 0,
    year_overrides_pay: 0,
    year_tafb_pay: 0,
    year_tafb_total: 0,
    year_tfp: 0,
    year_tfp_pay: 0,
    year_time_half: 0,
    year_time_half_pay: 0,
    year_time_half_rated: 0,
    year_total_credits: 0,
    year_total_credits_rated: 0,
    year_total_pay: 0,
    year_triple: 0,
    year_triple_pay: 0,
    year_triple_rated: 0,
    year_vacation_sick: 0,
    year_vacation_sick_pay: 0,
    year_vja: 0,
    year_vja_pay: 0,
    year_vja_rated: 0,
  });
  const handleEdit = (e) => {
    e.preventDefault();
    handleClose();
    console.log("form submitting", yearObj);
    fetch("/api/years", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(yearObj),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response error");
        }
        return response.json();
      })
      .then((data) => {
        console.log("response data, prob the year?", data);

        // Add the new dog to the userDogs array
        setUsersYears([...usersYears, data]);

        // Reset the dogObj state to clear the input fields
        setYearObj({
          user_id: user.id,
          year: 0,
          year_a_hours: 0,
          year_a_pay: 0,
          year_double_half: 0,
          year_double_half_pay: 0,
          year_double_half_rated: 0,
          year_double_time: 0,
          year_double_time_pay: 0,
          year_double_time_rated: 0,
          year_duty_hours: 0,
          year_holiday: 0,
          year_holiday_pay: 0,
          year_holiday_rated: 0,
          year_int_tafb_pay: 0,
          year_int_tafb_total: 0,
          year_overrides: 0,
          year_overrides_pay: 0,
          year_tafb_pay: 0,
          year_tafb_total: 0,
          year_tfp: 0,
          year_tfp_pay: 0,
          year_time_half: 0,
          year_time_half_pay: 0,
          year_time_half_rated: 0,
          year_total_credits: 0,
          year_total_credits_rated: 0,
          year_total_pay: 0,
          year_triple: 0,
          year_triple_pay: 0,
          year_triple_rated: 0,
          year_vacation_sick: 0,
          year_vacation_sick_pay: 0,
          year_vja: 0,
          year_vja_pay: 0,
          year_vja_rated: 0,
        });
      })
      .catch((error) => {
        console.log("error", error.message);
      });
  };
  //=============CAROUSEL STUFF======================
  const [index, setIndex] = useState(0);
  const handleSelect = (selectedIndex) => {
    setIndex(selectedIndex);
  };

  useEffect(() => {
    fetch(`/api/users/${user.id}`)
      .then((response) => response.json())
      .then((data) => {
        setUsersYears(data.years_field);
      });
  }, []);

  // console.log(usersMonths);
  const displayMonth = usersMonths.filter((month) => month.id === monthId);
  // console.log(displayMonth);
  const betterMonth = displayMonth[0];
  const betterPairings = betterMonth?.pairings_field;
  // console.log("works?", betterPairings);
  const guarantee_hours = displayMonth[0]?.month_guarantee_hours;
  const guarantee_hours_worked =
    displayMonth[0]?.month_guarantee_hours_worked_rated;

  return (
    <>
      {" "}
      <Container>
        <Row className="mt-3 d-flex ">
          <Col xs="auto" className="mt-1">
            <h4>Selected Year:</h4>
          </Col>
          <Col xs="auto">
            <Dropdown>
              <Dropdown.Toggle variant="dark" id="dropdown-basic">
                {displayYear ? displayYear.year : "Select Year"}
              </Dropdown.Toggle>

              <Dropdown.Menu>
                {usersYears.map((year) => (
                  <Button
                    className="dropdown-item"
                    key={year.id}
                    onClick={(e) => {
                      setUsersMonths(year.months_field), setDisplayYear(year);
                    }}
                  >
                    {year.year}
                  </Button>
                ))}
                <Dropdown.Divider />
                <>
                  <Button className="dropdown-item" onClick={handleShow}>
                    Add Year
                  </Button>

                  <Modal show={show} onHide={handleClose} animation={false}>
                    <Modal.Header closeButton>
                      <Modal.Title>Create Year </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                      <Form onSubmit={handleEdit}>
                        <Form.Group controlId="exampleForm.ControlInput1">
                          {/* <Form.Label>Year</Form.Label> */}
                          <Form.Control
                            type="number"
                            placeholder="Enter year you wish to create..."
                            onChange={(e) =>
                              setYearObj({ ...yearObj, year: e.target.value })
                            }
                            // You can add additional attributes like min and max to limit the year range.
                            min="1900"
                            max="2099"
                          />
                        </Form.Group>
                      </Form>
                    </Modal.Body>
                    <Modal.Footer>
                      <Button variant="secondary" onClick={handleClose}>
                        Close
                      </Button>
                      <Button variant="dark" onClick={handleEdit}>
                        Save Changes
                      </Button>
                    </Modal.Footer>
                  </Modal>
                </>
                {/* <Dropdown.Item href="#action/3.4">Separated link</Dropdown.Item> */}
              </Dropdown.Menu>
            </Dropdown>
          </Col>
        </Row>
        <Row className="mt-3  d-flex flex-nowrap overflow-auto">
          {usersMonths.map((month) => (
            <Col key={month.id} className="px-0 px-1">
              <Button
                variant={month.id === selectedMonthId ? "custom" : "dark"}
                style={{
                  borderRadius: "0",
                  background: month.id === selectedMonthId ? "#a9d262" : "",
                  color: month.id === selectedMonthId ? "white !important" : "",
                }}
                key={month.id}
                onClick={() => {
                  setSelectedMonthId(month.id), setMonthId(month.id);
                }}
                className={`w-100 mb-2 ${
                  month.id === selectedMonthId ? "text-white" : ""
                }`}
              >
                {month.month}
              </Button>
            </Col>
          ))}
        </Row>
      </Container>
      <Container>
        {/* this container has bot the carosel and the graphs in it */}
        <Row className="mt-5">
          <Col lg={4}>
            {displayMonth[0]?.pairings_field.length > 0 ? (
              <Carousel className="custom-carousel" interval={null}>
                {displayMonth[0]?.pairings_field.map((pairing) => (
                  <Carousel.Item key={pairing.id}>
                    <div className="centered-card">
                      <PairingCard pairing={pairing} />
                    </div>
                  </Carousel.Item>
                ))}
              </Carousel>
            ) : null}
          </Col>
          <Col lg={8} className="d-flex">
            <Container className="border mx-auto text-center">
              <Row>
                <Container className="m-0 p-0">
                  {" "}
                  {guarantee_hours > 0 ? (
                    <ProgressBar
                      now={(guarantee_hours / guarantee_hours) * 100}
                      label={`${guarantee_hours} Guarantee Hours This Month`}
                      style={{ borderRadius: 0 }}
                      className="border rounded-0"
                    />
                  ) : null}
                  {guarantee_hours_worked > 0 ? (
                    <ProgressBar
                      animated
                      now={(guarantee_hours_worked / guarantee_hours) * 100}
                      label={`${guarantee_hours_worked} Guarantee Worked`}
                      style={{ borderRadius: 0 }}
                      className="border rounded-0"
                    />
                  ) : null}
                </Container>
              </Row>
              <Row className="justify-content-center">
                <Col lg={6}>
                  {betterMonth ? (
                    <MonthPieChart betterMonth={betterMonth} />
                  ) : null}
                </Col>
                <Col lg={6}>
                  {betterMonth ? (
                    <MonthBarGraph
                      betterPairings={betterPairings}
                      betterMonth={betterMonth}
                    />
                  ) : null}
                  <Button className="mt-5 ">Add Pairing</Button>
                </Col>
              </Row>
            </Container>
          </Col>
        </Row>
      </Container>
    </>
  );
}
