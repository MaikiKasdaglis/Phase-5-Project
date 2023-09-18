/* eslint-disable react/prop-types */
import { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";

function ReserveBlockToggle({ diff_reserve_block, id, pairing }) {
  const [isSwitchOn, setIsSwitchOn] = useState(false);
  const [updateObj, setUpdateObj] = useState({});
  // console.log("this is the id", id);
  useEffect(() => {
    const updatedOg = { ...pairing };
    delete updatedOg.days_field;
    // console.log("UPDATED OG", updatedOg);
    setUpdateObj(updatedOg);
    setIsSwitchOn(diff_reserve_block);
  }, [diff_reserve_block, pairing]);

  const handleSwitchChange = (event) => {
    const isChecked = event.target.checked;
    setIsSwitchOn(isChecked);
    // console.log(isChecked);
    // setUpdateObj((prevUpdateObj) => ({
    //   ...prevUpdateObj,
    //   reserve_block: isChecked,
    // }));
    // console.log(updateObj);

    const newObj = {
      ...updateObj,
      reserve_block: isChecked,
      pairing_reserve_no_fly_hours: 0,

      pairing_reserve_no_fly_pay: 0,
    };
    // console.log(newObj);
    fetch(`/api/pairings/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newObj),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response error");
        }
        return response.json();
      })
      .then((data) => {
        console.log("this is form data", data);
      })
      .catch((error) => {
        console.log("error", error.message);
      });
  };

  // console.log("og pairing", pairing);
  //   console.log("updateObj", updateObj);

  return (
    <Form>
      <div className="d-flex align-items-center">
        <Form.Check
          type="switch"
          id="custom-switch"
          className="m-2"
          style={{ backgroundColor: "black" }}
          onChange={handleSwitchChange}
          checked={isSwitchOn}
        />
        <Form.Label className="m-2" htmlFor="custom-switch">
          : This is a Reserve Block
        </Form.Label>
      </div>
    </Form>
  );
}

export default ReserveBlockToggle;
