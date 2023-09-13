import { useState } from "react";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Row from "react-bootstrap/Row";
import useUserStore from "../../hooks/useStore";

export default function Signup() {
  // username
  // user_role
  // email
  // tfp_pay
  // per_diem_pay
  // international_per_diem_pay
  // override_pay
  // _password_hash

  const [validated, setValidated] = useState(false);
  const [signupObj, setSignupObj] = useState({
    username: "",
    _password_hash: "",
    email: "",
    user_role: "",
    tfp_pay: 0,
    per_diem_pay: 0,
    international_per_diem_pay: 0,
    override_pay: 0,
  });
  //new shit for email
  const [email, setEmail] = useState("");
  const [isValid, setIsValid] = useState(true);
  const handleEmailChange = (event) => {
    const emailValue = event.target.value;
    const isValidEmail = /\S+@\S+\.\S+/.test(emailValue); // Basic email format validation
    setSignupObj({ ...signupObj, email: emailValue });
    setIsValid(isValidEmail);
    setEmail(emailValue);
  };
  const { updateUser } = useUserStore();

  const handleSubmit = (event) => {
    const form = event.currentTarget;
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
      //   console.log("this is my obj", signupObj);
      fetch("/api/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(signupObj),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response error");
          }
          return response.json();
        })
        .then((data) => {
          updateUser(data);
        })
        .catch((error) => {
          console.log("error", error.message);
        });
    }

    setValidated(true);
  };
  return (
    <Form noValidate validated={validated} onSubmit={handleSubmit}>
      <Row className="mb-3">
        <Form.Group as={Col} md="3" controlId="validationCustom01">
          <Form.Label>Username</Form.Label>
          <Form.Control
            required
            type="text"
            placeholder="Enter Username"
            onChange={(e) =>
              setSignupObj({ ...signupObj, username: e.target.value })
            }
          />
          <Form.Control.Feedback>Great Name!</Form.Control.Feedback>
          <Form.Control.Feedback type="invalid">
            Please choose a username.
          </Form.Control.Feedback>
        </Form.Group>
        <Form.Group as={Col} md="3" controlId="validationPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            required
            type="password"
            placeholder="Enter Password"
            onChange={(e) =>
              setSignupObj({ ...signupObj, _password_hash: e.target.value })
            }
          />
          <Form.Control.Feedback>Strong password!</Form.Control.Feedback>
          <Form.Control.Feedback type="invalid">
            Please enter a password.
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group as={Col} md="3" controlId="validationRole">
          <Form.Label>Users Role</Form.Label>
          <Form.Control
            required
            as="select"
            onChange={(e) =>
              setSignupObj({ ...signupObj, user_role: e.target.value })
            }
          >
            {" "}
            <option value="">Choose Role...</option>
            <option value="flight_attendant">Flight Attendant</option>
            <option value="captian" disabled>
              Captian
            </option>
            <option value="first_officer" disabled>
              First Officer
            </option>
            <option value="ground_ops" disabled>
              Ground Operations
            </option>
          </Form.Control>

          <Form.Control.Feedback>
            Thats literally the best role!
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group as={Col} md="3" controlId="validationCustomUsername">
          <Form.Label>Email Address</Form.Label>
          <InputGroup hasValidation>
            <Form.Control
              type="email" // Use type="email" for email input
              placeholder="Enter Valid Email"
              value={email}
              onChange={handleEmailChange}
              isInvalid={!isValid}
              required
            />
            <Form.Control.Feedback type="valid">
              Looks good. Your feelings, and your email are valid.
            </Form.Control.Feedback>
            <Form.Control.Feedback type="invalid">
              Please enter a valid email address.
            </Form.Control.Feedback>
          </InputGroup>
        </Form.Group>
      </Row>

      <Row className="mb-3">
        <Form.Group as={Col} md="2" controlId="validationCustom03">
          <Form.Label>TFP Rate</Form.Label>
          <Form.Control
            type="number"
            step="0.01"
            placeholder="Millions?"
            required
            onChange={(e) =>
              setSignupObj({ ...signupObj, tfp_pay: e.target.value })
            }
          />
          <Form.Control.Feedback>
            Bro, thats hella money! 💰
          </Form.Control.Feedback>
          <Form.Control.Feedback type="invalid">
            Please provide your base TFP rate.
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group as={Col} md="2" controlId="validationCustom04">
          <Form.Label>Per Diem Rate</Form.Label>
          <Form.Control
            type="number"
            step="0.01"
            placeholder="Millions?"
            required
            onChange={(e) =>
              setSignupObj({ ...signupObj, per_diem_pay: e.target.value })
            }
          />
          <Form.Control.Feedback>
            Bro, thats hella money! 💰
          </Form.Control.Feedback>
          <Form.Control.Feedback type="invalid">
            Please provide a valid pay rate.
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group as={Col} md="2" controlId="validationCustom05">
          <Form.Label>Int. Per Diem Rate</Form.Label>
          <Form.Control
            type="number"
            step="0.01"
            placeholder="Millions?"
            required
            onChange={(e) =>
              setSignupObj({
                ...signupObj,
                international_per_diem_pay: e.target.value,
              })
            }
          />
          <Form.Control.Feedback>
            Bro, thats hella money! 💰
          </Form.Control.Feedback>
          <Form.Control.Feedback type="invalid">
            Please provide a valid pay rate.
          </Form.Control.Feedback>
        </Form.Group>
        <Form.Group as={Col} md="2" controlId="validationCustom07">
          <Form.Label>Override Pay Rate</Form.Label>
          <Form.Control
            type="number"
            step="0.01"
            placeholder="Millions?"
            required
            onChange={(e) =>
              setSignupObj({ ...signupObj, override_pay: e.target.value })
            }
          />
          <Form.Control.Feedback>
            Adjusted pay rate updated!
          </Form.Control.Feedback>
          <Form.Control.Feedback type="invalid">
            Please provide a valid pay rate.
          </Form.Control.Feedback>
        </Form.Group>
        <Form.Group as={Col} md="2" controlId="validationCustom08">
          <Form.Label>A Position Rate</Form.Label>
          <Form.Control
            type="number"
            step="0.01"
            placeholder="Millions?"
            required
            onChange={(e) =>
              setSignupObj({ ...signupObj, a_postion_pay: e.target.value })
            }
          />
          <Form.Control.Feedback>
            Adjusted pay rate updated!
          </Form.Control.Feedback>
          <Form.Control.Feedback type="invalid">
            Please provide a valid pay rate.
          </Form.Control.Feedback>
        </Form.Group>
      </Row>
      <Form.Group className="mb-3">
        <Form.Check
          required
          label="Agree to terms and conditions"
          feedback="You must agree before submitting."
          feedbackType="invalid"
        />
      </Form.Group>
      <Button type="submit">Submit form</Button>
    </Form>
  );
}
