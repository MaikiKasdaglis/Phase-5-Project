import { useState, useEffect } from "react";

import {
  Container,
  Row,
  Col,
  Navbar,
  Dropdown,
  ButtonGroup,
  Button,
} from "react-bootstrap";
import useUserStore from "../../../hooks/useStore";
import DualBarGraph from "./DualBarGraph";
export default function ComparisonPage() {
  //=============STATE AND WHAT NOT
  const { user } = useUserStore();
  useEffect(() => {
    fetch(`/api/users/${user.id}`)
      .then((response) => response.json())
      .then((data) => {
        setUserYears(data?.years_field);
      });
  }, []);
  const [userYears, setUserYears] = useState([]);
  console.log(user);
  console.log("userYears blank now?", userYears);
  const [leftSelect, setLeftSelect] = useState();
  const [rightSelect, setRightSelect] = useState();

  return (
    <>
      {" "}
      <Navbar
        expand="lg"
        sticky="top"
        className="bg-body-tertiary mt-3"
        style={{ position: "relative", zIndex: "100" }}
      >
        <Container>
          {/* <Navbar.Brand href="#">Navbar</Navbar.Brand> */}
          <Col>
            <Dropdown as={ButtonGroup}>
              <Button variant="dark" className="rounded-0">
                {leftSelect ? leftSelect.year : "Select Year"}
              </Button>

              <Dropdown.Toggle
                split
                id="dropdown-split-basic"
                variant="dark"
                className="rounded-0"
              />

              <Dropdown.Menu>
                {userYears?.map((year) => (
                  <Button
                    className="dropdown-item"
                    key={year.id}
                    onClick={() => setLeftSelect(year)}
                  >
                    {year.year}
                  </Button>
                ))}
              </Dropdown.Menu>
            </Dropdown>
          </Col>
          <Col>
            <Dropdown as={ButtonGroup}>
              <Button variant="secondary" className="rounded-0">
                {rightSelect ? rightSelect.year : "Select Year"}
              </Button>

              <Dropdown.Toggle
                split
                variant="secondary"
                className="rounded-0"
                id="dropdown-split-basic"
              />

              <Dropdown.Menu>
                {userYears?.map((year) => (
                  <Button
                    className="dropdown-item"
                    key={year.id}
                    onClick={() => setRightSelect(year)}
                  >
                    {year.year}
                  </Button>
                ))}
              </Dropdown.Menu>
            </Dropdown>
          </Col>
        </Container>
      </Navbar>
      <Container>
        <Row className="justify-content-center">
          <DualBarGraph leftSelect={leftSelect} rightSelect={rightSelect} />
        </Row>
        <Row>
          <Col>search details 1</Col>
          <Col>search details 2 </Col>
        </Row>
      </Container>
    </>
  );
}
