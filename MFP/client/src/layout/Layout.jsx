import React, { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import UserData from "../contexts/UserData";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { checkLoginFromNonLogin } from "../CONSTANT";
export default function Layout(props) {
  let navigate = useNavigate();
  // ------------------
  // SESSION - END
  // ------------------
  let __init_session = {
    personal: {
      id: "",
      email: "",
      username: "",
    },
    isLoggedIn: false,
    role: "",
  };
  const [session, setSession] = useState(__init_session);

  useEffect(() => {
    let sessionData = JSON.parse(sessionStorage.getItem("loggedin"));
    if (sessionData) {
      setSession({
        ...__init_session,
        personal: sessionData.data,
        isLoggedIn: true,
        role: sessionData?.data?.user_role?.role_name,
      });
    }
  }, []);

  const value = { session, setSession };
  // ------------------
  // SESSION - END
  // ------------------
  useEffect(() => {
    if (session.isLoggedIn) {
      if (props.login && checkLoginFromNonLogin()) {
        navigate("/login");
      } else {
        if (props.customer && session.role !== "customer") {
          navigate("/");
        }
        if (props.airline && session.role !== "airline") {
          navigate("/");
        }
      }
    }
  }, [session]);

  return (
    <>
      <UserData.Provider value={value}>
        {props.single ?? (
          <Navbar
            isLoggedIn={session.isLoggedIn}
            __init_session={__init_session}
            setSession={setSession}
            session={session}
          />
        )}
        <div className="">{props.children}</div>
        {props.single ?? <Footer />}
      </UserData.Provider>
    </>
  );
}
