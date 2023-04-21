import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Navbar(props) {
  let navigate = useNavigate();
  const logout = async () => {
    sessionStorage.removeItem("loggedin");
    props.setSession(props.__init_session);
    navigate("/login");
  };
  return (
    <header className="p-3 bg-dark text-white">
      <div className="container">
        <div className="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
          <Link className="navbar-brand text-decoration-none text-light" to="/">
            Flight Management System
          </Link>
          <ul className="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
            <li>
              <Link to="/" className="nav-link px-2 text-secondary">
                Home
              </Link>
            </li>
            {props.session.role === "airline" ? (
              <li>
                <Link
                  to="/myFlights"
                  className="nav-link px-2 text-white"
                  data-role="airline"
                >
                  My Flights
                </Link>
              </li>
            ) : (
              ""
            )}
            {props.session.role === "customer" ? (
              <li>
                <Link
                  to="/myTickets"
                  className="nav-link px-2 text-white"
                  data-role="customer"
                >
                  My Tickets
                </Link>
              </li>
            ) : (
              ""
            )}
          </ul>
          <div className="text-end">
            {!props.isLoggedIn ? (
              <>
                {" "}
                <Link
                  to="/login"
                  className="btn btn-outline-light me-2"
                  data-mode="not-loggedin"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="btn btn-outline-light"
                  data-mode="not-loggedin"
                >
                  Register
                </Link>
              </>
            ) : (
              <>
                <span data-mode="loggedin" className="me-3 text-light">{props?.session?.personal?.username}</span>
                <button
                  onClick={logout}
                  className="btn btn-outline-danger"
                  data-mode="loggedin"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
