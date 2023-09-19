import { useState } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import { Form } from "react-bootstrap";

function TermsConditions({ setReadAgreements }) {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const handleAgree = () => {
    setReadAgreements(true);
    handleClose();
  };
  const handleDisagree = () => {
    setReadAgreements(false);
    handleClose();
  };

  return (
    <>
      <Form.Label
        className="m-2 text-primary text-underline cursor-pointer"
        onClick={handleShow}
        htmlFor="custom-switch"
      >
        <a href="#" className="link-unstyled">
          Agree to terms and conditions
        </a>
      </Form.Label>
      {/* <Button variant="primary" onClick={handleShow}>
        Launch demo modal
      </Button> */}

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Terms and Conditions</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          I will not read these terms and conditions. Also, I agree to go get
          beers after this. Lastly, I agree to be impeccable with my word, not
          to take anything personally, not to make assumptions and to always do
          my best.{" "}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleDisagree}>
            Nope
          </Button>
          <Button variant="primary" onClick={handleAgree}>
            I Agree
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default TermsConditions;
