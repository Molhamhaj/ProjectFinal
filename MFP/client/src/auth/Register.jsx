import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";
import {
  CONSTANT,
  setMessage,
  resetMessage,
  checkLoginFromLogin,
} from "../CONSTANT";

const Register = () => {
  const navigate = useNavigate();
  useEffect(() => {
    if (checkLoginFromLogin()) {
      navigate("/");
    }
  }, []);
  const init__payload = {
    username: "",
    password: "",
    email: "",
    user_role: "",
    first_name: "",
    last_name: "",
    address: "",
    phone_no: "",
    credit_card_no: "",
    name: "",
    country: "",
  };
  const [payload, setPayload] = useState(init__payload);
  const changePayload = (e) => {
    setPayload({
      ...payload,
      [e.target.name]: e.target.value,
    });
  };

  const [countries, setCountries] = useState([]);

  const fetchCountries = async () => {
    await axios
      .get(CONSTANT.server + `countries`)
      .then((response) => {
        setCountries(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    fetchCountries();
  }, []);

  const validateForm = () => {
    let isValid = true;
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (
      !payload.username ||
      !payload.password ||
      !payload.email ||
      !payload.user_role
    ) {
      isValid = false;
      setMessage("Please fill in all required fields.", "red-500");
    } else if (!emailPattern.test(payload.email)) {
      isValid = false;
      setMessage("Please enter a valid email address.", "red-500");
    } else {
      resetMessage();
    }
    if (isValid) {
      if (payload.user_role === "customer") {
        if (
          !payload.first_name ||
          !payload.last_name ||
          !payload.address ||
          !payload.phone_no ||
          !payload.credit_card_no
        ) {
          isValid = false;
          setMessage("Please fill in all required fields.", "red-500");
        } else {
          resetMessage();
        }
      } else if (payload.user_role === "airline") {
        if (!payload.name || !payload.country) {
          isValid = false;
          setMessage("Please fill in all required fields.", "red-500");
        } else {
          resetMessage();
        }
      }
    }

    return isValid;
  };

  const submitForm = async () => {
    const username = payload.username;
    const password = payload.password;
    const email = payload.email;
    const userRole = payload.user_role;

    const formData = {
      username,
      password,
      email,
      user_role: userRole,
    };

    if (userRole === "customer") {
      const firstName = payload.first_name;
      const lastName = payload.last_name;
      const address = payload.address;
      const phoneNo = payload.phone_no;
      const creditCardNo = payload.credit_card_no;

      formData.first_name = firstName;
      formData.last_name = lastName;
      formData.address = address;
      formData.phone_no = phoneNo;
      formData.credit_card_no = creditCardNo;
    } else if (userRole === "airline") {
      const name = payload.name;
      const country = payload.country;

      formData.name = name;
      formData.country = country;
    }

    await axios
      .post(CONSTANT.server + "register", formData)
      .then((response) => {
        if (response.data?.message) {
          setMessage(response.data?.message, "red-500");
        } else {
          sessionStorage.setItem(
            "loggedin",
            JSON.stringify({
              data: response.data,
            })
          );
          if (response?.data?.user_role?.role_name === "airline") {
            window.location.href = "/myFlights";
          } else {
            window.location.href = "/";
          }
        }
      })
      .catch((error) => {
        console.error(error);
        setMessage("Registration failed. Please try again later.", "red-500");
      });
  };

  return (
    <main>
      {/* CONTENT HERE */}
      <div className="row m-0 p-0">
        <div
          className="col-lg-5 m-0 p-0 overflow-hidden"
          style={{ maxHeight: "100vh" }}
        >
          <img
            className="img-fluid w-100"
            src="https://images.unsplash.com/photo-1583150647472-d239652a12f5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=627&q=80"
          />
        </div>
        <div className="col-lg-7 p-5 justify-content-center align-items-center d-flex">
          <div
            id="registration-form"
            className="w-100 needs-validation"
            noValidate
          >
            <div className="mb-5 d-flex justify-content-center align-items-center flex-column">
              <h1 className="display-6">Registeration</h1>
              <Link to="/" className="text-decoration-none text-dark">
                <span className="h3">Flight Management System</span>
              </Link>
            </div>
            <div className="row my-3">
              <div className="col-6">
                <label htmlFor="username" className="form-label">
                  Username
                </label>
                <input
                  type="text"
                  className="form-control"
                  name="username"
                  value={payload.username}
                  onChange={changePayload}
                />
              </div>
              <div className="col-6">
                <label htmlFor="password" className="form-label">
                  Password
                </label>
                <input
                  type="password"
                  className="form-control"
                  name="password"
                  value={payload.password}
                  onChange={changePayload}
                />
              </div>
            </div>
            <div className="row my-3">
              <div className="col-6">
                <label htmlFor="email" className="form-label">
                  Email
                </label>
                <input
                  type="email"
                  className="form-control"
                  name="email"
                  value={payload.email}
                  onChange={changePayload}
                />
              </div>
              <div className="col-6">
                <label className="form-label">User Role</label>
                <select
                  className="form-select"
                  name="user_role"
                  value={payload.user_role}
                  onChange={changePayload}
                >
                  <option value>Choose User Role</option>
                  <option value="customer">Customer</option>
                  <option value="airline">Airline</option>
                </select>
              </div>
            </div>
            {payload.user_role === "customer" ? (
              <div id="customer-fields">
                <div className="row my-3">
                  <div className="col-6">
                    <label htmlFor="first_name" className="form-label">
                      First Name
                    </label>
                    <input
                      type="text"
                      className="form-control"
                      name="first_name"
                      value={payload.first_name}
                      onChange={changePayload}
                      id="first_name"
                    />
                  </div>
                  <div className="col-6">
                    <label htmlFor="last_name" className="form-label">
                      Last Name
                    </label>
                    <input
                      type="text"
                      className="form-control"
                      name="last_name"
                      value={payload.last_name}
                      onChange={changePayload}
                      id="last_name"
                    />
                  </div>
                </div>
                <div className="row my-3">
                  <div className="col-12">
                    <label htmlFor="address" className="form-label">
                      Address
                    </label>
                    <input
                      type="text"
                      className="form-control"
                      name="address"
                      value={payload.address}
                      onChange={changePayload}
                      id="address"
                    />
                  </div>
                </div>
                <div className="row my-3">
                  <div className="col-6">
                    <label htmlFor="phone_no" className="form-label">
                      Phone Number
                    </label>
                    <input
                      type="number"
                      className="form-control"
                      name="phone_no"
                      value={payload.phone_no}
                      onChange={changePayload}
                      id="phone_no"
                    />
                  </div>
                  <div className="col-6">
                    <label htmlFor="credit_card_no" className="form-label">
                      Credit Card Number
                    </label>
                    <input
                      type="text"
                      className="form-control"
                      id="credit_card_no"
                      name="credit_card_no"
                      value={payload.credit_card_no}
                      onChange={changePayload}
                    />
                  </div>
                </div>
              </div>
            ) : (
              ""
            )}
            {payload.user_role === "airline" ? (
              <div id="airline-fields">
                <div className="row my-3">
                  <div className="col-6">
                    <label htmlFor="name" className="form-label">
                      Name
                    </label>
                    <input
                      type="text"
                      className="form-control"
                      id="name"
                      name="name"
                      value={payload.name}
                      onChange={changePayload}
                    />
                  </div>
                  <div className="col-6">
                    <label htmlFor="country" className="form-label">
                      Country
                    </label>
                    <select
                      className="form-select"
                      id="country"
                      name="country"
                      value={payload.country}
                      onChange={changePayload}
                    >
                      <option value={""}>Select Country</option>
                      {countries.map((one, i) => {
                        return <option value={one.id}>{one.name}</option>;
                      })}
                    </select>
                  </div>
                </div>
              </div>
            ) : (
              ""
            )}
            <div className="mt-5 text-center">
              <button
                onClick={() => {
                  if (validateForm()) {
                    submitForm();
                  }
                }}
                className="btn btn-success bg-success w-25"
              >
                Register
              </button>
              <div className="mt-5 text-danger" id="error" />
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Register;
