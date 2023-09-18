import Form from "react-bootstrap/Form";
import { useState, useEffect } from "react";

function ApositionToggle({ a_position, id, day }) {
  const [isSwitchOn, setIsSwitchOn] = useState(false);
  const [updateObj, setUpdateObj] = useState({});
  return (
    <Form style={{ position: "sticky", top: 0, background: "white" }}>
      <Form.Check // prettier-ignore
        type="switch"
        id="custom-switch"
        label="Check this switch"
      />
      <Form.Check // prettier-ignore
        disabled
        type="switch"
        label="disabled switch"
        id="disabled-custom-switch"
      />
    </Form>
  );
}

export default ApositionToggle;
