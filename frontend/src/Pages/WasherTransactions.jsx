import {
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import { React, useState, useEffect } from "react";
import { Link } from "react-router-dom";
import API_LINK from "../API";

function WasherTransactions({ washer_id }) {
  // Get all washer transactions

  const [transactions, setTransactions] = useState([]);
  useEffect(() => {
    try {
      fetch(API_LINK + `transaction/washer/` + washer_id)
        .then((res) => res.json())
        .then((data) => setTransactions(data["data"]["transactions"]));
      // console.log(transactions);
    } catch (error) {
      console.error("An error occurred during fetch: ", error);
    }
  }, []);
  return (
    <div>
      Logged in as: {washer_id}
      <h1 style={{ fontSize: 50,}}>View your past transactions</h1>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Transaction ID</TableCell>
            <TableCell>Packaging Type</TableCell>
            <TableCell>Quantity</TableCell>
            <TableCell>Transaction Date</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {transactions
            ? transactions.map((item, id) => {
                return (
                  <TableRow key={id}>
                    <TableCell>{item["transaction_id"]}</TableCell>
                    <TableCell>{item["packaging_type"]}</TableCell>
                    <TableCell>{item["quantity"]}</TableCell>
                    <TableCell>{item["created"]}</TableCell>
                  </TableRow>
                );
              })
            : null}
        </TableBody>
      </Table>
      <br></br>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      <Link to="/washer-actions">
        <Button variant="contained" ><b>Back</b></Button>
      </Link>
      </div>
    </div>
  );
}

export default WasherTransactions;
