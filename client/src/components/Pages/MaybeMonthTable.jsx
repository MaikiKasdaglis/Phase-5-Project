import React from "react";
import { Table } from "react-bootstrap";

export default function MaybeMonthTable() {
  return (
    <>
      <div>MaybeMonthTable</div>
      <Table striped bordered hover style={{ border: "2px solid black" }}>
        <thead>
          <tr>
            <th>Category</th>
            <th>Credits</th>
            <th>Rate</th>
            <th>Total</th>
            <th>Pay</th>
          </tr>
        </thead>
        <tbody>
          {displayMonth[0]?.month_guarantee_hours ? (
            <tr>
              <td>Guarantee Hours</td>
              <td>{displayMonth[0].month_guarantee_hours}</td>
              <td>1</td>
              <td>{displayMonth[0].month_guarantee_hours * 1}</td>
              <td>
                $
                {(
                  user.tfp_pay *
                  (displayMonth[0].month_guarantee_hours * 1)
                ).toFixed(2)}
              </td>
            </tr>
          ) : null}
          <tr>
            <td>1</td>
            <td>Mark</td>
            <td>Otto</td>
            <td>@mdo</td>
            <td>@mdo</td>
          </tr>
          <tr>
            <td>2</td>
            <td>Jacob</td>
            <td>Thornton</td>
            <td>@fat</td>
            <td>@mdo</td>
          </tr>
          <tr>
            <td>3</td>
            <td>Larry the Bird</td>
            <td>@twitter</td>
            <td>@mdo</td>
            <td>@mdo</td>
          </tr>
        </tbody>
        <tfoot style={{ border: "2px solid black" }}>
          <tr>
            <th>Category</th>
            <th>Credits</th>
            <th>Rate</th>
            <th>Total</th>
            <th>Pay</th>
          </tr>
        </tfoot>
      </Table>
    </>
  );
}
