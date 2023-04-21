import axios from "axios";
import { CONSTANT, setMessage } from "../CONSTANT";
import React, { useState, useEffect, useContext } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import UserData from "../contexts/UserData";

export default function AddFlight() {
  const navigate = useNavigate();
  const { flight_id: flight_id } = useParams();
  const { session, setSession } = useContext(UserData);

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

  const init__payload = {
    originCountry: "",
    destinationCountry: "",
    departureTime: "",
    landingTime: "",
    remainingTickets: "",
  };
  const [payload, setPayload] = useState(init__payload);
  const changePayload = (e) => {
    setPayload({
      ...payload,
      [e.target.name]: e.target.value,
    });
  };

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
          let flight = responce.data;
          setPayload({
            originCountry: flight.origin_country.id,
            destinationCountry: flight.destination_country.id,
            departureTime: flight.departure_time.toString().slice(0, -1),
            landingTime: flight.landing_time.toString().slice(0, -1),
            remainingTickets: flight.remaining_tickets,
            id: flight.id,
          });
          setIsUpdate(true);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const [isUpdate, setIsUpdate] = useState(false);

  useEffect(() => {
    if (session.isLoggedIn && flight_id !== "") {
      searchFlight();
    }
  }, [session]);

  const addFlight = async () => {
    // Validate form data
    var originCountry = payload.originCountry;
    var destinationCountry = payload.destinationCountry;
    var departureTime = payload.departureTime;
    var landingTime = payload.landingTime;
    var remainingTickets = payload.remainingTickets;

    if (
      originCountry == "" ||
      destinationCountry == "" ||
      departureTime == "" ||
      landingTime == "" ||
      remainingTickets == ""
    ) {
      setMessage("All fields are required", "red-500");
      return;
    }

    if (remainingTickets < 1) {
      setMessage("Remaining Tickets should be at least 1", "red-500");
      return;
    }

    if (departureTime < Date.now()) {
      setMessage("Departure time cannot be in the past", "red-500");
      return;
    }

    if (departureTime >= landingTime) {
      setMessage("Departure time must be earlier than landing time", "red-500");
      return;
    }

    if (originCountry === destinationCountry) {
      setMessage(
        "Origin and destination cannot be the same country",
        "red-500"
      );
      return;
    }

    let toSend = {
      origin_country: originCountry,
      destination_country: destinationCountry,
      departure_time: departureTime,
      landing_time: landingTime,
      remaining_tickets: remainingTickets,
    };

    if (isUpdate) {
      // Send POST request to API endpoint
      await axios
        .put(
          `${CONSTANT.server}flights`,
          {
            ...toSend,
            id: payload.id,
          },
          {
            headers: {
              Authorization: `Token ${session?.personal?.username} ${session?.role}`,
            },
          }
        )
        .then(function (response) {
          if (response.data?.message) {
            setMessage(response.data?.message, "red-500");
          } else {
            navigate("/myFlights");
          }
        })
        .catch(function (error) {
          setMessage("Failed to update flight!", "red-500");
          console.error(error);
        });
    } else {
      // Send POST request to API endpoint
      await axios
        .post(`${CONSTANT.server}flights`, toSend, {
          headers: {
            Authorization: `Token ${session?.personal?.username} ${session?.role}`,
          },
        })
        .then(function (response) {
          if (response.data?.message) {
            setMessage(response.data?.message, "red-500");
          } else {
            navigate("/myFlights");
          }
        })
        .catch(function (error) {
          setMessage("Failed to add flight!", "red-500");
          console.error(error);
        });
    }
  };
  return (
    <main>
      {/* Book Now */}
      <div className="d-flex justify-content-around align-items-center mt-5 mb-2">
        <h1 className="display-6 fst-italic text-center">
          {isUpdate ? "Update" : "Add"} Flight
        </h1>
      </div>
      <div className="album py-5 bg-light mt-5">
        <div className="container">
          <div id="add_flight_form">
            <div className="row">
              <div className="col-md-6">
                <div className="form-group">
                  <label htmlFor="origin-country">Origin Country</label>
                  <select
                    className="form-select"
                    id="origin-country"
                    name="originCountry"
                    value={payload.originCountry}
                    onChange={changePayload}
                  >
                    <option value={""}>Select Country</option>
                    {countries.map((one, i) => {
                      return <option value={one.id}>{one.name}</option>;
                    })}
                  </select>
                </div>
              </div>
              <div className="col-md-6">
                <div className="form-group">
                  <label htmlFor="destination-country">
                    Destination Country
                  </label>
                  <select
                    className="form-select"
                    id="destination-country"
                    name="destinationCountry"
                    value={payload.destinationCountry}
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
            <div className="row mt-4">
              <div className="col-md-4">
                <div className="form-group">
                  <label htmlFor="departure-time">Departure Time</label>
                  <input
                    type="datetime-local"
                    className="form-control"
                    id="departure-time"
                    name="departureTime"
                    value={payload.departureTime}
                    onChange={changePayload}
                  />
                </div>
              </div>
              <div className="col-md-4">
                <div className="form-group">
                  <label htmlFor="landing-time">Landing Time</label>
                  <input
                    type="datetime-local"
                    className="form-control"
                    id="landing-time"
                    name="landingTime"
                    value={payload.landingTime}
                    onChange={changePayload}
                  />
                </div>
              </div>
              <div className="col-md-4">
                <div className="form-group">
                  <label htmlFor="remaining-tickets">Remaining Tickets</label>
                  <input
                    type="number"
                    className="form-control"
                    id="remaining-tickets"
                    name="remainingTickets"
                    value={payload.remainingTickets}
                    onChange={changePayload}
                  />
                </div>
              </div>
            </div>
            <div className="mt-5 d-flex flex-column justify-content-center align-items-center">
              <button
                onClick={addFlight}
                className="btn bg-success btn-success"
              >
                {isUpdate ? "Update" : "Add"}
              </button>
              <div className="mt-5 text-danger" id="error" />
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
