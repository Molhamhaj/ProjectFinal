import axios from "axios";
import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import { CONSTANT, resetMessage, setMessage } from "../CONSTANT";
import UserData from "../contexts/UserData";

export default function MyTickets() {
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
  const groupByFlight = (data) => {
    const groupedData = {};
    data.forEach((booking) => {
      const flightId = booking.flight.id;
      if (groupedData[flightId]) {
        groupedData[flightId].number_of_tickets++;
      } else {
        groupedData[flightId] = {
          id: booking.flight.id,
          number_of_tickets: 1,
          flight: booking.flight,
        };
      }
    });
    return Object.values(groupedData);
  };

  const fetchFlights = async () => {
    await axios
      .get(CONSTANT.server + `ticketsById`, {
        headers: {
          Authorization: `Token ${session?.personal?.username} ${session?.role}`,
        },
      })
      .then((response) => {
        setFlights(groupByFlight(response.data));
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

  return (
    <main>
      <h1 className="display-4 fst-italic text-center mt-5 mb-2">
        Your Tickets
      </h1>
      <div className="album py-5 bg-light mt-5">
        <div className="container">
          <div
            className="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3"
            id="flight_box"
          >
            {flights.map((ticket, one) => {
              return (
                <div class="col">
                  <div class="card shadow-sm">
                    <div class="card-body">
                      <h1 class="display-6 mb-2">
                        {ticket.flight.origin_country.name} to{" "}
                        {ticket.flight.destination_country.name}
                      </h1>
                      <small class="text-muted">
                        via {ticket.flight.airline.name}
                      </small>
                      <p class="card-text mb-2">
                        <strong>Departure Time: </strong>
                        {new Date(
                          ticket.flight.departure_time
                        ).toLocaleString()}
                      </p>
                      <p class="card-text mb-2">
                        <strong>Landing Time: </strong>
                        {new Date(ticket.flight.landing_time).toLocaleString()}
                      </p>
                      <div class="mt-3 d-flex justify-content-between align-items-center">
                        <div class="btn-group">
                          {getFlightStatus(ticket.flight.departure_time)}
                        </div>
                        <small class="text-muted">
                          {ticket.number_of_tickets} ticket
                          {ticket.number_of_tickets === 1 ? "" : "s"} booked
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
                No tickets available.
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
