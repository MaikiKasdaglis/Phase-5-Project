import { NavLink, Outlet, Link } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import useUserStore from "../../hooks/useStore";

export default function RootLayout() {
  const { user } = useUserStore();
  const navLinkText = user ? "Logout" : "Login";
  const navLinkTo = user ? "/logout" : "/login";
  const welcomeMessage = user ? user.username : "Login/Signup";
  return (
    <div>
      <Navbar
        expand="lg"
        className="bg-body-tertiary"
        bg="dark"
        data-bs-theme="dark"
        style={{ position: "relative", zIndex: "100" }}
      >
        <Container>
          <Navbar.Brand href="#home">FA Pay Tracker</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              {user ? (
                <NavLink to="dashboard" className="nav-link">
                  Dashboard
                </NavLink>
              ) : null}
              {/* {user ? <h1>hi</h1> : null} */}
              {user ? <Nav.Link href="#link">Link</Nav.Link> : null}
              {user ? <Nav.Link href="#link">Link</Nav.Link> : null}
              {user ? (
                <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                  <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                  <NavDropdown.Item href="#action/3.2">
                    Another action
                  </NavDropdown.Item>
                  <NavDropdown.Item href="#action/3.3">
                    Something
                  </NavDropdown.Item>
                  <NavDropdown.Divider />
                  <NavDropdown.Item href="#action/3.4">
                    Separated link
                  </NavDropdown.Item>
                </NavDropdown>
              ) : null}
            </Nav>
            <Nav className="ml-auto">
              <NavDropdown
                title={welcomeMessage}
                id="basic-nav-dropdown"
                className="custom-dropdown"
              >
                <Link to={navLinkTo} className="dropdown-item">
                  {navLinkText}
                </Link>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <main>
        <Outlet />
      </main>
    </div>
  );
}
