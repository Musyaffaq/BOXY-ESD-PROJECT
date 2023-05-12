import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import { React, useState, useEffect } from "react";
import { Button } from "@mui/material";
import { Link } from "react-router-dom";
import API_LINK from "../API";

function HawkerPayments({ hawker_id }) {
  // Get all payments
  const [payments, setPayments] = useState([]);
  useEffect(() => {
    try {
      fetch(API_LINK + `payment/hawker/` + hawker_id)
        .then((res) => res.json())
        .then((data) => setPayments(data["data"]["payments"]));
      // console.log(payments);
    } catch (error) {
      console.error("An error occurred during fetch: ", error);
    }
  }, []);
  return (
    <div>
      Logged in as: {hawker_id}
      <h1>View your past payments here</h1>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Payment ID</TableCell>
            <TableCell>Order ID</TableCell>
            <TableCell>Payment Amount</TableCell>
            <TableCell>Payment Date</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {payments.map((item, id) => {
            return (
              <TableRow key={id}>
                <TableCell>{item["payment_id"]}</TableCell>
                <TableCell>{item["order_id"]}</TableCell>
                <TableCell>{item["payment_amount"]}</TableCell>
                <TableCell>{item["payment_date"].slice(0, -3)}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
      <br></br>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      <Link to="/hawker-actions">
        <Button variant="contained"><b>Back</b></Button>
      </Link>
      </div>
    </div>
  );
}

export default HawkerPayments;
