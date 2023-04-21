from abc import ABC
import datetime
from .models import User, AirlineCompany, Flight, Customer, Country, UserRoles, Ticket, Administrator
from .utils import DAL
from django.contrib.auth.hashers import make_password, check_password


class FacadeBase(ABC):
    """
    This is an abstract base class that provides a facade for the application's data access layer (DAL).
    It defines methods for accessing different entities such as flights, airlines, countries, and users.
    """

    def __init__(self):
        """
        Initializes the FacadeBase object and creates a DAL object for data access.
        """
        self.dal = DAL()

    def get_all_flights(self):
        """
        Retrieves all the flights from the database.
        Returns:
            A list of Flight objects.
        """
        return self.dal.get_all(Flight)

    def get_flight_by_id(self, id):
        """
        Retrieves a flight by its ID from the database.
        Args:
            id: An integer ID of the flight to be retrieved.
        Returns:
            A Flight object if found, otherwise None.
        """
        if id is not None and isinstance(id, int):
            return self.dal.get_by_id(Flight, id)
        return None

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        """
        Retrieves flights from the database based on the given parameters.
        Args:
            origin_country_id: An integer ID of the origin country.
            destination_country_id: An integer ID of the destination country.
            date: A date object representing the departure date.
        Returns:
            A list of Flight objects that match the given parameters.
        """
        if origin_country_id is not None and isinstance(origin_country_id, int) and destination_country_id is not None and isinstance(destination_country_id, int) and date is not None:
            return self.dal.get_flights_by_parameters(origin_country_id, destination_country_id, date)
        return []

    def get_all_airlines(self):
        """
        Retrieves all the airline companies from the database.
        Returns:
            A list of AirlineCompany objects.
        """
        return self.dal.get_all(AirlineCompany)

    def get_airline_by_id(self, id):
        """
        Retrieves an airline company by its ID from the database.
        Args:
            id: An integer ID of the airline company to be retrieved.
        Returns:
            An AirlineCompany object if found, otherwise None.
        """
        if id is not None and isinstance(id, int):
            return self.dal.get_by_id(AirlineCompany, id)
        return None

    def get_airline_by_parameters(self, country_id, username):
        """
        Retrieves an airline company by its country and username from the database.
        Args:
            country_id: An integer ID of the country where the airline is registered.
            username: A string representing the username of the airline.
        Returns:
            An AirlineCompany object if found, otherwise None.
        """
        if country_id is not None and isinstance(country_id, int) and username is not None and isinstance(username, str):
            airline = self.dal.get_airline_by_username(username)
            if airline and airline.country.id == country_id:
                return airline
        return None

    def get_all_countries(self):
        """
        Retrieves all the countries from the database.
        Returns:
            A list of Country objects.
        """
        return self.dal.get_all(Country)

    def get_country_by_id(self, id):
        """
        Retrieves a country by its ID from the database.
        Args:
            id: An integer ID of the country to be retrieved.
        Returns:
            A Country object if found, otherwise None.
        """
        if id is not None and isinstance(id, int):
            return self.dal.get_by_id(Country, id)
        return None

    def create_new_user(self, username, password, email, user_role_id):
        """
        Creates a new user with the provided information and adds it to the database.
        Args:
            username: A string representing the username of the new user.
            password: A string representing the password of the new user.
            email: A string representing the email of the new user.
            user_role_id: An integer representing the ID of the user role of the new user.
        Returns:
            A User object representing the new user if successfully created, otherwise None.
        """
        # Checking that all the required arguments are provided and are of the correct type
        if username is not None and isinstance(username, str) and password is not None and isinstance(password, str) and len(password) >= 6 and email is not None and isinstance(email, str) and user_role_id is not None and isinstance(user_role_id, int):
            # Hashing the password
            hashed_password = make_password(password)
            # Retrieving the user role from the database by its ID
            user_role = self.dal.get_by_id(UserRoles, user_role_id)
            # Checking that the user role was found in the database
            if user_role is not None:
                # Creating a new user object with the provided information
                user = User(username=username, password=hashed_password,
                            email=email, user_role=user_role_id)
                # Adding the new user object to the database
                self.dal.add(user)
                # Returning the new user object
                return user
        # If any of the conditions above are not met, return None
        return None


