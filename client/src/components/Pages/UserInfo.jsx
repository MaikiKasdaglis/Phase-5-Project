/* eslint-disable no-unused-vars */
import useUserStore from "../../hooks/useStore";
import { useState } from "react";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Row from "react-bootstrap/Row";
import { Container } from "react-bootstrap";

export default function UserInfo() {
  const { user, updateUser } = useUserStore();
  const strippedUser = user;
  delete strippedUser.years_field;
  const {
    a_postion_pay,
    email,
    id,
    international_per_diem_pay,
    override_pay,
    per_diem_pay,
    tfp_pay,
    user_role,
    _password_hash,
    username,
  } = user;

  const [formValues, setFormValues] = useState({
    a_postion_pay: a_postion_pay,
    email: email,
    international_per_diem_pay: international_per_diem_pay,
    override_pay: override_pay,
    per_diem_pay: per_diem_pay,
    tfp_pay: tfp_pay,
    user_role: user_role,
    password_hash: _password_hash,
    username: username,
  });
  // console.log(user);
  //============SWITCH STUFF
  const [isSwitchOn, setIsSwitchOn] = useState(false);

  const handleChange = (e, key) => {
    if (typeof e.target.value === "number") {
      setFormValues({ ...formValues, [key]: parseFloat(e.target.value) });
    } else if (key === _password_hash) {
      setFormValues({ ...formValues, password_hash: e.target.value });
    } else {
      setFormValues({ ...formValues, [key]: e.target.value });
    }
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("from submit", formValues);
    fetch(`/api/users/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      // body: JSON.stringify({
      //   a_postion_pay: 2,
      //   password_hash: "321",
      //   email: "email@email.com",
      //   international_per_diem_pay: 2.85,
      //   override_pay: 5,
      //   per_diem_pay: 2.35,
      //   tfp_pay: 27.91,
      //   user_role: "flight_attendant",
      //   username: "McKenzey Brooke Simper",
      // }),
      body: JSON.stringify({ ...formValues }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response error");
        }
        return response.json();
      })
      .then((data) => {
        console.log("this is form data", data);
        updateUser(data);
      })
      .catch((error) => {
        console.log("error", error.message);
      });
  };

  const handleSwitch = (e) => {
    // console.log(e.target.checked);
    setIsSwitchOn(e.target.checked);
  };

  return (
    <>
      <Container className="mt-5">
        {/* <Col lg={4}> */}
        <Form onSubmit={handleSubmit}>
          <Row className="d-flex justify-content-center">
            <Col lg={4}>
              <InputGroup className="mb-1">
                <InputGroup.Text>Username</InputGroup.Text>
                <Form.Control
                  disabled={!isSwitchOn}
                  aria-label="username"
                  value={formValues.username}
                  type="text"
                  onChange={(e) => handleChange(e, "username")}
                  name="username"
                />
              </InputGroup>
              <InputGroup className="mb-1">
                <InputGroup.Text>Password</InputGroup.Text>
                <Form.Control
                  disabled={!isSwitchOn}
                  aria-label="password_hash"
                  value={formValues.password_hash}
                  type="password"
                  onChange={(e) => handleChange(e, "password_hash")}
                  name="password_hash"
                />
              </InputGroup>
              <InputGroup className="mb-1">
                <InputGroup.Text>Email Address</InputGroup.Text>
                <Form.Control
                  disabled={!isSwitchOn}
                  aria-label="email"
                  value={formValues.email}
                  type="text"
                  onChange={(e) => handleChange(e, "email")}
                  name="email"
                />
              </InputGroup>
            </Col>
            <Col lg={4}>
              <InputGroup className="mb-1">
                <InputGroup.Text>Regular TFP</InputGroup.Text>
                <Form.Control
                  disabled={!isSwitchOn}
                  aria-label="tfp_pay"
                  value={formValues.tfp_pay}
                  type="number"
                  step="0.01"
                  onChange={(e) => handleChange(e, "tfp_pay")}
                  name="tfp_pay"
                />
              </InputGroup>
              <InputGroup className="mb-1">
                <InputGroup.Text>Override Pay</InputGroup.Text>
                <Form.Control
                  disabled={!isSwitchOn}
                  aria-label="override_pay"
                  value={formValues.override_pay}
                  type="number"
                  step="0.01"
                  onChange={(e) => handleChange(e, "override_pay")}
                  name="override_pay"
                />
              </InputGroup>
              <InputGroup className="mb-1">
                <InputGroup.Text>A-Position Pay</InputGroup.Text>
                <Form.Control
                  disabled={!isSwitchOn}
                  aria-label="a_postion_pay"
                  value={formValues.a_postion_pay}
                  type="number"
                  step="0.01"
                  onChange={(e) => handleChange(e, "a_postion_pay")}
                  name="a_postion_pay"
                />
              </InputGroup>
              <InputGroup className="mb-1">
                <InputGroup.Text>Per Diem Rate</InputGroup.Text>
                <Form.Control
                  disabled={!isSwitchOn}
                  aria-label="per_diem_pay"
                  value={formValues.per_diem_pay}
                  type="number"
                  step="0.01"
                  onChange={(e) => handleChange(e, "per_diem_pay")}
                  name="per_diem_pay"
                />
              </InputGroup>
              <InputGroup className="mb-1">
                <InputGroup.Text>Int. Per Diem Rate</InputGroup.Text>
                <Form.Control
                  disabled={!isSwitchOn}
                  aria-label="international_per_diem_pay"
                  value={formValues.international_per_diem_pay}
                  type="number"
                  step="0.01"
                  onChange={(e) =>
                    handleChange(e, "international_per_diem_pay")
                  }
                  name="international_per_diem_pay"
                />
              </InputGroup>
            </Col>
          </Row>
          <div className="d-flex justify-content-center align-items-center">
            <Form.Label className="mt-3 m-1" htmlFor="custom-switch">
              Toggle to Edit
            </Form.Label>
            <Form.Check
              type="switch"
              id="custom-switch"
              className="mt-3 m-1"
              onChange={handleSwitch}
            />

            <Button
              style={{ width: "30%" }}
              variant="dark"
              className="rounded-0 mt-3 "
              type="submit"
              disabled={!isSwitchOn}
            >
              Submit
            </Button>
          </div>
        </Form>{" "}
      </Container>
    </>
  );
}
