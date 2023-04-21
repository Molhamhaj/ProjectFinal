import React from "react";
import { Routes, Route, BrowserRouter as Router } from "react-router-dom";
import Login from "./auth/Login";
import Register from "./auth/Register";
import Home from "./views/Home";
import Layout from "./layout/Layout";
import TakeMeToAdmin from "./components/TakeMeToAdmin";
import "./App.css";
import Book from "./views/Book";
import MyTickets from "./views/MyTickets";
import MyFlights from "./views/MyFlights";
import AddFlight from "./views/AddFlight";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route
            path="/"
            element={
              <Layout>
                <Home />
              </Layout>
            }
          />
          <Route
            path="/book/:flight_id"
            element={
              <Layout login={true} customer={true}>
                <Book />
              </Layout>
            }
          />
          <Route
            path="/myTickets"
            element={
              <Layout login={true} customer={true}>
                <MyTickets />
              </Layout>
            }
          />
          <Route
            path="/myFlights"
            element={
              <Layout login={true} airline={true}>
                <MyFlights />
              </Layout>
            }
          />
          <Route
            path="/addFlight"
            element={
              <Layout login={true} airline={true}>
                <AddFlight />
              </Layout>
            }
          />
          <Route
            path="/addFlight/:flight_id"
            element={
              <Layout login={true} airline={true}>
                <AddFlight />
              </Layout>
            }
          />
          <Route path="/admin" element={<TakeMeToAdmin />} />
          <Route
            path="/login"
            element={
              <Layout single={true}>
                <Login />
              </Layout>
            }
          />
          <Route
            path="/register"
            element={
              <Layout single={true}>
                <Register />
              </Layout>
            }
          />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
