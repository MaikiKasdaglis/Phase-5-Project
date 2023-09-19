import { useLocation } from "react-router-dom";

import { Container, Row, Col } from "react-bootstrap";
import DayCard from "../DayCardShit/DayCard";
import DayAdder from "./DayAdder";
import TafbForm from "./TafbForm";
export default function PairingDashboard() {
  const location = useLocation();
  console.log(location, "this is location");
  const passPairing = location.state.passPairing;

  console.log("Received pairing object:", passPairing.pairing);
  return (
    <>
      <Container className="mt-5">
        <Row>
          <Col lg={4}>
            <TafbForm passPairing={passPairing} />
          </Col>
          <Col lg={2}>
            <DayAdder passPairing={passPairing} />
          </Col>
          <Col lg={6}>
            <h3>{passPairing.pairing.pairing_name}</h3>
          </Col>
        </Row>
      </Container>

      <Container className="mt-4">
        <Row className="m-0 mt-0 mb-0">
          {passPairing.pairing.days_field?.map((day) => (
            <DayCard key={day.id} day={day} passPairing={passPairing} />
          ))}
        </Row>
      </Container>
    </>
  );
}
