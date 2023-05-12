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

function HawkerOrders({ hawker_id }) {
  // Get all the orders
  const [orders, setOrders] = useState([]);
  useEffect(() => {
    try {
      fetch(API_LINK + `orders/hawker/` + hawker_id)
        .then((res) => res.json())
        .then((data) => setOrders(data["data"]["orders"]));
      // console.log(orders);
    } catch (error) {
      console.error("An error occurred during fetch: ", error);
    }
  }, []);
  return (
    <div>
      Logged in as: {hawker_id}
      <h1>Your past hawker orders</h1>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Order ID</TableCell>
            <TableCell>Order Items</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Order Date</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {orders
            ? orders.map((item, id) => {
                return (
                  <TableRow key={id}>
                    <TableCell>{item["order_id"]}</TableCell>
                    <TableCell>
                      {item["order_item"].map((i) => {
                        return (
                          <>
                            {i["packaging_type"]} - {i["quantity"]}
                            <br />
                          </>
                        );
                      })}
                    </TableCell>
                    <TableCell>{item["status"]}</TableCell>
                    <TableCell>{item["created"]}</TableCell>
                  </TableRow>
                );
              })
            : null}
        </TableBody>
      </Table>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      <Link to="/hawker-actions">
        <Button variant="contained"><b>Back</b></Button>
      </Link>
      </div>
    </div>
  );
}

export default HawkerOrders;