class AnonymousFacade(FacadeBase):
    """
    This is a facade class that provides an interface for users who are not authenticated to interact with the application's
    data access layer (DAL). It defines methods for user authentication and adding new customers to the system.
    """

    def login(self, username, password):
        """
        Authenticates a user with the given username and password.
        Args:
            username (str): The username of the user to authenticate.
            password (str): The password of the user to authenticate.
        Returns:
            A CustomerFacade, AirlineFacade, or AdministratorFacade object if the authentication is successful.
            None if the authentication fails.
        Raises:
            ValueError: If either username or password is not provided.
        """
        if not username or not password:
            print("Both username and password must be provided.")
            return None
            raise ValueError("Both username and password must be provided.")

        # Get the user object from the DAL using the provided username
        user = self.dal.get_user_by_username(username)

        # If the user doesn't exist, return None
        if not user:
            return None

        # Check if the provided password matches the user's password
        if not check_password(password, user.password):
            return None

        # Generate a token for the user (currently just the username)
        token = user.username

        # Determine the role of the user and return the corresponding facade object
        try:
            if user.user_role.role_name == 'customer':
                return CustomerFacade(token)
            elif user.user_role.role_name == 'airline':
                return AirlineFacade(token)
            return AdministratorFacade(token)
        except:
            return None

    def add_customer(self, username, password, email, first_name, last_name, address, phone_no, credit_card_no):
        """
        Adds a new customer to the database.
        Args:
        username: A string representing the customer's username.
        password: A string representing the customer's password.
        email: A string representing the customer's email.
        first_name: A string representing the customer's first name.
        last_name: A string representing the customer's last name.
        address: A string representing the customer's address.
        phone_no: A string representing the customer's phone number.
        credit_card_no: A string representing the customer's credit card number.
        Returns:
        A Customer object representing the newly added customer.
        Raises:
        ValueError: If any of the input parameters are invalid, or if the username, email, phone number or credit card number already exist.
        Exception: If an error occurs while adding the customer to the database.
        """
        if not isinstance(username, str) or not username:
            print("Invalid username provided")
            return None
            raise ValueError("Invalid username provided")
        if not isinstance(password, str) or not password or len(password) < 6:
            print("Invalid password provided")
            return None
            raise ValueError("Invalid password provided")
        if not isinstance(email, str) or not email:
            print("Invalid email provided")
            return None
            raise ValueError("Invalid email provided")
        if not isinstance(first_name, str) or not first_name:
            print("Invalid first name provided")
            return None
            raise ValueError("Invalid first name provided")
        if not isinstance(last_name, str) or not last_name:
            print("Invalid last name provided")
            return None
            raise ValueError("Invalid last name provided")
        if not isinstance(address, str) or not address:
            print("Invalid address provided")
            return None
            raise ValueError("Invalid address provided")
        if not phone_no:
            print("Invalid phone number provided")
            return None
            raise ValueError("Invalid phone number provided")
        if not credit_card_no:
            print("Invalid credit card number provided")
            return None
            raise ValueError("Invalid credit card number provided")

        if User.objects.filter(username=username).exists():
            print("Username already exists")
            return None
            raise ValueError("Username already exists")
        if User.objects.filter(email=email).exists():
            print("Email already exists")
            return None
            raise ValueError("Email already exists")
        if Customer.objects.filter(phone_no=phone_no).exists():
            print("Phone number already exists")
            return None
            raise ValueError("Phone number already exists")
        if Customer.objects.filter(credit_card_no=credit_card_no).exists():
            print("Credit card number already exists")
            return None
            raise ValueError("Credit card number already exists")
        
        try:
            user_role = UserRoles.objects.get(role_name='customer')
            user = User(username=username, password=make_password(
                password), email=email, user_role=user_role)
            self.dal.add(user)
            customer = Customer(user=user, first_name=first_name, last_name=last_name,
                                address=address, phone_no=phone_no, credit_card_no=credit_card_no)
            self.dal.add(customer)
            return user
        except Exception as error:
            print(error)
            return None


