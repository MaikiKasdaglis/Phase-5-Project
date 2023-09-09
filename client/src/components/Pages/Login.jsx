/* eslint-disable react/no-unescaped-entities */
import { useState } from "react";
import { Container, Row, Col, Form, Button } from "react-bootstrap";
import useUserStore from "../../hooks/useStore";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { updateUser, user } = useUserStore();

  const handleLogin = (e) => {
    e.preventDefault();
    const userObj = {
      username,
      password,
    };
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
        //   navigate("/home");
      })
      .catch((error) => {
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
      >
        <Row className="justify-content-center">
          <Col lg={6}>
            <Form className="border p-4" onSubmit={(e) => handleLogin(e)}>
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

              <Button variant="primary" type="submit">
                Submit
              </Button>
            </Form>
          </Col>
        </Row>
      </Container>
    </>
  );
}
