import {
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import { React, useState, useEffect } from "react";
import { Link } from "react-router-dom";
import API_LINK from "../API";
import ReactConfirmAlert, { confirmAlert } from "react-confirm-alert"; // Import
import "react-confirm-alert/src/react-confirm-alert.css"; // Import css

function HawkerPlaceOrder({ hawker_id }) {
  const [message, setMessage] = useState(false);

  // Get all the inventory
  const [inventory, setInventory] = useState([]);
  useEffect(() => {
    try {
      fetch(API_LINK + "inventory")
        .then((res) => res.json())
        .then((data) => setInventory(data["data"]["inventory"]));
    } catch (error) {
      console.error("An error occurred during fetch: ", error);
    }
  }, []);

  // form data
  const [formData, setFormData] = useState([
    { packaging_type: "", quantity: "" },
  ]);
  const [additionalInputs, setAdditionalInputs] = useState([]);

  const packagingTypes = [
    "large-bento",
    "large-bowl",
    "medium-bento",
    "medium-bowl",
    "small-bento",
    "small-bowl",
  ];

  const handleInputChange = (event, index) => {
    const { name, value } = event.target;
    setFormData((prevFormData) => {
      const updatedFormData = [...prevFormData];
      updatedFormData[index] = {
        ...updatedFormData[index],
        [name]: value,
      };
      return updatedFormData;
    });
  };

  const handleAddInput = () => {
    setAdditionalInputs((prevInputs) => [...prevInputs, prevInputs.length + 1]);
    setFormData((prevFormData) => [
      ...prevFormData,
      { packaging_type: "", quantity: "" },
    ]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formattedData = formData.map((data) => ({
      packaging_type: data.packaging_type,
      quantity: parseInt(data.quantity),
    }));

    let submittingForm = {
      hawker_id: hawker_id,
      cart_item: formattedData,
    };
    console.log(submittingForm); // log form data

    try {
      const response = await fetch(API_LINK + `hawkerplaceorder`, {
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
      message: "Are you sure you want to submit this?", // Message dialog
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
      Logged in as: {hawker_id}
      <h1>Place your order for Boxy packages here</h1>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Type</TableCell>
            <TableCell>Available</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {inventory.map((item, id) => {
            return (
              <TableRow key={id}>
                <TableCell>{item["type"]}</TableCell>
                <TableCell>{item["available"]}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
      <br></br>
      --- Order Form --- <br />
      <br></br>
      <form onSubmit={confirmSubmit}>
        {formData.map((data, index) => (
          <div key={index}>
            <FormControl sx={{ minWidth: 120 }}>
              <InputLabel id={`packaging_type${index}-label`}>
                Packaging Type {index + 1}
              </InputLabel>
              <Select
                labelId={`packaging_type${index}-label`}
                name="packaging_type"
                value={data.packaging_type}
                onChange={(event) => handleInputChange(event, index)}
              >
                {packagingTypes.map((type) => (
                  <MenuItem key={type} value={type}>
                    {type}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            &nbsp;&nbsp;&nbsp;
            <TextField
              name="quantity"
              label={`Quantity`}
              value={data.quantity}
              onChange={(event) => handleInputChange(event, index)}
            />
          </div>
        ))}
        <br></br>
        <Button onClick={handleAddInput} variant="contained">
          <b>Add Input</b>
        </Button>
        &nbsp;&nbsp;&nbsp;
        <Button type="submit" variant="contained">
          <b>Submit</b>
        </Button>
      </form>
      {message ? "Order successfully placed!" : null}
      <br></br>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Link to="/hawker-actions">
          <Button variant="contained">
            <b>Back</b>
          </Button>
        </Link>
      </div>
    </div>
  );
}

export default HawkerPlaceOrder;