class CustomerFacade(FacadeBase):
    """
    A facade class that provides a simplified interface for accessing customer-related operations.
    It inherits from the abstract base class FacadeBase.
    """

    def __init__(self, token):
        """
        Initializes the CustomerFacade object.
        Args:
            token (str): A string containing the token for the logged-in user.
        """
        self.token = token
        super().__init__()

    def update_customer(self, username=None, password=None, email=None, first_name=None, last_name=None, address=None, phone_no=None, credit_card_no=None):
        """
        Updates the details of an existing customer in the database.
        Args:
            customer_id (int): The ID of the customer to be updated.
            username (str, optional): The new username for the customer.
            password (str, optional): The new password for the customer.
            email (str, optional): The new email address for the customer.
            first_name (str, optional): The new first name for the customer.
            last_name (str, optional): The new last name for the customer.
            address (str, optional): The new address for the customer.
            phone_no (str, optional): The new phone number for the customer.
            credit_card_no (str, optional): The new credit card number for the customer.
        Returns:
            The updated customer object.
        Raises:
            ValueError: If the customer is not found or if the new username, email, phone number, or credit card number already exists for another customer.
        """
        customer = self.dal.get_customer_by_username(self.token)
        if not customer:
            print("Customer not found")
            return None
            raise ValueError("Customer not found")

        if customer.user.username != self.token:
            print("Cannot update another customer")
            return None
            raise ValueError("Cannot update another customer")

        if username and User.objects.filter(username=username).exclude(pk=customer.user.id).exists():
            print("Username already exists")
            return None
            raise ValueError("Username already exists")

        if email and User.objects.filter(email=email).exclude(pk=customer.user.id).exists():
            print("Email already exists")
            return None
            raise ValueError("Email already exists")

        if phone_no and Customer.objects.filter(phone_no=phone_no).exclude(pk=customer.id).exists():
            print("Phone number already exists")
            return None
            raise ValueError("Phone number already exists")

        if credit_card_no and Customer.objects.filter(credit_card_no=credit_card_no).exclude(pk=customer.id).exists():
            print("Credit card number already exists")
            return None
            raise ValueError("Credit card number already exists")

        if username:
            customer.user.username = username
        if password:
            customer.user.password = make_password(password)
        if email:
            customer.user.email = email
        if first_name:
            customer.first_name = first_name
        if last_name:
            customer.last_name = last_name
        if address:
            customer.address = address
        if phone_no:
            customer.phone_no = phone_no
        if credit_card_no:
            customer.credit_card_no = credit_card_no

        self.dal.update(customer)
        return customer

    def add_ticket(self, flight_id, num_of_tickets=1):
        """
        Adds a new ticket for a customer for a given flight.
        Args:
            customer_username (str): The username of the customer who is adding the ticket.
            flight_id (int): The ID of the flight for which the ticket is being added.
            num_of_tickets (int): The number of tickets to be added.
        Returns:
            The newly created ticket object.
        Raises:
            ValueError: If the customer or flight is not found, or if there are not enough remaining tickets for the flight.
        """
        customer = self.dal.get_customer_by_username(self.token)
        if not customer:
            print("Customer not found")
            return None
            raise ValueError("Customer not found")

        flight = self.dal.get_by_id(Flight, flight_id)
        if not flight:
            print("Flight not found")
            return None
            raise ValueError("Flight not found")
        if flight.remaining_tickets < num_of_tickets:
            print("Not enough remaining tickets for the flight")
            return None
            raise ValueError("Not enough remaining tickets for the flight")

        ticket = Ticket(customer=customer, flight=flight)
        self.dal.add(ticket)

        flight.remaining_tickets -= num_of_tickets

        self.dal.update(flight)
        return ticket

    def remove_ticket(self, ticket_id):
        """
        Removes a ticket by its ID.
        Args:
        ticket_id: An integer ID of the ticket to be removed.
        Raises:
        ValueError: If ticket not found.
        """
        ticket = self.dal.get_by_id(Ticket, ticket_id)
        if not ticket:
            print("Ticket not found")
            return None
            raise ValueError("Ticket not found")
        if ticket.customer.user.username != self.token:
            print("Cannot remove a ticket of another customer")
            return None
            raise ValueError("Cannot remove a ticket of another customer")
        flight = ticket.flight
        flight.remaining_tickets += 1
        self.dal.update(flight)
        self.dal.remove(ticket)
        return ticket

    def get_my_tickets(self):
        """
        Retrieves all the tickets of the customer who is currently logged in.
        Returns:
            A list of Ticket objects.
        Raises:
            ValueError: If customer not found.
        """
        customer = self.dal.get_customer_by_username(self.token)
        if not customer:
            print("Customer not found")
            return None
            raise ValueError("Customer not found")
        tickets = self.dal.get_tickets_by_customer(customer.id)
        return tickets


