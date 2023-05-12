import React from "react";
import API_LINK from "../API";

function Success({ hawker_id }) {
  console.log(hawker_id);
  const response = fetch(API_LINK + `hawkerpayment`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      hawker_id: hawker_id,
    }),
  });
  return <div>Success</div>;
}

export default Success;
