/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
// eslint-disable-next-line no-unused-vars
import Card from "react-bootstrap/Card";
import Accordion from "react-bootstrap/Accordion";
import DaysBarGraph from "./DaysBarGraph";
import { Link } from "react-router-dom";
import { useState } from "react";
import ListGroup from "react-bootstrap/ListGroup";
import ReserveBlockToggle from "./ReserveBlockToggle";

export default function PairingCard({ pairing }) {
  const [passPairing, setPassPairing] = useState({ pairing });
  // console.log("form state", passPairing);
  // console.log(pairing, `from pairing card`);
  const {
    pairing_name,
    id,
    // #===============Reserve Stuff
    reserve_block,
    pairing_guarantee_hours,
    pairing_guarantee_hours_worked_rated,

    // #=============TAFB
    tafb_total,
    tafb_pay,

    int_tafb_total,
    int_tafb_pay,

    // #================TOTALS===================

    // #================TFP LYFE
    pairing_tfp,
    pairing_tfp_pay,
    // #================ VACATION/SICK LYFE
    pairing_vacation_sick,
    pairing_vacation_sick_pay,
    // #================VJA LYFE
    pairing_vj,
    pairing_vja_rate,
    pairing_vja_pay,
    // #================ HOLIDAY LYFE
    pairing_holiday,
    pairing_holiday_rated,
    pairing_holiday_pay,
    // #================ TIME_HALF
    pairing_time_half,
    pairing_time_half_rated,
    pairing_time_half_pay,
    // #================ DOUBLE TIME LYFE
    pairing_double_time,
    pairing_double_time_rated,
    pairing_double_time_pay,
    // #================ DOUBLE & HALF LYFE
    pairing_double_half,
    pairing_double_half_rated,
    pairing_double_half_pay,
    // #================ TRIPLE LYFE
    pairing_triple,
    pairing_triple_rated,
    pairing_triple_pay,
    // #================ OVERRIDES LYFE
    pairing_overrides,
    pairing_overrides_pay,
    // #================ A-POSITION LYFE
    pairing_a_hours,
    pairing_a_pay,
    // #============Totals
    pairing_total_credits,
    pairing_total_credits_rated,
    pairing_total_pay,
    // #========New additions=======
    pairing_duty_hours,
    pairing_reserve_no_fly_hours,
    pairing_reserve_no_fly_pay,
  } = pairing;
  // console.log(`day_field?`, pairing.days_field);
  // console.log(`pairing`, pairing.id);
  const days = pairing.days_field;

  return (
    <Card style={{ width: "18rem" }} className="m-0 p-0">
      <ReserveBlockToggle
        diff_reserve_block={reserve_block}
        id={id}
        pairing={pairing}
      />
      <DaysBarGraph days={days} />
      <Link
        className="btn btn-dark rounded-0"
        onClick={() => console.log(`this is the pairing i'm clicking`, pairing)}
        to="pairing_dashboard"
        state={{ passPairing: passPairing }}
      >
        Go To Pairing Dashboard
      </Link>
      <Card.Body className="m-0 p-1">
        {/* <Card.Title>{`${pairing_name} Totals:`}</Card.Title> */}
        <Card.Text>
          <Accordion flush>
            <Accordion.Item eventKey="0">
              <Accordion.Header>
                {<h5>{pairing_name} Totals</h5>}
              </Accordion.Header>
              <Accordion.Body>
                <ListGroup>
                  {" "}
                  {reserve_block ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      Reserve Block: True
                    </ListGroup.Item>
                  ) : null}
                  {tafb_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      TAFB Pay: ${tafb_pay}
                    </ListGroup.Item>
                  ) : null}
                  {int_tafb_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      Int. TAFB Pay: ${int_tafb_pay}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_tfp_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      Reg TFP: ${pairing_tfp_pay}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_vacation_sick_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      Vacation/Sick Pay: ${pairing_vacation_sick_pay}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_vja_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      VJA Pay: ${pairing_vja_pay}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_holiday_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      Holiday Pay: ${pairing_holiday_pay}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_time_half_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      Overtime Pay: ${pairing_time_half_pay}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_double_time_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      Double Time Pay: ${pairing_double_time_pay}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_double_half_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      Double & Half Pay: ${pairing_double_half_pay}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_triple_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      Triple Time Pay: ${pairing_triple_pay}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_overrides_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      Overried Pay: ${pairing_overrides_pay}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_a_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      A Pay: ${pairing_a_pay}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_reserve_no_fly_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      Reserve No Fly Pay: ${pairing_reserve_no_fly_pay}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_total_pay ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      Total Pay: ${pairing_total_pay}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_total_credits_rated ? (
                    <ListGroup.Item
                      action
                      variant="primary"
                      className="m-0 rounded-0"
                    >
                      Total Credits (rated): {pairing_total_credits_rated}
                    </ListGroup.Item>
                  ) : null}
                </ListGroup>
              </Accordion.Body>
            </Accordion.Item>
          </Accordion>
        </Card.Text>
        <Accordion flush>
          {pairing.days_field.map((day) => (
            <Accordion.Item key={day.id} eventKey={day.id}>
              <Accordion.Header>{day.date} Totals</Accordion.Header>
              <Accordion.Body>
                <ListGroup>
                  {" "}
                  {day.total_tfp_pay ? (
                    <ListGroup.Item
                      action
                      variant="light"
                      className="m-0 rounded-0"
                    >
                      Reg TFP: ${day.total_tfp_pay.toFixed(2)}
                    </ListGroup.Item>
                  ) : null}
                  {pairing_vacation_sick_pay ? (
                    <ListGroup.Item
                      action
                      variant="light"
                      className="m-0 rounded-0"
                    >
                      Vacation/Sick Pay: ${day.vacation_sick_pay}
                    </ListGroup.Item>
                  ) : null}
                  {day.vja_pay ? (
                    <ListGroup.Item
                      action
                      variant="light"
                      className="m-0 rounded-0"
                    >
                      VJA Pay: ${day.vja_pay}
                    </ListGroup.Item>
                  ) : null}
                  {day.holiday_pay ? (
                    <ListGroup.Item
                      action
                      variant="light"
                      className="m-0 rounded-0"
                    >
                      Holiday Pay: ${day.holiday_pay}
                    </ListGroup.Item>
                  ) : null}
                  {day.time_half_pay ? (
                    <ListGroup.Item
                      action
                      variant="light"
                      className="m-0 rounded-0"
                    >
                      Overtime Pay: ${day.time_half_pay}
                    </ListGroup.Item>
                  ) : null}
                  {day.double_time_pay ? (
                    <ListGroup.Item
                      action
                      variant="light"
                      className="m-0 rounded-0"
                    >
                      Double Time Pay: ${day.double_time_pay}
                    </ListGroup.Item>
                  ) : null}
                  {day.double_half_pay ? (
                    <ListGroup.Item
                      action
                      variant="light"
                      className="m-0 rounded-0"
                    >
                      Double & Half Pay: ${day.double_half_pay}
                    </ListGroup.Item>
                  ) : null}
                  {day.triple_pay ? (
                    <ListGroup.Item
                      action
                      variant="light"
                      className="m-0 rounded-0"
                    >
                      Triple Time Pay: ${day.triple_pay}
                    </ListGroup.Item>
                  ) : null}
                  {day.overrides_pay ? (
                    <ListGroup.Item
                      action
                      variant="light"
                      className="m-0 rounded-0"
                    >
                      Overried Pay: ${day.overrides_pay}
                    </ListGroup.Item>
                  ) : null}
                  {day.a_pay ? (
                    <ListGroup.Item
                      action
                      variant="light"
                      className="m-0 rounded-0"
                    >
                      A Pay: ${day.a_pay}
                    </ListGroup.Item>
                  ) : null}
                  {day.reserve_no_fly_pay ? (
                    <ListGroup.Item
                      action
                      variant="light"
                      className="m-0 rounded-0"
                    >
                      Reserve No Fly Pay: ${day.reserve_no_fly_pay}
                    </ListGroup.Item>
                  ) : null}
                  {day.total_pay ? (
                    <ListGroup.Item
                      action
                      variant="light"
                      className="m-0 rounded-0"
                    >
                      Total Pay: ${day.total_pay}
                    </ListGroup.Item>
                  ) : null}
                  {day.total_credits_rated ? (
                    <ListGroup.Item
                      action
                      variant="light"
                      className="m-0 rounded-0"
                    >
                      Total Credits (rated): {day.total_credits_rated}
                    </ListGroup.Item>
                  ) : null}
                </ListGroup>
              </Accordion.Body>
            </Accordion.Item>
          ))}
        </Accordion>
      </Card.Body>
    </Card>
  );
}
