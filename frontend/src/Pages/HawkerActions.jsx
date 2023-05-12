import React from "react";
import { Button } from "@mui/material";
import { Link } from "react-router-dom";

function HawkerActions({ hawker_id }) {
  return (
    <div >
      Logged in as: {hawker_id}
      <h1 style={{ fontSize: 50,}}>Hello {hawker_id}, what would you like to do today?</h1>
      <br />
      <Link to="/hawker-orders">
        <Button variant="contained"><b>View Orders</b></Button>
      </Link>{" "}
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{" "}
      <Link to="/hawker-place-order">
        <Button variant="contained"><b>Place Order</b></Button>
      </Link>{" "}
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{" "}
      <Link to="/hawker-make-payment">
        <Button variant="contained"><b>Make Payment</b></Button>
      </Link>{" "}
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{" "}
      <Link to="/hawker-payments">
        <Button variant="contained"><b>View Payments</b></Button>
      </Link>
    </div>
  );
}

export default HawkerActions;
