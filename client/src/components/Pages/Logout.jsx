import { Container, Row, Col, Form, Button } from "react-bootstrap";
import useUserStore from "../../hooks/useStore";
import { useNavigate } from "react-router-dom";

export default function Logout() {
  const { deleteUser } = useUserStore();
  const navigate = useNavigate();

  const handleBackToHome = () => {
    navigate("/login");
  };

  const handleLogout = (e) => {
    e.preventDefault();
    fetch("/api/logout", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response error");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        deleteUser();
        navigate("/login");
      })
      .catch((error) => {
        console.log("error", error.message);
      });
  };
  return (
    <Container>
      <Row className="justify-content-center mt-4">
        <Col xs={12} md={8} lg={6}>
          <div
            className="border p-4 rounded"
            style={{ backgroundColor: "rgba(225 , 225, 225, 0.5)" }}
          >
            <h2>Are You Sure You Want To Logout? </h2>
            <Form>
              <Button
                variant="primary"
                type="submit"
                onClick={handleLogout}
                className="m-1 "
              >
                Logout
              </Button>
              <Button
                style={{ marginLeft: "5px" }}
                variant="secondary"
                onClick={handleBackToHome}
              >
                Back To Home
              </Button>
            </Form>
          </div>
        </Col>
      </Row>
    </Container>
  );
}
