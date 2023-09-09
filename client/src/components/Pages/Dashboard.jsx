/* eslint-disable no-unused-vars */
import { useEffect, useState } from "react";
import { Col, Row, Container, Nav, Button } from "react-bootstrap";
import useUserStore from "../../hooks/useStore";
import Carousel from "react-bootstrap/Carousel";
import PairingCard from "./PairingCard";
import Table from "react-bootstrap/Table";
import Dropdown from "react-bootstrap/Dropdown";
import DayCard from "./DayCard";

export default function Dashboard() {
  //   const today = new Date();
  //   const start = today.getMonth() + 1;
  const [usersYears, setUsersYears] = useState([]);
  const [monthId, setMonthId] = useState(0);
  const [usersMonths, setUsersMonths] = useState([]);
  // const [displayMonth, setDisplayMonth] = useState();
  const { user } = useUserStore();
  //for carousel
  const [index, setIndex] = useState(0);
  const handleSelect = (selectedIndex) => {
    setIndex(selectedIndex);
  };
  //   console.log("this it the month", month);

  useEffect(() => {
    fetch(`/api/users/${user.id}`)
      .then((response) => response.json())
      .then((data) => {
        // console.log(`this is the whold user object`, data);
        setUsersYears(data.years_field);
      });
  }, []);
  // console.log(`these are userYears`, usersYears);
  const displayMonth = usersMonths.filter((month) => month.id === monthId);
  // console.log(`this should be the month i click on`, displayMonth);

  return (
    <>
      {" "}
      <Container>
        <Row className="mt-3 border ">
          <Col xs="auto">
            <Dropdown>
              <Dropdown.Toggle variant="dark" id="dropdown-basic">
                Select Year
              </Dropdown.Toggle>

              <Dropdown.Menu>
                {usersYears.map((year) => (
                  <Button
                    className="dropdown-item"
                    key={year.id}
                    onClick={(e) => setUsersMonths(year.months_field)}
                  >
                    {year.year}
                  </Button>
                ))}
              </Dropdown.Menu>
            </Dropdown>
          </Col>
        </Row>
        <Row className="mt-3 border d-flex flex-nowrap overflow-auto ">
          {usersMonths.map((month) => (
            <Col key={month.id} className="px-0 px-1 ">
              <Button
                variant="dark"
                key={month.id}
                onClick={() => setMonthId(month.id)}
                className="w-100 mb-2 mt-2"
              >
                {month.month}
              </Button>
            </Col>
          ))}
        </Row>
      </Container>
      <Container>
        <Row className="mt-5">
          <Col lg={4}>
            {displayMonth[0]?.pairings_field.length > 0 ? (
              <Carousel className=" custom-carousel" interval={null}>
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
              {" "}
              <Table
                striped
                bordered
                hover
                style={{ border: "2px solid black" }}
              >
                <thead>
                  <tr>
                    <th>Catagory</th>
                    <th>Credits</th>
                    <th>Rate</th>
                    <th>Total</th>
                    <th>Pay</th>
                  </tr>
                </thead>
                {/* guarantee_hours month: "03" month_a_hours month_double_half
                month_double_time month_holiday month_int_tafb_total
                month_overrides month_tafb_total month_tfp month_time_half
                month_triple month_vja */}
                {/* {<h1>Hello {displayMonth[0].guarantee_hours}</h1>} */}
                <tbody>
                  {displayMonth[0]?.guarantee_hours ? (
                    <tr>
                      <td>Guarantee Hours</td>
                      <td>{displayMonth[0].guarantee_hours}</td>
                      <td>1</td>
                      <td>{displayMonth[0].guarantee_hours * 1}</td>
                      <td>
                        $
                        {(
                          user.tfp_pay *
                          (displayMonth[0].guarantee_hours * 1)
                        ).toFixed(2)}
                      </td>
                    </tr>
                  ) : null}
                  <tr>
                    <td>1</td>
                    <td>Mark</td>
                    <td>Otto</td>
                    <td>@mdo</td>
                    <td>@mdo</td>
                  </tr>
                  <tr>
                    <td>2</td>
                    <td>Jacob</td>
                    <td>Thornton</td>
                    <td>@fat</td>
                    <td>@mdo</td>
                  </tr>
                  <tr>
                    <td>3</td>
                    <td>Larry the Bird</td>
                    {/* <td colSpan={2}>Larry the Bird</td> */}
                    <td>@twitter</td>
                    <td>@mdo</td>
                    <td>@mdo</td>
                  </tr>
                </tbody>
                <tfoot style={{ border: "2px solid black" }}>
                  <tr>
                    <th>Catagory</th>
                    <th>Credits</th>
                    <th>Rate</th>
                    <th>Total</th>
                    <th>Pay</th>
                  </tr>
                </tfoot>
              </Table>
              <DayCard />
            </Container>
          </Col>
        </Row>
      </Container>
    </>
  );
}
