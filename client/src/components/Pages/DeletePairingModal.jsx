/* eslint-disable react/jsx-no-duplicate-props */
/* eslint-disable react/prop-types */
// eslint-disable-next-line no-unused-vars
import { useEffect, useState } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";

function DeletePairingModal({ displayMonth }) {
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const [selectedPairing, setSelectedPairing] = useState();
  const [thisWorks, setThisWorks] = useState("dark");

  //   console.log("hella parings?", displayMonth[0].pairings_field);

  function handleDelete(selectedPairing) {
    // console.log("gonna delete", selectedPairing);
    fetch(`/api/pairings/${selectedPairing}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(),
    })
      .then(() => {
        // Refresh the page after successful deletion
        location.reload();
      })
      .catch((error) => {
        console.error("Error deleting pairing:", error);
      });
    handleClose();
  }
  // useEffect(() => {
  //   console.log("refreshing, isnt it? ");
  // }, [displayMonth]);

  return (
    <>
      <Button
        style={{ width: "100%" }}
        className="m-0 mt-1  p-0 rounded-0"
        onClick={handleShow}
        variant={thisWorks}
        onMouseEnter={() => setThisWorks("danger")}
        onMouseLeave={() => setThisWorks("dark")}
      >
        Delete Pairing
      </Button>

      <Modal
        show={show}
        onHide={handleClose}
        backdrop="static"
        keyboard={false}
      >
        <Modal.Header closeButton>
          <Modal.Title>Select Pairing You Wish To Delete</Modal.Title>
        </Modal.Header>
        <Modal.Body className="d-flex justify-content-around">
          {displayMonth[0].pairings_field.map((pairing) => (
            <Button
              className="m-1 rounded-0"
              key={pairing.id}
              onClick={() => setSelectedPairing(pairing.id)}
              variant={pairing.id === selectedPairing ? "danger" : "dark"}
            >
              {pairing.pairing_name}
            </Button>
          ))}
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            className=" rounded-0"
            onClick={handleClose}
          >
            Close
          </Button>
          <Button
            className=" rounded-0"
            variant="danger"
            onClick={() => handleDelete(selectedPairing)}
          >
            Delete Selected Pairing
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default DeletePairingModal;
