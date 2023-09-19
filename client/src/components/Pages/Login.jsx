/* eslint-disable react/no-unescaped-entities */
import { useState } from "react";
import { Container, Row, Col, Form, Button, Alert } from "react-bootstrap";
import useUserStore from "../../hooks/useStore";
import { Link } from "react-router-dom";
// eslint-disable-next-line no-unused-vars
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { updateUser, user } = useUserStore();
  const [error, setError] = useState(""); // Step 1: State for error message

  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    const userObj = {
      username,
      password,
    };
    setError(""); // Reset error message before making the request
    console.log(userObj);
    fetch("/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userObj),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response error");
        }
        return response.json();
      })
      .then((data) => {
        console.log("this is what we talkin bout", data);
        console.log(user, `before`);
        updateUser(data);
        console.log(user, `after`);
        navigate("/userinfo");
      })
      .catch((error) => {
        setError("Try again, stupid idiot"); // Step 2: Set error message
        console.log("error", error.message);
      });
  };
  return (
    <>
      <Container
        style={{
          zIndex: 5,
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          border: "5px, black",
        }}
        className="mt-5"
      >
        <Row className="justify-content-center mt-5">
          <Col lg={6}>
            <Form className="border p-4" onSubmit={(e) => handleLogin(e)}>
              {error && (
                <Alert className="mt-5" variant="danger">
                  {error}
                </Alert>
              )}{" "}
              {/* Step 4: Display error message */}
              <Form.Group className="mb-3" controlId="formBasicUsername">
                <Form.Label>Username</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </Form.Group>
              <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </Form.Group>
              <Button variant="dark" type="submit" className="m-1 rounded-0">
                Login
              </Button>
              <Link
                style={{ marginLeft: "5px" }}
                className="btn btn-secondary rounded-0"
                variant="secondary"
                to="signup"
                activeClassName="active"
              >
                Signup
              </Link>
            </Form>
          </Col>
        </Row>
      </Container>
    </>
  );
}
