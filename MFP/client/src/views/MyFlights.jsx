import axios from "axios";
import React, { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { CONSTANT, resetMessage, setMessage } from "../CONSTANT";
import UserData from "../contexts/UserData";

export default function MyFlights() {
  let navigate = useNavigate();
  const { session, setSession } = useContext(UserData);
  const [flights, setFlights] = useState([]);
  const getFlightStatus = (departureTime) => {
    // Convert the departure time string to a Date object
    const departureDate = new Date(departureTime);

    // Get the current time
    const now = new Date();

    // Calculate the time difference between the current time and the departure time in hours
    const hoursDifference = (departureDate - now) / (1000 * 60 * 60);

    // If the flight has already departed, return "Flown"
    if (hoursDifference < 0) {
      return <span class="text-danger">Expired</span>;
    }

    // If the flight is departing within the next hour, return "On the way"
    if (hoursDifference < 1) {
      return <span class="text-success">Upcoming</span>;
    }

    // Otherwise, return "Is about to fly within [calculated] hours"
    return (
      <span class="text-dark">
        About to fly within {Math.floor(hoursDifference)} hours
      </span>
    );
  };

  const fetchFlights = async () => {
    await axios
      .get(CONSTANT.server + `myFlights`, {
        headers: {
          Authorization: `Token ${session?.personal?.username} ${session?.role}`,
        },
      })
      .then((response) => {
        setFlights(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    if (session.isLoggedIn) {
      fetchFlights();
    }
  }, [session]);

  const deleteFlight = async (flightId) => {
    // Send a DELETE request to the API endpoint with the flight ID as a parameter
    await axios
      .delete(`${CONSTANT.server}myFlights/${flightId}`, {
        headers: {
          Authorization: `Token ${session?.personal?.username} ${session?.role}`,
        },
      })
      .then(function (response) {
        fetchFlights();
      })
      .catch(function (error) {
        console.error("Failed to delete flight:", error);
      });
  };

  return (
    <main>
      <div className="d-flex justify-content-around align-items-center mt-5 mb-2">
        <h1 className="display-6 fst-italic text-center">Your Flights</h1>
        <Link to="/addFlight" className="btn btn-outline-success">
          Add Flight
        </Link>
      </div>

      <div className="album py-5 bg-light mt-5">
        <div className="container">
          <div
            className="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3"
            id="flight_box"
          >
            {flights.map((flight, one) => {
              return (
                <div class="col">
                  <div class="card shadow-sm">
                    <div class="card-body">
                      <h1 class="display-6 mb-2">
                        {flight.origin_country.name} to{" "}
                        {flight.destination_country.name}
                      </h1>
                      <small class="text-muted">
                        via {flight.airline.name}
                      </small>
                      <p class="card-text mb-2">
                        <strong>Departure Time: </strong>
                        {new Date(flight.departure_time).toLocaleString()}
                      </p>
                      <p class="card-text mb-2">
                        <strong>Landing Time: </strong>
                        {new Date(flight.landing_time).toLocaleString()}
                      </p>
                      <p class="card-text mb-2">
                        <strong>Status: </strong>
                        {getFlightStatus(flight.departure_time)}
                      </p>
                      <div class="mt-3 d-flex justify-content-between align-items-center">
                        <div className="btn-group">
                          <button
                            onClick={() => {
                              deleteFlight(flight.id);
                            }}
                            className="btn btn-sm btn-outline-danger delete_flight"
                          >
                            Delete
                          </button>
                          <button
                            onClick={() => {
                              navigate(`/addFlight/${flight.id}`);
                            }}
                            className="btn btn-sm btn-outline-success delete_flight"
                          >
                            Update
                          </button>
                        </div>
                        <small class="text-muted">
                          {flight.remaining_tickets} ticket
                          {flight.remaining_tickets === 1 ? "" : "s"} left
                        </small>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
            {flights.length <= 0 ? (
              <div
                className="alert alert-secondary w-100 text-center"
                role="alert"
              >
                No flights available.
              </div>
            ) : (
              ""
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
