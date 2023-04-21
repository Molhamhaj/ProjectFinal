import axios from "axios";
import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import { CONSTANT, resetMessage, setMessage } from "../CONSTANT";
import UserData from "../contexts/UserData";

export default function Home() {
  const { session, setSession } = useContext(UserData);
  const [filters, setFilter] = useState({
    origin_country_id: "",
    destination_country_id: "",
    date: "",
  });
  const changeFilters = (e) => {
    setFilter({
      ...filters,
      [e.target.name]: e.target.value,
    });
  };

  const [countries, setCountries] = useState([]);
  const [flights, setFlights] = useState([]);

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

  const fetchFlights = async () => {
    await axios
      .get(CONSTANT.server + `flights`)
      .then((response) => {
        setFlights(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    fetchCountries();
    fetchFlights();
  }, []);

  const filterFlights = () => {
    resetMessage();
    const origin_country_id = filters.origin_country_id;
    const destination_country_id = filters.destination_country_id;
    const date = filters.date;

    if (!origin_country_id || !destination_country_id || !date) {
      setMessage("Please fill all the fields");
      return;
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const selectedDate = new Date(date);

    if (selectedDate.getTime() < today.getTime()) {
      setMessage("Departure date cannot be less than today's date");
      return;
    }

    axios
      .post(`${CONSTANT.server}filter`, {
        origin_country_id,
        destination_country_id,
        date,
      })
      .then((response) => {
        setFlights(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <main>
      <section className="py-5 text-center container __hero_main w-100">
        <div className="row py-lg-5 w-100">
          <div className="col-lg-6 col-md-8 mx-auto">
            <h1 className="h1 fw-normal text-light">
              Let's Fly Around The World
            </h1>
            <p className="lead text-muted fw-normal">
              Want to find specific flights? Search now.
            </p>
          </div>
        </div>
      </section>
      <div className="container w-100 py-5">
        <div className="card bg-light rounded">
          <div className="card-body">
            <div id="filter_form">
              <div className="row g-3">
                <div className="col">
                  <label htmlFor="origin_country_id" className="form-label">
                    Origin Country
                  </label>
                  <select
                    id="origin_country_id"
                    name="origin_country_id"
                    className="form-select"
                    value={filters.origin_country_id}
                    onChange={changeFilters}
                  >
                    <option value={""}>Select Country</option>
                    {countries.map((one, i) => {
                      return <option value={one.id}>{one.name}</option>;
                    })}
                  </select>
                </div>
                <div className="col">
                  <label
                    htmlFor="destination_country_id"
                    className="form-label"
                  >
                    Destination Country
                  </label>
                  <select
                    id="destination_country_id"
                    name="destination_country_id"
                    className="form-select"
                    value={filters.destination_country_id}
                    onChange={changeFilters}
                  >
                    <option value={""}>Select Country</option>
                    {countries.map((one, i) => {
                      return <option value={one.id}>{one.name}</option>;
                    })}
                  </select>
                </div>
                <div className="col">
                  <label htmlFor="date" className="form-label">
                    Departure Date
                  </label>
                  <input
                    type="date"
                    name="date"
                    value={filters.date}
                    onChange={changeFilters}
                    className="form-control"
                  />
                </div>
              </div>
              <div className="text-center my-4">
                <button
                  onClick={filterFlights}
                  className="btn btn-outline-success"
                >
                  Search
                </button>
              </div>
            </div>
          </div>
        </div>
        <div
          style={{ display: "none" }}
          className="mt-3 alert alert-danger"
          id="error"
          role="alert"
        ></div>
      </div>

      <div className="album py-5 bg-light">
        <div className="container">
          <div
            className="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3"
            id="flight_box"
          >
            {flights.map((flight, one) => {
              return (
                <div class="col">
                  <div class="card shadow-sm">
                    <Link
                      to={`/${
                        session?.isLoggedIn ? `book/${flight.id}` : `login`
                      }`}
                    >
                      <img
                        src={`https://source.unsplash.com/random/400x250/?airplanes,id_${flight.id}`}
                        class="card-img-top rounded-top"
                        alt="Flight Image"
                      />
                    </Link>

                    <div class="card-body">
                      <h1 class="display-6 mb-2">
                        {flight.origin_country.name} to{" "}
                        {flight.destination_country.name}
                      </h1>
                      <small class="text-muted">{flight.airline.name}</small>
                      <p class="card-text mb-2">
                        <strong>Departure Time: </strong>
                        {new Date(flight.departure_time).toLocaleString()}
                      </p>
                      <p class="card-text mb-2">
                        <strong>Landing Time: </strong>
                        {new Date(flight.landing_time).toLocaleString()}
                      </p>
                      <div class="mt-3 d-flex justify-content-between align-items-center">
                        <div class="btn-group">
                          <Link
                            to={`/${
                              session?.isLoggedIn
                                ? `book/${flight.id}`
                                : `login`
                            }`}
                            class="btn btn-sm btn-outline-success"
                          >
                            {session?.isLoggedIn ? `Book Now` : "Login to Book"}
                          </Link>
                        </div>
                        <small class="text-muted">
                          {flight.remaining_tickets} tickets left
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
