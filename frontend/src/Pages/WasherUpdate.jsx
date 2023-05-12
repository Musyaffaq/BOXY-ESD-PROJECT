import React, { useState } from "react";
import ReactConfirmAlert, { confirmAlert } from "react-confirm-alert"; // Import
import "react-confirm-alert/src/react-confirm-alert.css"; // Import css
//import AlertConfirm from 'react-alert-confirm';
//import { Alert } from 'react-alert'

import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
} from "@mui/material";
import { Link } from "react-router-dom";
import API_LINK from "../API";

const packagingTypes = [
  "large-bento",
  "large-bowl",
  "medium-bento",
  "medium-bowl",
  "small-bento",
  "small-bowl",
];

function WasherUpdate({ washer_id }) {
  const [packagingType, setPackagingType] = useState("");
  const [quantity, setQuantity] = useState("");
  const [message, setMessage] = useState(false);

  const handlePackagingTypeChange = (event) => {
    setPackagingType(event.target.value);
  };

  const handleQuantityChange = (event) => {
    setQuantity(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    let submittingForm = {
      washer_id: washer_id, // must change to username of hawker
      packaging_type: packagingType,
      quantity: parseInt(quantity),
    };
    console.log(submittingForm);

    try {
      const response = await fetch(API_LINK + `washingvendorupdate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(submittingForm),
      });

      if (response.ok) {
        // handle success
        console.log("success!");
        setMessage(true);
      } else {
        // handle error
        console.error("Form submission failed.");
        throw new Error("Form submission failed.");
      }
    } catch (error) {
      console.error("An error occurred:", error);
      throw error;
    }
  };

  const confirmSubmit = (event) => {
    event.preventDefault();
    confirmAlert({
      title: "Confirm to submit", // Title dialog
      message: "Are you sure to do this.", // Message dialog
      childrenElement: () => <div></div>, // Custom UI or Component
      confirmLabel: "Confirm", // Text button confirm
      cancelLabel: "Cancel", // Text button cancel
      buttons: [
        {
          label: "Confirm",
          onClick: () => handleSubmit(event),
        },
        {
          label: "Cancel",
          onClick: () => alert("Action cancelled"),
        },
      ],
      onConfirm: () => handleSubmit, // Action after Confirm
      onCancel: () => alert("Action cancelled"), // Action after Cancel
    });
  };

  return (
    <div>
      Logged in as: {washer_id}
      <h1 style={{ fontSize: 50 }}>Return washed packages</h1>
      <form onSubmit={confirmSubmit}>
        <FormControl fullWidth>
          <InputLabel id="packaging-type-label">Packaging Type</InputLabel>
          <Select
            labelId="packaging-type-label"
            id="packaging-type"
            value={packagingType}
            onChange={handlePackagingTypeChange}
          >
            {packagingTypes.map((type) => (
              <MenuItem key={type} value={type}>
                {type}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <br></br>
        <br></br>
        <TextField
          fullWidth
          label="Quantity"
          type="number"
          value={quantity}
          onChange={handleQuantityChange}
        />
        <br></br>
        <br></br>
        <Button variant="contained" color="primary" type="submit">
          <b>Submit</b>
        </Button>
      </form>
      {message ? "Successfully updated inventory!" : null}
      <br></br>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Link to="/washer-actions">
          <Button variant="contained">
            <b>Back</b>
          </Button>
        </Link>
      </div>
    </div>
  );
}

export default WasherUpdate;
