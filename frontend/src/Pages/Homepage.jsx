import React from "react";
import { Button } from "@mui/material";
import { Link } from "react-router-dom";



function Homepage() {
  return (
    <div style={{height: '100vh', margin:0}}>
      <h1 style={{ fontSize: 70, marginBottom: 0}}>BOXY&reg;</h1>
      <h2 style={{ fontSize: 30, marginTop: 0}}>Changing the world, one box at a time</h2>
      <br />
      <div style={{display: "flex",
          justifyContent: "center",
          alignItems: "center"}}>
      <Link to="hawker-actions">
        <Button variant="contained" style={{ fontSize: 20}}><b>For Hawkers</b></Button>
      </Link>{" "}
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {"  "}
      <Link to="washer-actions">
        <Button variant="contained" style={{ fontSize: 20}}><b>For Washers</b></Button>
      </Link>
      </div>
    </div>
  );
}

export default Homepage;
