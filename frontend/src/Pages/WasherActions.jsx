import React from "react";
import { Button } from "@mui/material";
import { Link } from "react-router-dom";

function WasherActions({ washer_id }) {
  return (
    <div>
      Logged in as: {washer_id}
      <h1 style={{ fontSize: 50,}}>Hello {washer_id}, what would you like to do today?</h1>
      <br />
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <Link to="/washer-update">
        <Button variant="contained" style={{ fontSize: 20}}><b>Washer Update</b></Button>
      </Link>{" "}
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{" "}
      <Link to="/washer-transactions">
        <Button variant="contained" style={{ fontSize: 20}}><b>Washer Transactions</b></Button>
      </Link>
    </div>
  );
}

export default WasherActions;
