/* eslint-disable react/prop-types */
// eslint-disable-next-line no-unused-vars
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import Accordion from "react-bootstrap/Accordion";
import DaysBarGraph from "./DaysBarGraph";

export default function PairingCard({ pairing }) {
  console.log(pairing, `from pairing card`);
  const {
    int_tafb_total,
    pairing_a_hours,
    pairing_double_half,
    pairing_double_time,
    pairing_holiday,
    pairing_overrides,
    pairing_tfp,
    pairing_time_half,
    pairing_triple,
    pairing_vja,
    reserve_block,
    tafb_total,

    pairing_vacation_sick,
    pairing_duty_hours,
  } = pairing;
  // console.log(`day_field?`, pairing.days_field);
  // console.log(`pairing`, pairing.id);
  const days = pairing.days_field;

  return (
    <Card style={{ width: "18rem" }} className="m-0 p-0">
      <DaysBarGraph days={days} />
      <Card.Body>
        <Card.Title>{`Pairing Begin: ${pairing.pairing_name}`}</Card.Title>
        <Card.Text>
          <div>
            <ul>
              {int_tafb_total ? (
                <li>TAFB International: {int_tafb_total}</li>
              ) : null}
              {tafb_total ? <li>TAFB: {tafb_total}</li> : null}
              {pairing_a_hours ? <li>A Position: {pairing_a_hours}</li> : null}
              {pairing_tfp ? <li>Total Regular TFP: {pairing_tfp}</li> : null}
              {pairing_holiday ? <li>Holiday: {pairing_holiday}</li> : null}
              {pairing_double_half ? (
                <li>Double Time & Half: {pairing_double_half}</li>
              ) : null}
              {pairing_double_time ? (
                <li>Double Time: {pairing_double_time}</li>
              ) : null}
              {pairing_overrides ? (
                <li>Total Overrides: {pairing_overrides}</li>
              ) : null}
              {pairing_time_half ? (
                <li>Time & Half: {pairing_time_half}</li>
              ) : null}
              {pairing_triple ? <li>Triple Time: {pairing_triple}</li> : null}
              {pairing_vja ? <li>V.J.A: {pairing_vja}</li> : null}
              {reserve_block ? <li>Reserve Block: True</li> : null}

              {pairing_vacation_sick ? (
                <li>pairing_vacation_sick: {pairing_vacation_sick}</li>
              ) : null}
              {pairing_duty_hours ? (
                <li> pairing_duty_hours: {pairing_duty_hours}</li>
              ) : null}
            </ul>
          </div>
        </Card.Text>
        <Accordion flush>
          {pairing.days_field.map((day) => (
            <Accordion.Item key={day.id} eventKey={day.id}>
              <Accordion.Header>{day.date}</Accordion.Header>
              <Accordion.Body>
                <div>
                  {" "}
                  <ul>
                    {day.type_of_day ? (
                      <li>day.type_of_day: {day.type_of_day}</li>
                    ) : null}
                    {day.a_hours ? <li>day.a_hours: {day.a_hours}</li> : null}
                    {day.a_position ? (
                      <li>day.a_position: {day.a_position}</li>
                    ) : null}
                    {day.double_half ? (
                      <li>day.double_half: {day.double_half}</li>
                    ) : null}
                    {day.double_time ? (
                      <li>day.double_time: {day.double_time}</li>
                    ) : null}
                    {day.holiday ? <li>day.holiday: {day.holiday}</li> : null}
                    {day.overrides ? (
                      <li>day.overrides: {day.overrides}</li>
                    ) : null}
                    {day.reserve_no_fly ? (
                      <li>day.reserve_no_fly: {day.reserve_no_fly}</li>
                    ) : null}
                    {day.time_half ? (
                      <li>day.time_half: {day.time_half}</li>
                    ) : null}
                    {day.total_tfp ? (
                      <li>day.total_tfp: {day.total_tfp}</li>
                    ) : null}
                    {day.triple ? <li>day.triple: {day.triple}</li> : null}
                    {day.vja ? <li>day.vja: {day.vja}</li> : null}
                    {day.vacation_sick ? (
                      <li>day.vacation_sick: {day.vacation_sick}</li>
                    ) : null}
                    {day.daily_duty_hours ? (
                      <li>day.daily_duty_hours: {day.daily_duty_hours}</li>
                    ) : null}
                    {day.comments ? (
                      <li>day.comments: {day.comments}</li>
                    ) : null}
                  </ul>
                </div>
              </Accordion.Body>
            </Accordion.Item>
          ))}
        </Accordion>
        {/* <Button variant="primary">Go somewhere</Button> */}
      </Card.Body>
    </Card>
  );
}
