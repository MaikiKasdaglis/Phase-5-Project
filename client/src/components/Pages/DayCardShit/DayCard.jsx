/* eslint-disable react/no-unknown-property */
/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
import React, { useState, useEffect } from "react";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import Accordion from "react-bootstrap/Accordion";
import {
  Container,
  Row,
  Col,
  Button,
  Table,
  FormControl,
  Modal,
} from "react-bootstrap";
import Figure from "react-bootstrap/Figure";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import ApositionToggle from "./ApositionToggle";

export default function DayCard({ day, passPairing }) {
  // console.log("the whold paiing", passPairing.pairing.reserve_block);
  const renderNofly = passPairing.pairing.reserve_block;
  // console.log("form daycard", day);
  // ============button state==================
  const [thisWorks, setThisWorks] = useState("dark");
  // ======================destructure day
  const [formValues, setFormValues] = useState(day);
  const {
    // ==============USER MUST BE ABLE TO EDIT=============
    //BOOLEANS
    a_position,
    reserve_no_fly,
    reserve_no_fly_holiday,
    //NOT IMPORTANT
    comments,
    type_of_day,
    //MUST ENTER
    daily_duty_hours,
    total_tfp,
    vacation_sick,
    vja,
    time_half,
    holiday,
    double_time,
    double_half,
    triple,
    //UNIQUE
    overrides,
    // ======================DAY INFO======================
    id,
    pairing_id,
    date,
    //=================HOURS/RATED CREDITS
    a_hours,
    reserve_no_fly_hours,
    holiday_rated,
    double_time_rated,
    double_half_rated,
    time_half_rated,
    triple_rated,
    vja_rated,
    //TOTALS
    total_credits,
    total_credits_rated,
    //====================PAY TOTALS
    a_pay,
    holiday_pay,
    double_time_pay,
    double_half_pay,
    overrides_pay,
    reserve_no_fly_pay,
    time_half_pay,
    total_pay,
    total_tfp_pay,
    triple_pay,
    vacation_sick_pay,
    vja_pay,
  } = formValues;
  // ================= A POSITION TOGGLE
  const [aPosition, setAPosition] = useState(a_position);
  // =====================RESERVE NO FLY TOGGLE
  const [noFly, setNoFly] = useState(reserve_no_fly);
  const [noFlyHoliday, setNoFlyHoliday] = useState(reserve_no_fly_holiday);

  const handleRadioChange = (event) => {
    const { id } = event.target;

    if (id === "radioOption1") {
      // flew
      setNoFly(false);
      setNoFlyHoliday(false);
    } else if (id === "radioOption2") {
      // no-fly
      setNoFly(true);
      setNoFlyHoliday(false);
    } else if (id === "radioOption3") {
      // no-fly holiday
      setNoFly(false);
      setNoFlyHoliday(true);
    }
  };
  // useEffect(() => {
  //   console.log("no fly =", noFly, "no fly holiday =", noFlyHoliday);
  // }, [noFly, noFlyHoliday]);

  // ==============DUTY HOURS
  const [hours, setHours] = useState(Math.floor(daily_duty_hours));
  const [minutes, setMinutes] = useState(
    Math.floor(daily_duty_hours * 60) % 60
  );

  const handleChangeHours = (e) => {
    setHours(parseInt(e.target.value));
  };

  const handleChangeMinutes = (e) => {
    setMinutes(parseInt(e.target.value));
    // console.log("mins", parseInt(e.target.value) / 60);
  };

  // Convert hours and minutes to float
  let totalHours = hours + minutes / 60;
  let formattedHours = parseFloat(totalHours.toFixed(2));
  // ===========DUTY HOURS END

  const handleChange = (e, key) => {
    if (key === "a_position") {
      setFormValues({ ...formValues, a_position: aPosition });
    } else if (key === "daily_duty_hours") {
      setFormValues({ ...formValues, daily_duty_hours: formattedHours });
    } else {
      setFormValues({ ...formValues, [key]: parseFloat(e.target.value) });
    }
    // console.log("from handle change", formValues);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    let updatedFormValues;
    noFly || noFlyHoliday
      ? (updatedFormValues = {
          //BOOLEANS
          a_position: false,
          reserve_no_fly: noFly,
          reserve_no_fly_holiday: noFlyHoliday,
          //NOT IMPORTANT
          comments: "",
          type_of_day: "",
          //MUST ENTER
          daily_duty_hours: 0,
          total_tfp: 0,
          vacation_sick: 0,
          vja: 0,
          time_half: 0,
          holiday: 0,
          double_time: 0,
          double_half: 0,
          triple: 0,
          //UNIQUE
          overrides: 0,
          // ======================DAY INFO======================
          id,
          pairing_id,
          date,
          //=================HOURS/RATED CREDITS
          a_hours: 0,
          reserve_no_fly_hours: 0,
          holiday_rated: 0,
          double_time_rated: 0,
          double_half_rated: 0,
          time_half_rated: 0,
          triple_rated: 0,
          vja_rated: 0,
          //TOTALS
          total_credits: 0,
          total_credits_rated: 0,
          //====================PAY TOTALS
          a_pay: 0,
          holiday_pay: 0,
          double_time_pay: 0,
          double_half_pay: 0,
          overrides_pay: 0,
          reserve_no_fly_pay: 0,
          time_half_pay: 0,
          total_pay: 0,
          total_tfp_pay: 0,
          triple_pay: 0,
          vacation_sick_pay: 0,
          vja_pay: 0,
        })
      : (updatedFormValues = {
          ...formValues,
          a_position: aPosition,
          daily_duty_hours: formattedHours,
          reserve_no_fly: noFly,
          reserve_no_fly_holiday: noFlyHoliday,
        });

    fetch(`/api/cascade_test/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedFormValues),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response error");
        }
        return response.json();
      })
      .then((data) => {
        // console.log("this is form data", data);
      })
      .catch((error) => {
        console.log("error", error.message);
      });
  };
  //=======MODAL AND DELETE DAY STUFF
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  function handleDelete(id) {
    // console.log("gonna delete", id);
    fetch(`/api/cascade_test/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(),
    });

    handleClose();
  }
  const number = total_pay / daily_duty_hours;
  const formNum = number >= 0 ? number.toFixed(2) : 0;
  return (
    <>
      <Col lg={4} className="mt-3">
        <Card className="m-0 p-0">
          {/* //===============MAYBE DISPLAY SHIT====================== */}
          <Accordion className="m-0 p-0">
            <Accordion.Item eventKey="0">
              <Accordion.Header>{date} Quick View </Accordion.Header>
              <Accordion.Body>
                <div
                  class="grid-container"
                  style={{ position: "sticky", top: 0 }}
                >
                  <div class="grid-item">
                    <h6>Total Pay</h6>
                    <p class="large-text">${total_pay}</p>
                  </div>
                  <div class="grid-item">
                    <h6>Total Credits</h6>
                    <p class="large-text">{total_credits_rated}</p>
                  </div>
                  <div class="grid-item">
                    <h6>Average Pay Duty Hour</h6>
                    <p class="large-text"> ${formNum}</p>
                  </div>
                  <div class="grid-item">
                    <h6>Total Overrides</h6>
                    <p class="large-text">${overrides_pay}</p>
                  </div>
                </div>
              </Accordion.Body>
            </Accordion.Item>
          </Accordion>
          .
          <Form onSubmit={handleSubmit}>
            <Card.Body>
              <Card.Title>{date}</Card.Title>
              {/* <Card.Text>
              </Card.Text> */}
            </Card.Body>
            <Container>
              <Row>
                <Col className="d-flex align-items-center">
                  {" "}
                  <Form.Check
                    className="m-3 mt-0 mb-0"
                    type="switch"
                    id="aPositionSwitch"
                    label="A Position"
                    disabled={noFly || noFlyHoliday}
                    checked={noFly || noFlyHoliday ? false : aPosition}
                    onChange={() => {
                      setAPosition(!aPosition);
                    }}
                    // onChange={(e) => {
                    //   setAPosition(!aPosition), handleChange(e, "a_position");
                    // }}
                  />
                </Col>
              </Row>
              <Row>
                {renderNofly ? (
                  <Col className="d-flex align-items-center m-3 mt-0 mb-0">
                    {" "}
                    <Form.Check
                      type="radio"
                      label="flew"
                      name="radioGroup"
                      id="radioOption1"
                      checked={!noFly && !noFlyHoliday}
                      className="m-1 mt-0 mb-0"
                      onChange={handleRadioChange}
                    />
                    <Form.Check
                      type="radio"
                      label="no-fly"
                      name="radioGroup"
                      id="radioOption2"
                      className="m-1 mt-0 mb-0"
                      onChange={handleRadioChange}
                      checked={noFly && !noFlyHoliday}
                    />
                    <Form.Check
                      type="radio"
                      label="no-fly holiday"
                      name="radioGroup"
                      id="radioOption3"
                      className="m-1 mt-0 mb-0"
                      onChange={handleRadioChange}
                      checked={!noFly && noFlyHoliday}
                    />
                  </Col>
                ) : null}
              </Row>
            </Container>

            <ListGroup className="list-group-flush">
              <ListGroup.Item>
                <InputGroup>
                  <InputGroup.Text>Daily Duty Hours</InputGroup.Text>
                  <FormControl
                    disabled={noFly || noFlyHoliday}
                    aria-label="Hours"
                    value={noFly || noFlyHoliday ? 0 : hours}
                    type="number"
                    step="1"
                    onChange={(e) => {
                      handleChangeHours(e), handleChange(e, "daily_duty_hours");
                    }}
                  />
                  <FormControl
                    disabled={noFly || noFlyHoliday}
                    aria-label="Minutes"
                    value={noFly || noFlyHoliday ? 0 : minutes}
                    type="number"
                    step="1"
                    onChange={(e) => {
                      handleChangeMinutes(e),
                        handleChange(e, "daily_duty_hours");
                    }}
                  />
                </InputGroup>

                <InputGroup>
                  <InputGroup.Text>Regular TFP</InputGroup.Text>
                  <Form.Control
                    disabled={noFly || noFlyHoliday}
                    aria-label="Cat"
                    value={noFly || noFlyHoliday ? 0 : total_tfp}
                    type="number"
                    step="0.01"
                    onChange={(e) => handleChange(e, "total_tfp")}
                    name="total_tfp"
                  />
                </InputGroup>
                <InputGroup>
                  <InputGroup.Text>Vacation/Sic</InputGroup.Text>
                  <Form.Control
                    disabled={noFly || noFlyHoliday}
                    aria-label="Cat"
                    value={noFly || noFlyHoliday ? 0 : vacation_sick}
                    type="number"
                    step="0.01"
                    onChange={(e) => handleChange(e, "vacation_sick")}
                  />
                </InputGroup>
                <InputGroup>
                  <InputGroup.Text>V.J.A</InputGroup.Text>
                  <Form.Control
                    disabled={noFly || noFlyHoliday}
                    aria-label="Cat"
                    value={noFly || noFlyHoliday ? 0 : vja}
                    type="number"
                    step="0.01"
                    onChange={(e) => handleChange(e, "vja")}
                  />
                </InputGroup>
                <InputGroup>
                  <InputGroup.Text>Overtime</InputGroup.Text>
                  <Form.Control
                    disabled={noFly || noFlyHoliday}
                    aria-label="Cat"
                    value={noFly || noFlyHoliday ? 0 : time_half}
                    type="number"
                    step="0.01"
                    onChange={(e) => handleChange(e, "time_half")}
                  />
                </InputGroup>
                <InputGroup>
                  <InputGroup.Text>Holiday</InputGroup.Text>
                  <Form.Control
                    disabled={noFly || noFlyHoliday}
                    aria-label="Cat"
                    value={noFly || noFlyHoliday ? 0 : holiday}
                    type="number"
                    step="0.01"
                    onChange={(e) => handleChange(e, "holiday")}
                  />
                </InputGroup>
                <InputGroup>
                  <InputGroup.Text>Double Time</InputGroup.Text>
                  <Form.Control
                    disabled={noFly || noFlyHoliday}
                    aria-label="Cat"
                    value={noFly || noFlyHoliday ? 0 : double_time}
                    type="number"
                    step="0.01"
                    onChange={(e) => handleChange(e, "double_time")}
                  />
                </InputGroup>
                <InputGroup>
                  <InputGroup.Text>Double & Half</InputGroup.Text>
                  <Form.Control
                    disabled={noFly || noFlyHoliday}
                    aria-label="Cat"
                    value={noFly || noFlyHoliday ? 0 : double_half}
                    type="number"
                    step="0.01"
                    onChange={(e) => handleChange(e, "double_half")}
                  />
                </InputGroup>
                <InputGroup>
                  <InputGroup.Text>Triple Time</InputGroup.Text>
                  <Form.Control
                    disabled={noFly || noFlyHoliday}
                    aria-label="Cat"
                    value={noFly || noFlyHoliday ? 0 : triple}
                    type="number"
                    step="0.01"
                    onChange={(e) => handleChange(e, "triple")}
                  />
                </InputGroup>
                <InputGroup>
                  <InputGroup.Text>Overrides</InputGroup.Text>
                  <Form.Control
                    disabled={noFly || noFlyHoliday}
                    aria-label="Cat"
                    value={noFly || noFlyHoliday ? 0 : overrides}
                    type="number"
                    step="0.01"
                    onChange={(e) => handleChange(e, "overrides")}
                  />
                </InputGroup>
              </ListGroup.Item>
            </ListGroup>

            <Card.Body>
              {/* <Card.Link href="#">Card Link</Card.Link> */}
              {/* <Card.Link href="#">Another Link</Card.Link> */}
              {/* <Button
                onMouseEnter={() => setThisWorks("danger")}
                onMouseLeave={() => setThisWorks("dark")}
                type="submit"
                className="rounded-0  m-1 mt-0 mb-0"
                variant={thisWorks}
                onClick={(e) => handleDelete(id)}
              >
                Delete
              </Button> */}
              <Button
                onMouseEnter={() => setThisWorks("danger")}
                onMouseLeave={() => setThisWorks("dark")}
                type="submit"
                className="rounded-0  m-1 mt-0 mb-0"
                variant={thisWorks}
                onClick={handleShow}
              >
                DELETE {date}
              </Button>

              <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                  {/* <Modal.Title>Modal heading</Modal.Title> */}
                </Modal.Header>
                <Modal.Body className="text-center">
                  Are you sure you want to delete {date}?
                </Modal.Body>
                <Modal.Footer>
                  <Button
                    className="rounded-0  m-1 mt-0 mb-0"
                    variant="secondary"
                    onClick={handleClose}
                  >
                    Go Back
                  </Button>
                  <Button
                    className="rounded-0  m-1 mt-0 mb-0"
                    onMouseEnter={() => setThisWorks("danger")}
                    onMouseLeave={() => setThisWorks("dark")}
                    variant={thisWorks}
                    onClick={() => handleDelete(id)}
                  >
                    Yes Delete
                  </Button>
                </Modal.Footer>
              </Modal>
              <Button
                variant="dark"
                type="submit"
                className="rounded-0 m-1 mt-0 mb-0"
              >
                Submit
              </Button>
            </Card.Body>
          </Form>
        </Card>
      </Col>
    </>
  );
}