class AirlineFacade(FacadeBase):
    """
    This is a class that provides a simplified interface to the DAL for airline-related actions. It includes methods to get
    the flights of a specific airline, update an airline's details, add a new flight for an airline, update an existing
    flight, and remove a flight.
    Attributes:
    token (str): The token that identifies the current airline user.
    """

    def __init__(self, token):
        """
        Initializes the AirlineFacade object with the given token.
        Args:
            token (str): The token that identifies the current airline user.
        """
        self.token = token
        super().__init__()

    def get_my_flights(self):
        """
        Retrieves all the flights associated with the current airline user.

        Returns:
            A list of Flight objects.
        Raises:
            ValueError: If the airline user cannot be found.
        """
        airline = self.dal.get_airline_by_username(self.token)
        if not airline:
            print("Airline not found")
            return None
            raise ValueError("Airline not found")
        flights = self.dal.get_flights_by_airline_id(airline.id)
        return flights

    def update_airline(self, name=None, country=None, username=None, password=None, email=None):
        """
        Updates the details of the airline identified by the given ID.

        Args:
            airline_id (int): The ID of the airline to update.
            name (str): The new name of the airline.
            country (int): The ID of the country the airline is located in.
            username (str): The new username for the airline user.
            password (str): The new password for the airline user.
            email (str): The new email address for the airline user.

        Returns:
            The updated AirlineCompany object.

        Raises:
            ValueError: If the airline cannot be found, the current user is not the same as the airline being updated,
                the new username or email already exists in the database, or there is an issue with the provided data.
        """
        airline = self.dal.get_airline_by_username(self.token)
        if not airline:
            print("Airline not found")
            return None
            raise ValueError("Airline not found")
        if airline.user.username != self.token:
            print("Cannot update another airline")
            return None
            raise ValueError("Cannot update another airline")
        if username and User.objects.filter(username=username).exclude(pk=airline.user.id).exists():
            print("Username already exists")
            return None
            raise ValueError("Username already exists")
        if email and User.objects.filter(email=email).exclude(pk=airline.user.id).exists():
            print("Email already exists")
            return None
            raise ValueError("Email already exists")
        if name:
            airline.name = name
        if country:
            airline.country = self.dal.get_by_id(Country, country)
        if username:
            airline.user.username = username
        if password:
            airline.user.password = make_password(password)
        if email:
            airline.user.email = email

        self.dal.update(airline)
        return airline

    def add_flight(self, origin_country, destination_country,
                   departure_time, landing_time, remaining_tickets):
        """
        Adds a new flight to the database with the given details.

        Args:
            origin_country (int): The ID of the country the flight departs from.
            destination_country (int): The ID of the country the flight arrives in.
            departure_time (datetime): The departure time of the flight.
            landing_time (datetime): The arrival time of the flight.
            remaining_tickets (int): The number of tickets remaining for the flight.

        Raises:
            ValueError: If the airline cannot be found or there is an issue with the provided data.
        """
        if remaining_tickets < 0:
            print("Remaining tickets cannot be negative")
            return None
            raise ValueError("Remaining tickets cannot be negative")
        if departure_time > landing_time:
            print("Landing time cannot be before take-off time")
            return None
            raise ValueError("Landing time cannot be before take-off time")
        if origin_country == destination_country:
            print("Origin and destination cannot be the same country")
            return None
            raise ValueError(
                "Origin and destination cannot be the same country")
        airline = self.dal.get_airline_by_username(self.token)
        if not airline:
            print("Airline not found")
            return None
            raise ValueError("Airline not found")

        origin_country = self.dal.get_by_id(Country, origin_country)
        destination_country = self.dal.get_by_id(Country, destination_country)
        flight = Flight(airline=airline, origin_country=origin_country,
                        destination_country=destination_country,
                        departure_time=departure_time, landing_time=landing_time,
                        remaining_tickets=remaining_tickets)
        self.dal.add(flight)
        return flight

    def update_flight(self, flight_id, origin_country=None,
                      destination_country=None, departure_time=None, landing_time=None,
                      remaining_tickets=None):
        """
        Updates the details of a flight with the given flight ID.

        Args:
        flight_id: An integer ID of the flight to be updated.
        origin_country: A Country object representing the country of origin for the flight.
        destination_country: A Country object representing the country of destination for the flight.
        departure_time: A datetime object representing the departure time for the flight.
        landing_time: A datetime object representing the landing time for the flight.
        remaining_tickets: An integer representing the number of remaining tickets for the flight.

        Raises:
        ValueError: If the flight is not found, the current user is not authorized to update the flight,
        remaining_tickets is negative, departure_time is after landing_time, or
        origin_country and destination_country are the same.

        Returns:
        The updated Flight object, or None if there was an error updating the flight.
        """
        current_flight = self.dal.get_by_id(Flight, flight_id)
        if not current_flight:
            print("Flight not found")
            return None
            raise ValueError("Flight not found")
        if current_flight.airline.user.username != self.token:
            print("Cannot update a flight for another airline")
            return None
            raise ValueError("Cannot update a flight for another airline")
        if remaining_tickets and remaining_tickets < 0:
            print("Remaining tickets cannot be negative")
            return None
            raise ValueError("Remaining tickets cannot be negative")
        if departure_time and landing_time and departure_time > landing_time:
            print("Landing time cannot be before take-off time")
            return None
            raise ValueError("Landing time cannot be before take-off time")
        if origin_country and destination_country and origin_country == destination_country:
            print("Origin and destination cannot be the same country")
            return None
            raise ValueError(
                "Origin and destination cannot be the same country")

        if origin_country:
            current_flight.origin_country = self.dal.get_by_id(
                Country, origin_country)
        if destination_country:
            current_flight.destination_country = self.dal.get_by_id(
                Country, destination_country)
        if departure_time:
            current_flight.departure_time = departure_time
        if landing_time:
            current_flight.landing_time = landing_time
        if remaining_tickets:
            current_flight.remaining_tickets = remaining_tickets
        self.dal.update(current_flight)
        return current_flight

    def remove_flight(self, flight_id):
        """
        Removes a flight with the given flight ID.
        Args:
            flight_id: An integer ID of the flight to be removed.
        Raises:
            ValueError: If the flight is not found or the current user is not authorized to remove the flight.
        """
        current_flight = self.dal.get_by_id(Flight, flight_id)
        if not current_flight:
            print("Flight not found")
            return None
            raise ValueError("Flight not found")
        if current_flight.airline.user.username != self.token:
            print("Cannot remove a flight for another airline")
            return None
            raise ValueError("Cannot remove a flight for another airline")
        self.dal.remove(current_flight)
        return current_flight


