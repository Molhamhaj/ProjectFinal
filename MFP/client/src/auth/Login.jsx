import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";
import {
  CONSTANT,
  setMessage,
  resetMessage,
  checkLoginFromLogin,
} from "../CONSTANT";

const Login = () => {
  const navigate = useNavigate();
  useEffect(() => {
    if (checkLoginFromLogin()) {
      navigate("/");
    }
  }, []);
  const init__payload = {
    username: "",
    password: "",
  };
  const [payload, setPayload] = useState(init__payload);
  const changePayload = (e) => {
    setPayload({
      ...payload,
      [e.target.name]: e.target.value,
    });
  };
  const validateForm = () => {
    let isValid = true;
    const username = payload.username;
    const password = payload.password;

    if (!username || !password) {
      isValid = false;
      setMessage("Please fill in all required fields.", "red-500");
    } else {
      resetMessage();
    }
    return isValid;
  };

  // Function to submit form data
  const submitForm = () => {
    const username = payload.username;
    const password = payload.password;

    const formData = {
      username,
      password,
    };

    axios
      .post(CONSTANT.server + "login", formData)
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
        setMessage("Login failed. Please try again later.", "red-500");
      });
  };

  return (
    <main>
      {/* CONTENT HERE */}
      <div className="row m-0 p-0">
        <div className="col-lg-7 p-5 justify-content-center align-items-center d-flex">
          <div
            id="registration-form"
            className="w-75 needs-validation"
            noValidate
          >
            <div className="mb-5 d-flex justify-content-center align-items-center flex-column">
              <h1 className="display-6">Login</h1>
              <Link to="/" className="text-decoration-none text-dark">
                <span className="h3">Flight Management System</span>
              </Link>
            </div>
            <div className="row my-3">
              <div className="col-12 my-3">
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
              <div className="col-12">
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
            <div className="mt-5 text-center">
              <button
                onClick={() => {
                  if (validateForm()) {
                    submitForm();
                  }
                }}
                type="button"
                className="btn btn-success bg-success w-25"
              >
                Login
              </button>
              <div className="mt-5 text-danger" id="error" />
            </div>
          </div>
        </div>
        <div
          className="col-lg-5 m-0 p-0 overflow-hidden"
          style={{ maxHeight: "100vh" }}
        >
          <img
            className="img-fluid w-100"
            src="https://images.unsplash.com/photo-1559268950-2d7ceb2efa3a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8Mnx8fGVufDB8fHx8&w=1000&q=80"
          />
        </div>
      </div>
    </main>
  );
};

export default Login;
