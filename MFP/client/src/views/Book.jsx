import axios from "axios";
import UserData from "../contexts/UserData";
import React, { useState, useEffect, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { CONSTANT, setMessage } from "../CONSTANT";
export default function Book() {
  const { session, setSession, refreshSession } = useContext(UserData);
  const { flight_id: flight_id } = useParams();
  let navigate = useNavigate();

  const [data, setData] = useState({
    id: "",
    airline: {
      id: "",
      user: {
        id: "",
        username: "",
        email: "",
        user_role: {
          id: "",
          role_name: "",
          thumbnail: "",
        },
      },
      country: {
        id: "",
        name: "",
        flag: "",
      },
      name: "",
    },
    origin_country: {
      id: "",
      name: "",
      flag: "",
    },
    destination_country: {
      id: "",
      name: "",
      flag: "",
    },
    departure_time: "",
    landing_time: "",
    remaining_tickets: 0,
  });

  const searchFlight = async () => {
    await axios
      .get(CONSTANT.server + `flightById/${flight_id}`, {
        headers: {
          Authorization: `Token ${session?.personal?.username} ${session?.role}`,
        },
      })
      .then((responce) => {
        if (responce.data?.message) {
          navigate("/");
        } else {
          setData(responce.data);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    if (session.isLoggedIn) {
      searchFlight();
    }
  }, [session]);

  const book = async () => {
    await axios
      .post(
        CONSTANT.server + `book`,
        {
          flight: flight_id,
        },
        {
          headers: {
            Authorization: `Token ${session?.personal?.username} ${session?.role}`,
          },
        }
      )
      .then((responce) => {
        if (responce.data.message) {
          setMessage("Not enough tickets!", "red-500");
        } else {
          setData({
            ...data,
            remaining_tickets: data.remaining_tickets - 1,
          });
          setMessage("Ticket booked!", "green-500");
        }
        setTimeout(() => {
          navigate("/myTickets");
        }, 2000);
      })
      .catch((error) => {
        console.log(error);
      });
  };
  const redirectToHome = () => {
    navigate("/");
  };

  return (
    <main className="">
      {data.id !== "" ? (
        <div id="flight-info" className="rounded my-5 py-3">
          <div className="bg-light flex-column d-flex justify-content-center align-items-center">
            <div className="mb-2 w-100 d-flex justify-content-center align-items-center flex-column">
              <div className="display-4 fst-italic d-flex justify-content-center align-items-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="#000000"
                  width="80px"
                  height="80px"
                  viewBox="-2.5 0 19 19"
                  className="cf-icon-svg"
                >
                  <path d="M12.382 5.304 10.096 7.59l.006.02L11.838 14a.908.908 0 0 1-.211.794l-.573.573a.339.339 0 0 1-.566-.08l-2.348-4.25-.745-.746-1.97 1.97a3.311 3.311 0 0 1-.75.504l.44 1.447a.875.875 0 0 1-.199.79l-.175.176a.477.477 0 0 1-.672 0l-1.04-1.039-.018-.02-.788-.786-.02-.02-1.038-1.039a.477.477 0 0 1 0-.672l.176-.176a.875.875 0 0 1 .79-.197l1.447.438a3.322 3.322 0 0 1 .504-.75l1.97-1.97-.746-.744-4.25-2.348a.339.339 0 0 1-.08-.566l.573-.573a.909.909 0 0 1 .794-.211l6.39 1.736.02.006 2.286-2.286c.37-.372 1.621-1.02 1.993-.65.37.372-.279 1.622-.65 1.993z" />
                </svg>
                {data.origin_country.name} to {data.destination_country.name}
              </div>
              <span className>
                via <span className="lead">{data.airline.name}</span>
              </span>
            </div>
            <hr />
            <div className="my-2 w-100 d-flex justify-content-center align-items-center flex-column">
              <div className="mb-3 h4 fst-italic d-flex justify-content-center align-items-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="40px"
                  height="40px"
                  className="me-4"
                  viewBox="0 0 512 512"
                >
                  <path
                    fill="#000000"
                    d="M442.6 67.37c-1.6.01-3.2.06-4.8.16-13.2.73-26.9 3.8-36.8 8.74l-.2.12-281 120.21-4.1-2.6c-20.62-13.3-42.15-26.8-73.84-32.1 2.07 4.7 4.64 9.9 7.76 15.5 6.69 11.9 15.26 25.3 23.75 37.6 8.49 12.2 16.96 23.3 23.21 30.4 2.41 2.8 4.02 4.3 5.42 5.6l172.2-68.6-1.2 14.4c-3.7 44.4-11.3 89.6-23.5 135.7l28.5-19c32.6-51.5 43.5-87.2 71-157.3l1.2-3 91.5-50.5h.2c22.9-11.49 32.8-21.65 34.4-25.36.8-1.86.6-1.37.2-2.04-.4-.66-2.3-2.39-5.8-3.85-5.4-2.2-13.8-3.72-23.3-4.03-1.5-.05-3.2-.07-4.8-.05zm-283 11.74l-22.1 4.4L222 133.3l60.1-25.7C248 96.96 210.8 86.98 159.6 79.11zM32 439v18h448v-18H32z"
                  />
                </svg>
                Departure
              </div>
              <span className="display-6">
                {new Date(data.departure_time).toLocaleString()}
              </span>
            </div>
            <hr />
            <div className="my-2 w-100 d-flex justify-content-center align-items-center flex-column">
              <div className="mb-3 h4 fst-italic d-flex justify-content-center align-items-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="40px"
                  height="40px"
                  className="me-4"
                  viewBox="0 0 512 512"
                >
                  <path
                    fill="#000000"
                    d="M86.48 31.83c-1.96 4.68-4.03 10.14-5.96 16.22-4.14 13.05-8.05 28.48-11.15 43.03-3.1 14.52-5.39 28.32-6.34 37.82-.35 3.6-.35 5.8-.35 7.7l167.92 78.6-11.4 9c-34.8 27.7-73 53-115.1 75.7l33.4 7.8c60-11.4 93.5-27.9 163.4-55.9l3-1.2 99.4 32.3.2.1c24 8.8 38.2 9.1 42 7.8 1.9-.7 1.4-.5 1.6-1.3.2-.8.2-3.3-1.2-6.9-2.7-7.2-10.1-17.6-19.6-26.7-9.5-9.1-21.2-17-31.5-20.9l-.3-.1-279.9-122.6-.8-4.6c-4.6-24.2-9.5-49.13-27.32-75.87zM209.2 47.9l21.5 95.6 59.8 26.3c-15.5-32.1-33.8-66.1-63.1-108.83L209.2 47.9zM32 439v18h448v-18H32z"
                  />
                </svg>
                Landing
              </div>
              <span className="display-6">
                {new Date(data.landing_time).toLocaleString()}
              </span>
            </div>
            <hr />
            <div className="my-2 w-100 d-flex justify-content-center align-items-center flex-column">
              <div className="mb-3 h4 fst-italic d-flex justify-content-center align-items-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="40px"
                  height="40px"
                  className="me-4"
                  viewBox="0 0 20 20"
                >
                  <rect x={0} fill="none" width={20} height={20} />
                  <g>
                    <path d="M20 6.38L18.99 9.2v-.01c-.52-.19-1.03-.16-1.53.08s-.85.62-1.04 1.14-.16 1.03.07 1.53c.24.5.62.84 1.15 1.03v.01l-1.01 2.82-15.06-5.38.99-2.79c.52.19 1.03.16 1.53-.08.5-.23.84-.61 1.03-1.13s.16-1.03-.08-1.53c-.23-.49-.61-.83-1.13-1.02L4.93 1zm-4.97 5.69l1.37-3.76c.12-.31.1-.65-.04-.95s-.39-.53-.7-.65L8.14 3.98c-.64-.23-1.37.12-1.6.74L5.17 8.48c-.24.65.1 1.37.74 1.6l7.52 2.74c.14.05.28.08.43.08.52 0 1-.33 1.17-.83zM7.97 4.45l7.51 2.73c.19.07.34.21.43.39.08.18.09.38.02.57l-1.37 3.76c-.13.38-.58.59-.96.45L6.09 9.61c-.39-.14-.59-.57-.45-.96l1.37-3.76c.1-.29.39-.49.7-.49.09 0 .17.02.26.05zm6.82 12.14c.35.27.75.41 1.2.41H16v3H0v-2.96c.55 0 1.03-.2 1.41-.59.39-.38.59-.86.59-1.41s-.2-1.02-.59-1.41-.86-.59-1.41-.59V10h1.05l-.28.8 2.87 1.02c-.51.16-.89.62-.89 1.18v4c0 .69.56 1.25 1.25 1.25h8c.69 0 1.25-.56 1.25-1.25v-1.75l.83.3c.12.43.36.78.71 1.04zM3.25 17v-4c0-.41.34-.75.75-.75h.83l7.92 2.83V17c0 .41-.34.75-.75.75H4c-.41 0-.75-.34-.75-.75z" />
                  </g>
                </svg>
                Remaining Tickets
              </div>
              <span className="display-6">{data.remaining_tickets}</span>
            </div>
            <button
              onClick={
                session.isLoggedIn
                  ? session.role === "customer"
                    ? book
                    : redirectToHome
                  : redirectToHome
              }
              className={`btn-${
                session.isLoggedIn
                  ? session.role === "customer"
                    ? "success"
                    : "danger"
                  : "danger"
              } btn my-3`}
              id="confirm-booking"
            >
              {session.isLoggedIn
                ? session.role === "customer"
                  ? "Confirm Booking"
                  : "Not Eligible"
                : "Login to Book"}
            </button>
            <div className="my-3" id="error" />
          </div>
        </div>
      ) : (
        ""
      )}
    </main>
  );
}