class AdministratorFacade(FacadeBase):
    def __init__(self, token=""):
        self.token = token
        super().__init__()

    def get_all_customers(self):
        """
        Returns all the customers stored in the database.
        Returns:
            A list of Customer objects.
        """
        return self.dal.get_all(Customer)

    def add_airline(self, name, country, username, password, email):
        """
        Adds a new airline company to the database.
        Args:
            name: A string name of the airline company.
            country: A string ID of the country where the airline company is located.
            username: A string username of the user associated with the airline company.
            password: A string password of the user associated with the airline company.
            email: A string email of the user associated with the airline company.
        Returns:
            An AirlineCompany object that was added to the database.
        Raises:
            ValueError: If the input parameters are not of the correct type or format.
                        If the username or email already exists in the database.
        """
        if not isinstance(username, str) or not username:
            print("Invalid username provided")
            return None
            raise ValueError("Invalid username provided")
        if not isinstance(password, str) or not password or len(password) < 6:
            print("Invalid password provided")
            return None
            raise ValueError("Invalid password provided")
        if not isinstance(email, str) or not email:
            print("Invalid email provided")
            return None
            raise ValueError("Invalid email provided")
        if not isinstance(name, str) or not name:
            print("Invalid name provided for airline")
            return None
            raise ValueError("Invalid name provided for airline")
        if not country:
            print("Invalid country id provided")
            return None
            raise ValueError("Invalid country id provided")

        if User.objects.filter(username=username).exists():
            print("Username already exists")
            return None
            raise ValueError("Username already exists")
        if User.objects.filter(email=email).exists():
            print("Email already exists")
            return None
            raise ValueError("Email already exists")
        try:
            country_obj = self.dal.get_by_id(Country, country)
            user_role = UserRoles.objects.get(role_name='airline')
            user = User(username=username, password=make_password(password),
                        email=email, user_role=user_role)
            airline = AirlineCompany(name=name, country=country_obj, user=user)
            self.dal.add(user)
            self.dal.add(airline)
            return user
        except Exception as e:
            print(e)
            return None

    def add_customer(self, username, password, email, first_name, last_name, address, phone_no, credit_card_no):
        """
        Adds a new customer to the database.
        Args:
        username: A string representing the customer's username.
        password: A string representing the customer's password.
        email: A string representing the customer's email.
        first_name: A string representing the customer's first name.
        last_name: A string representing the customer's last name.
        address: A string representing the customer's address.
        phone_no: A string representing the customer's phone number.
        credit_card_no: A string representing the customer's credit card number.
        Returns:
        A Customer object representing the newly added customer.
        Raises:
        ValueError: If any of the input parameters are invalid, or if the username, email, phone number or credit card number already exist.
        Exception: If an error occurs while adding the customer to the database.
        """
        if not isinstance(username, str) or not username:
            print("Invalid username provided")
            return None
            raise ValueError("Invalid username provided")
        if not isinstance(password, str) or not password or len(password) < 6:
            print("Invalid password provided")
            return None
            raise ValueError("Invalid password provided")
        if not isinstance(email, str) or not email:
            print("Invalid email provided")
            return None
            raise ValueError("Invalid email provided")
        if not isinstance(first_name, str) or not first_name:
            print("Invalid first name provided")
            return None
            raise ValueError("Invalid first name provided")
        if not isinstance(last_name, str) or not last_name:
            print("Invalid last name provided")
            return None
            raise ValueError("Invalid last name provided")
        if not isinstance(address, str) or not address:
            print("Invalid address provided")
            return None
            raise ValueError("Invalid address provided")
        if not phone_no:
            print("Invalid phone number provided")
            return None
            raise ValueError("Invalid phone number provided")
        if not credit_card_no:
            print("Invalid credit card number provided")
            return None
            raise ValueError("Invalid credit card number provided")

        if User.objects.filter(username=username).exists():
            print("Username already exists")
            return None
            raise ValueError("Username already exists")
        if User.objects.filter(email=email).exists():
            print("Email already exists")
            return None
            raise ValueError("Email already exists")
        if Customer.objects.filter(phone_no=phone_no).exists():
            print("Phone number already exists")
            return None
            raise ValueError("Phone number already exists")
        if Customer.objects.filter(credit_card_no=credit_card_no).exists():
            print("Credit card number already exists")
            return None
            raise ValueError("Credit card number already exists")

        user_role = UserRoles.objects.get(role_name='customer')
        user = User(username=username, password=make_password(
            password), email=email, user_role=user_role)
        try:
            self.dal.add(user)
            customer = Customer(user=user, first_name=first_name, last_name=last_name,
                                address=address, phone_no=phone_no, credit_card_no=credit_card_no)
            self.dal.add(customer)
            return user
        except Exception as error:
            print(error)
            return None

    def add_administrator(self, username, password, email, first_name, last_name):
        """
        Adds a new administrator to the system.
        Args:
            username: A string containing the username of the new administrator.
            password: A string containing the password of the new administrator.
            email: A string containing the email of the new administrator.
            first_name: A string containing the first name of the new administrator.
            last_name: A string containing the last name of the new administrator.
        Returns:
            An Administrator object representing the newly created administrator.
        Raises:
            ValueError: If the username or email already exists in the database.
        """
        if not isinstance(password, str) or not password or len(password) < 6:
            print("Invalid password provided")
            return None
            raise ValueError("Invalid password provided")
        if User.objects.filter(username=username).exists():
            print("Username already exists")
            return None
            raise ValueError("Username already exists")
        if User.objects.filter(email=email).exists():
            print("Email already exists")
            return None
            raise ValueError("Email already exists")
        user_role = UserRoles.objects.get(role_name='manager')
        user = User(username=username, password=make_password(password),
                    email=email, user_role=user_role)
        self.dal.add(user)
        admin = Administrator(first_name=first_name,
                              last_name=last_name, user=user)
        self.dal.add(admin)
        return user

    def remove_airline(self, airline_id):
        """
        Removes an airline from the system.
        Args:
            airline_id: An integer ID of the airline to be removed.
        Raises:
            ValueError: If the airline is not found in the database.
        """
        airline = self.dal.get_by_id(AirlineCompany, airline_id)
        if not airline:
            print("Airline not found")
            return None
            raise ValueError("Airline not found")
        self.dal.remove(airline.user)
        self.dal.remove(airline)
        return airline

    def remove_customer(self, customer_id):
        """
        Removes a customer from the system.
        Args:
            customer_id: An integer ID of the customer to be removed.
        Raises:
            ValueError: If the customer is not found in the database.
        """
        customer = self.dal.get_by_id(Customer, customer_id)
        if not customer:
            print("Customer not found")
            return None
            raise ValueError("Customer not found")
        self.dal.remove(customer.user)
        self.dal.remove(customer)
        return customer

    def remove_administrator(self, admin_id):
        """
        Removes an administrator from the system.
        Args:
            admin_id: An integer ID of the administrator to be removed.
        Raises:
            ValueError: If the administrator is not found in the database.
        """
        admin = self.dal.get_by_id(Administrator, admin_id)
        if not admin:
            print("Administrator not found")
            return None
            raise ValueError("Administrator not found")
        self.dal.remove(admin.user)
        self.dal.remove(admin)
        return admin
