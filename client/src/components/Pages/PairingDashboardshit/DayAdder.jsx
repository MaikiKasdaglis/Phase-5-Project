/* eslint-disable react/prop-types */
import { Row, Col, Button } from "react-bootstrap";
import { useState } from "react";

import Modal from "react-bootstrap/Modal";

export default function DayAdder({ passPairing }) {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  // console.log("FROM ADDER", passPairing.pairing.days_field.length + 1);

  const postObj = {
    a_hours: 0,
    a_pay: 0,
    a_position: false,
    comments: "",
    daily_duty_hours: 0.0,
    date: `Day ${passPairing.pairing.days_field.length + 1}`,
    double_half: 0.0,
    double_half_pay: 0,
    double_half_rated: 0,
    double_time: 0.0,
    double_time_pay: 0,
    double_time_rated: 0,
    holiday: 0,
    holiday_pay: 0,
    holiday_rated: 0,
    overrides: 0,
    overrides_pay: 0,
    pairing_id: passPairing.pairing.id,
    reserve_no_fly: false,
    reserve_no_fly_holiday: 0,
    reserve_no_fly_hours: 0,
    reserve_no_fly_pay: 0,
    time_half: 0.0,
    time_half_pay: 0,
    time_half_rated: 0,
    total_credits: 0,
    total_credits_rated: 0,
    total_pay: 0,
    total_tfp: 0,
    total_tfp_pay: 0,
    triple: 0,
    triple_pay: 0,
    triple_rated: 0,
    type_of_day: "",
    vacation_sick: 0,
    vacation_sick_pay: 0,
    vja: 0,
    vja_pay: 0,
    vja_rated: 0,
  };

  function handleSubmit() {
    console.log(postObj);
    handleClose();
    fetch("/api/days", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postObj),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response error");
        }
        return response.json();
      })
      .then((data) => {
        console.log(`this is the reponse from new pairing post`, data);
      })
      .catch((error) => {
        console.log("error", error.message);
      });
  }

  return (
    <Row>
      <Col>
        <>
          <Button variant="dark" className="rounded-0" onClick={handleShow}>
            Add Day to Current Pairing
          </Button>

          <Modal show={show} onHide={handleClose} animation={false}>
            <Modal.Header closeButton>
              <Modal.Title>Modal heading</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              Woohoo, you are reading this text in a modal!
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={handleClose}>
                Close
              </Button>
              <Button variant="primary" onClick={(e) => handleSubmit(e)}>
                Add New Day
              </Button>
            </Modal.Footer>
          </Modal>
        </>
      </Col>
    </Row>
  );
}
