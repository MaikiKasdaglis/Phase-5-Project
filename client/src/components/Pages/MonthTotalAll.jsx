/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
import Accordion from "react-bootstrap/Accordion";
import Table from "react-bootstrap/Table";
import { Col, Row, Container, Button, Modal, Form } from "react-bootstrap";
import useUserStore from "../../hooks/useStore";

function MonthTotalAll({ betterMonth }) {
  // console.log("from accordian", betterMonth);
  const { user } = useUserStore();
  const {
    month,
    month_a_hours,
    month_a_pay,
    month_double_half,
    month_double_half_pay,
    month_double_half_rated,
    month_double_time,
    month_double_time_pay,
    month_double_time_rated,
    month_duty_hours,
    month_guarantee_hours,
    month_guarantee_hours_worked_rated,
    month_holiday,
    month_holiday_pay,
    month_holiday_rated,
    month_int_tafb_pay,
    month_int_tafb_total,
    month_overrides,
    month_overrides_pay,
    month_reserve_no_fly_hours,
    month_reserve_no_fly_pay,
    month_tafb_pay,
    month_tafb_total,
    month_tfp,
    month_tfp_pay,
    month_time_half,
    month_time_half_pay,
    month_time_half_rated,
    month_total_credits,
    month_total_credits_rated,
    month_total_pay,
    month_triple,
    month_triple_pay,
    month_triple_rated,
    month_vacation_sick,
    month_vacation_sick_pay,
    month_vja,
    month_vja_pay,
    month_vja_rated,
    year,
  } = betterMonth;
  const test = month_total_credits.toFixed(2);

  return (
    <Accordion flush className="mt-2 p-0">
      <Accordion.Item eventKey="0">
        <Accordion.Header>
          {month} {year} Totals:
        </Accordion.Header>
        <Accordion.Body>
          <Row>
            {month_total_credits > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={5}>ALL CREDITS TOTALS</th>
                    </tr>
                    <tr>
                      <th>Credits</th>
                      <th>Rated</th>
                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_total_credits}</td>
                      <td>{month_total_credits_rated}</td>
                      <td>${month_total_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}
            {month_a_hours > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={2}>A-Position</th>
                    </tr>
                    <tr>
                      <th>Credits</th>

                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_a_hours}</td>

                      <td>${month_a_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}
            {month_reserve_no_fly_hours > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={2}>Reserve No Fly</th>
                    </tr>
                    <tr>
                      <th>Credits</th>

                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_reserve_no_fly_hours}</td>

                      <td>${month_reserve_no_fly_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}
            {month_overrides > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={2}>Overrides</th>
                    </tr>
                    <tr>
                      <th>Total</th>

                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_overrides}</td>

                      <td>${month_overrides_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}
            {month_tafb_total > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={2}>TAFB</th>
                    </tr>
                    <tr>
                      <th>Hours</th>

                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_tafb_total}</td>

                      <td>${month_tafb_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}
            {month_int_tafb_total > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={2}>International TAFB</th>
                    </tr>
                    <tr>
                      <th>Hours</th>
                      {/* <th>Rate</th> */}
                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_int_tafb_total}</td>
                      {/* <td>${user.a_postion_pay} x Credit</td> */}
                      <td>${month_int_tafb_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}
            {month_tfp > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={5}>Regular TFP</th>
                    </tr>
                    <tr>
                      <th>Credits</th>
                      <th>Rated</th>
                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_tfp}</td>
                      <td>{month_tfp}</td>
                      <td>${month_tfp_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}
            {month_vacation_sick > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={5}>Vacation/Sick Pay</th>
                    </tr>
                    <tr>
                      <th>Credits</th>
                      <th>Rated</th>
                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_vacation_sick}</td>
                      <td>{month_vacation_sick}</td>
                      <td>${month_vacation_sick_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}
            {month_time_half > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={5}>Overtime</th>
                    </tr>
                    <tr>
                      <th>Credits</th>
                      <th>Rated</th>
                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_time_half}</td>
                      <td>{month_time_half_rated}</td>
                      <td>${month_time_half_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}
            {month_vja > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={5}>V.J.A</th>
                    </tr>
                    <tr>
                      <th>Credits</th>
                      <th>Rated</th>
                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_vja}</td>
                      <td>{month_vja_rated}</td>
                      <td>${month_vja_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}
            {month_holiday > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={5}>Holiday</th>
                    </tr>
                    <tr>
                      <th>Credits</th>
                      <th>Rated</th>
                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_holiday}</td>
                      <td>{month_holiday_rated}</td>
                      <td>${month_holiday_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}

            {month_double_time > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={5}>Double Time</th>
                    </tr>
                    <tr>
                      <th>Credits</th>
                      <th>Rated</th>
                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_double_time}</td>
                      <td>{month_double_time_rated}</td>
                      <td>${month_double_time_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}
            {month_double_half > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={5}>Double & Half</th>
                    </tr>
                    <tr>
                      <th>Credits</th>
                      <th>Rated</th>
                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_double_half}</td>
                      <td>{month_double_half_rated}</td>
                      <td>${month_double_half_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}
            {month_triple > 0 ? (
              <Col lg={3}>
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th colSpan={5}>Triple Time</th>
                    </tr>
                    <tr>
                      <th>Credits</th>
                      <th>Rated</th>
                      <th>Pay</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{month_triple}</td>
                      <td>{month_triple_rated}</td>
                      <td>${month_triple_pay}</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            ) : null}
          </Row>
        </Accordion.Body>
      </Accordion.Item>
    </Accordion>
  );
}

export default MonthTotalAll;
