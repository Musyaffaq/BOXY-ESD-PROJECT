import { Button } from "@mui/material";
import React from "react";
import { Link } from "react-router-dom";

function Header() {
  return (
    <div>
      <Link to="/">
        <Button variant="contained"><b>Home</b></Button>
      </Link>
    </div>
  );
}

export default Header;
