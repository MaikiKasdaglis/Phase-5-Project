/* eslint-disable react/jsx-no-duplicate-props */
/* eslint-disable react/prop-types */
import { useState } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";

function DeleteYearModal({ usersYears }) {
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const [selectedYear, setSelectedYear] = useState();
  const [thisWorks, setThisWorks] = useState("dark");

  // console.log(usersYears);

  function handleDelete(selectedYear) {
    // console.log("gonna delete", selectedYear);
    fetch(`/api/years/${selectedYear}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(),
    });
  }

  return (
    <>
      <Button
        style={{ width: "100%" }}
        className="m-0 mb-1  p-0 rounded-0"
        onClick={handleShow}
        variant={thisWorks}
        onMouseEnter={() => setThisWorks("danger")}
        onMouseLeave={() => setThisWorks("dark")}
      >
        Delete Year
      </Button>

      <Modal
        show={show}
        onHide={handleClose}
        backdrop="static"
        keyboard={false}
      >
        <Modal.Header closeButton>
          <Modal.Title>Select Year You Wish To Delete</Modal.Title>
        </Modal.Header>
        <Modal.Body className="d-flex justify-content-around">
          {usersYears.map((year) => (
            <Button
              className="m-1 rounded-0"
              key={year.id}
              onClick={() => setSelectedYear(year.id)}
              variant={year.id === selectedYear ? "danger" : "dark"}
            >
              {year.year}
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
            onClick={() => handleDelete(selectedYear)}
          >
            Delete Selected Year
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default DeleteYearModal;
