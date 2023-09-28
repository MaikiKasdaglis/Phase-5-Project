/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import useUserStore from "../../hooks/useStore";

function PairingAddModal({ displayMonth, onPostSuccess, forceReset }) {
  const { user } = useUserStore();
  //============MODAL SHIT=====================
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  //=============MONTH STUFF=================
  // console.log(displayMonth[0].pairings_field, "from modal");
  const num = displayMonth[0].pairings_field.length + 1;
  //=============POST OBJ====================
  const [postObj, setPostObj] = useState({
    int_tafb_pay: 0,
    int_tafb_total: 0.0,
    month_id: displayMonth[0].id,
    pairing_a_hours: 0,
    pairing_a_pay: 0,
    pairing_double_half: 0,
    pairing_double_half_pay: 0,
    pairing_double_half_rated: 0,
    pairing_double_time: 0.0,
    pairing_double_time_pay: 0.0,
    pairing_double_time_rated: 0.0,
    pairing_duty_hours: 0.0,
    pairing_guarantee_hours: 0,
    pairing_guarantee_hours_worked_rated: 0.0,
    pairing_holiday: 0.0,
    pairing_holiday_pay: 0.0,
    pairing_holiday_rated: 0.0,
    pairing_name: `Pairing ${num}`,
    pairing_overrides: 0,
    pairing_overrides_pay: 0,
    pairing_tfp: 0,
    pairing_tfp_pay: 0,
    pairing_time_half: 0.0,
    pairing_time_half_pay: 0.0,
    pairing_time_half_rated: 0.0,
    pairing_total_credits: 0,
    pairing_total_credits_rated: 0,
    pairing_total_pay: 0,
    pairing_triple: 0.0,
    pairing_triple_pay: 0.0,
    pairing_triple_rated: 0.0,
    pairing_vacation_sick: 0.0,
    pairing_vacation_sick_pay: 0.0,
    pairing_vja: 0.0,
    pairing_vja_pay: 0.0,
    pairing_vja_rated: 0.0,
    reserve_block: false,
    tafb_pay: 0,
    tafb_total: 0.0,
    pairing_reserve_no_fly_hours: 0.0,
    pairing_reserve_no_fly_pay: 0.0,
  });
  function handleSubmit() {
    console.log(postObj);
    handleClose();
    fetch("/api/pairings", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postObj),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response error");
        }
        return response.json();
      })
      .then((data) => {
        console.log(`this is the reponse from new pairing post`, data);
        // window.location.reload();
        // onPostSuccess();
        // fetch(`/api/users/${user.id}`);

        forceReset("pairingAddModal");
        location.reload();
      })
      .catch((error) => {
        console.log("error", error.message);
      });
  }

  return (
    <>
      <Button
        style={{ width: "100%" }}
        variant="dark"
        className="m-0 mt-5 p-0 rounded-0"
        onClick={handleShow}
      >
        {`Add Pairing to ${displayMonth[0].month}`}
      </Button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          {/* <Modal.Title>Modal heading</Modal.Title> */}
        </Modal.Header>
        <Modal.Body>
          Are you sure you want to add a pairing to {displayMonth[0].month}?
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Go Back
          </Button>
          <Button variant="dark" onClick={handleSubmit}>
            Add the Pairing!
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default PairingAddModal;
