import "./App.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Container } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

import Homepage from "./Pages/Homepage";

import HawkerActions from "./Pages/HawkerActions";
import HawkerOrders from "./Pages/HawkerOrders";
import HawkerPlaceOrder from "./Pages/HawkerPlaceOrder";
import HawkerMakePayment from "./Pages/HawkerMakePayment";
import HawkerPayments from "./Pages/HawkerPayments";

import WasherActions from "./Pages/WasherActions";
import WasherUpdate from "./Pages/WasherUpdate";
import WasherTransactions from "./Pages/WasherTransactions";

import Success from "./Pages/Success";

import Header from "./Components/Header";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

function App() {
  const hawker_id = "stevejobs"; // can change to whichever username
  const washer_id = "roylee"; // can change to whichever username
  return (
    <ThemeProvider theme={darkTheme}>
      <Container maxWidth="md">
        <CssBaseline />
        <BrowserRouter>
          <Header />
          <Routes>
            <Route path="/" element={<Homepage />} />
            <Route
              path="/hawker-actions"
              element={<HawkerActions hawker_id={hawker_id} />}
            />
            <Route
              path="/hawker-orders"
              element={<HawkerOrders hawker_id={hawker_id} />}
            />
            <Route
              path="/hawker-place-order"
              element={<HawkerPlaceOrder hawker_id={hawker_id} />}
            />
            <Route
              path="/hawker-make-payment"
              element={<HawkerMakePayment hawker_id={hawker_id} />}
            />
            <Route
              path="/hawker-payments"
              element={<HawkerPayments hawker_id={hawker_id} />}
            />
            <Route
              path="/washer-actions"
              element={<WasherActions washer_id={washer_id} />}
            />
            <Route
              path="/washer-update"
              element={<WasherUpdate washer_id={washer_id} />}
            />
            <Route
              path="/washer-transactions"
              element={<WasherTransactions washer_id={washer_id} />}
            />
            <Route
              path="/success"
              element={<Success hawker_id={hawker_id} />}
            />
          </Routes>
        </BrowserRouter>
      </Container>
    </ThemeProvider>
  );
}

export default App;
