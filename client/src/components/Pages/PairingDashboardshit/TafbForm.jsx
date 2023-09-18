/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
import React, { useState, useEffect } from "react";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import {
  Container,
  Row,
  Col,
  Button,
  Table,
  FormControl,
} from "react-bootstrap";
import Figure from "react-bootstrap/Figure";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";

export default function TafbForm({ passPairing }) {
  //=============ISOLATE MY PAIRING
  const updatedObject = { ...passPairing.pairing };
  delete updatedObject.days_field;
  const [formValues, setFormValues] = useState(updatedObject);
  //   ========DESTRUCTURE
  const {
    id,
    int_tafb_pay,
    int_tafb_total,
    month_id,
    pairing_a_hours,
    pairing_a_pay,
    pairing_double_half,
    pairing_double_half_pay,
    pairing_double_half_rated,
    pairing_double_time,
    pairing_double_time_pay,
    pairing_double_time_rated,
    pairing_duty_hours,
    pairing_guarantee_hours,
    pairing_guarantee_hours_worked_rated,
    pairing_holiday,
    pairing_holiday_pay,
    pairing_holiday_rated,
    pairing_name,
    pairing_overrides,
    pairing_overrides_pay,
    pairing_reserve_no_fly_hours,
    pairing_reserve_no_fly_pay,
    pairing_tfp,
    pairing_tfp_pay,
    pairing_time_half,
    pairing_time_half_pay,
    pairing_time_half_rated,
    pairing_total_credits,
    pairing_total_credits_rated,
    pairing_total_pay,
    pairing_triple,
    pairing_triple_pay,
    pairing_triple_rated,
    pairing_vacation_sick,
    pairing_vacation_sick_pay,
    pairing_vja,
    pairing_vja_pay,
    pairing_vja_rated,
    reserve_block,
    tafb_pay,
    tafb_total,
  } = formValues;

  //   ===============REGULAR TAFB STATE==================
  const [hours, setHours] = useState(Math.floor(tafb_total));
  const [minutes, setMinutes] = useState(Math.floor(tafb_total * 60) % 60);

  const handleChangeHours = (e) => {
    setHours(parseInt(e.target.value));
  };
  const handleChangeMinutes = (e) => {
    setMinutes(parseInt(e.target.value));
  };

  // Convert hours and minutes to float
  let totalHours = hours + minutes / 60;
  let formattedHours = parseFloat(totalHours.toFixed(2));

  //   ===============INTERNATIONAL TAFB STATE==================
  const [intHours, setIntHours] = useState(Math.floor(int_tafb_total));
  const [intMinutes, setIntMinutes] = useState(
    Math.floor(int_tafb_total * 60) % 60
  );
  const handleChangeIntHours = (e) => {
    setIntHours(parseInt(e.target.value));
  };
  const handleChangeIntMinutes = (e) => {
    setIntMinutes(parseInt(e.target.value));
  };
  // Convert hours and minutes to float INTERNATIONAL
  let intTotalHours = intHours + intMinutes / 60;
  let intFormattedHours = parseFloat(intTotalHours.toFixed(2));

  const handleChange = (e, key) => {
    setFormValues({
      ...formValues,
      tafb_total: formattedHours,
      int_tafb_total: intFormattedHours,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const weirdPatchObj = {
      ...formValues,
      tafb_total: formattedHours,
      int_tafb_total: intFormattedHours,
    };

    fetch(`/api/pairings/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(weirdPatchObj),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response error");
        }
        return response.json();
      })
      .then((data) => {
        console.log("this is form data", data);
      })
      .catch((error) => {
        console.log("error", error.message);
      });
  };
  return (
    <>
      <Container>
        <Col>
          <ListGroup>
            <ListGroup.Item>
              <InputGroup>
                <InputGroup.Text>TAFB Hours/Mins</InputGroup.Text>
                <FormControl
                  aria-label="Hours"
                  value={hours}
                  type="number"
                  step="1"
                  onChange={(e) => {
                    handleChangeHours(e), handleChange(e, "tafb_total");
                  }}
                />
                <FormControl
                  aria-label="Minutes"
                  value={minutes}
                  type="number"
                  step="1"
                  onChange={(e) => {
                    handleChangeMinutes(e), handleChange(e, "tafb_total");
                  }}
                />
              </InputGroup>
            </ListGroup.Item>
            <ListGroup.Item>
              <InputGroup>
                <InputGroup.Text>Int. TAFB Hours/Mins</InputGroup.Text>
                <FormControl
                  aria-label="IntHours"
                  value={intHours}
                  type="number"
                  step="1"
                  onChange={(e) => {
                    handleChangeIntHours(e), handleChange(e, "int_tafb_total");
                  }}
                />
                <FormControl
                  aria-label="IndMinutes"
                  value={intMinutes}
                  type="number"
                  step="1"
                  onChange={(e) => {
                    handleChangeIntMinutes(e),
                      handleChange(e, "int_tafb_total");
                  }}
                />
              </InputGroup>
            </ListGroup.Item>
            <Button
              variant="dark"
              className="rounded-0"
              type="submit"
              onClick={handleSubmit}
            >
              Submit
            </Button>
          </ListGroup>
        </Col>
      </Container>
    </>
  );
}
