from .facades import AnonymousFacade, CustomerFacade, AirlineFacade, AdministratorFacade
from .models import Country, UserRoles, User, Customer, AirlineCompany, Administrator, Flight, Ticket
from .utils import DAL
from django.contrib.auth.hashers import make_password
import pytest
import random


@pytest.fixture
def setup_test_environment():
    # Initialize data for testing
    dal = DAL()
    countries = [Country(name='USA'), Country(name='Canada')]
    user_roles = [UserRoles(role_name='customer'),
                  UserRoles(role_name='airline'),
                  UserRoles(role_name='manager')]
    users = [
        User(
            username='user1',
            password=make_password('password1'),
            email='user1@example.com',
            user_role=user_roles[0]
        ),
        User(
            username='user2',
            password=make_password('password2'),
            email='user2@example.com',
            user_role=user_roles[1]
        ),
        User(
            username='user3',
            password=make_password('password3'),
            email='user3@example.com',
            user_role=user_roles[2]
        ),
        User(
            username='user4',
            password=make_password('password4'),
            email='user4@example.com',
            user_role=user_roles[0]
        ),
        User(
            username='user5',
            password=make_password('password5'),
            email='user5@example.com',
            user_role=user_roles[1]
        ),
        User(
            username='user6',
            password=make_password('password6'),
            email='user6@example.com',
            user_role=user_roles[2]
        )
    ]
    customers = [Customer(first_name='John', last_name='Doe', address='123 Main St', phone_no='555-1234',
                          credit_card_no='1234567812345678', user=users[0]),
                 Customer(first_name='Jane', last_name='Doe', address='456 Elm St', phone_no='555-5678',
                          credit_card_no='8765432187654321', user=users[3])]
    airline_companies = [AirlineCompany(name='American Airlines', country=countries[0], user=users[1]),
                         AirlineCompany(name='Air Canada', country=countries[1], user=users[4])]
    administrators = [Administrator(
        first_name='Admin', last_name='User', user=users[2]), Administrator(
        first_name='Admin2', last_name='User2', user=users[5])]
    flights = [Flight(airline=airline_companies[0], origin_country=countries[0], destination_country=countries[1],
                      departure_time='2023-03-09 12:00:00', landing_time='2023-03-09 14:00:00', remaining_tickets=100),
               Flight(airline=airline_companies[1], origin_country=countries[1], destination_country=countries[0],
                      departure_time='2023-03-10 12:00:00', landing_time='2023-03-10 14:00:00', remaining_tickets=100)]
    tickets = [Ticket(flight=flights[0], customer=customers[0]),
               Ticket(flight=flights[1], customer=customers[1])]
    ids = dal.add_all(countries + user_roles + users + customers +
                      airline_companies + administrators + flights + tickets)

    yield ids

    # Clean up the test environment after the tests have run
    dal.delete_all_records(Country)
    dal.delete_all_records(UserRoles)
    dal.delete_all_records(User)
    dal.delete_all_records(Customer)
    dal.delete_all_records(AirlineCompany)
    dal.delete_all_records(Administrator)
    dal.delete_all_records(Flight)
    dal.delete_all_records(Ticket)


def login_to_session(username, password):
    init = AnonymousFacade()
    respective_facade = init.login(username, password)
    assert respective_facade is not None
    return respective_facade


def incorrect_number(ids):
    random_number = random.randint(1, 100)
    while random_number in ids:
        random_number = random.randint(1, 100)
    return random_number


@pytest.mark.django_db
def test_anonymous_facade(setup_test_environment):
    facade = AnonymousFacade()

    # checking correct logins
    assert isinstance(facade.login('user1', 'password1'), CustomerFacade)
    assert isinstance(facade.login('user2', 'password2'), AirlineFacade)
    assert isinstance(facade.login('user3', 'password3'), AdministratorFacade)

    # checking incorrect login
    assert facade.login('user1', 'wrong_password') is None

    # checking empty login
    assert facade.login('', '') is None

    # checking non-existent login
    assert facade.login('nonexistent_user', 'password') is None

    # adding customer with correct information
    assert facade.add_customer('johndoe', 'password123', 'johndoe@example.com',
                               'John', 'Doe', '123 Main St', '555-1230', '1234567812345608') is not None

    # check the login
    assert isinstance(facade.login('johndoe', 'password123'), CustomerFacade)

    # adding customer with existing username
    assert facade.add_customer('johndoe', 'password123', 'johndoe_2@example.com',
                               'John', 'Doe', '123 Main St', '555-1234', '1234567812345678') is None

    # adding customer with invalid password
    assert facade.add_customer('johndoe', 'pass', 'johndoe_2@example.com',
                               'John', 'Doe', '123 Main St', '555-1234', '1234567812345678') is None


@pytest.mark.django_db
def test_customer_facade(setup_test_environment):
    session = login_to_session("user1", "password1")
    other_session = login_to_session("user4", "password4")

    # checking customer updation with complete information
    assert session.update_customer(username="user1_updated", password="password1_updated", email="user1_updated@example.com", first_name='John_updated', last_name='Doe_updated', address='123 Main St_updated', phone_no='555-4321',
                                   credit_card_no='4321567812345678').user.username == "user1_updated"

    # checking customer updation with specific information
    assert session.update_customer(
        username="user1_undo", last_name='Doe_undo').last_name == "Doe_undo"

    # adding new ticket with correct flight
    ticket1 = session.add_ticket(setup_test_environment['Flight'][0])
    assert ticket1 is not None
    other_ticket1 = other_session.add_ticket(
        setup_test_environment['Flight'][1])
    assert other_ticket1 is not None

    # adding new ticket with wrong flight
    assert session.add_ticket(incorrect_number(
        setup_test_environment['Flight'])) is None

    # remove ticket
    assert session.remove_ticket(ticket1.id) is not None

    # remove ticket of someone else
    assert session.remove_ticket(other_ticket1.id) is None

    # get my tickets
    assert len(session.get_my_tickets()) == 1


@pytest.mark.django_db
def test_airline_facade(setup_test_environment):
    session = login_to_session("user2", "password2")
    other_session = login_to_session("user5", "password5")

    # checking airline updation with complete information
    assert session.update_airline(name="user2_updated", country=setup_test_environment["Country"][
                                  1], username="user2_updated", password="user2_updated", email="user2_updated@gmail.com").user.username == "user2_updated"

    # checking airline updation with specific information
    assert session.update_airline(
        name="sample airline", email="airline@gmail.com").name == "sample airline"

    # add flight
    flight1 = session.add_flight(setup_test_environment["Country"][1], setup_test_environment["Country"]
                                 [0], '2023-03-12 12:00:00', '2023-03-12 14:00:00', 100)
    other_flight1 = other_session.add_flight(setup_test_environment["Country"][0], setup_test_environment["Country"]
                                             [1], '2023-03-12 12:00:00', '2023-03-12 14:00:00', 50)
    assert flight1 is not None
    assert other_flight1 is not None

    # add flight with negative number of tickets
    assert session.add_flight(setup_test_environment["Country"][1], setup_test_environment["Country"]
                              [0], '2023-03-12 14:00:00', '2023-03-12 16:00:00', -1) is None

    # add flight with same origin and destination
    assert session.add_flight(setup_test_environment["Country"][1], setup_test_environment["Country"]
                              [1], '2023-03-12 12:00:00', '2023-03-12 14:00:00', 100) is None

    # add flight with landing time before take-off
    assert session.add_flight(setup_test_environment["Country"][0], setup_test_environment["Country"]
                              [1], '2023-03-12 14:00:00', '2023-03-12 12:00:00', 100) is None

    # checking flight updation with complete information
    assert session.update_flight(flight1.id, setup_test_environment["Country"][0],
                                 setup_test_environment["Country"][1], '2023-03-12 15:00:00', '2023-03-12 17:00:00', 200).remaining_tickets == 200

    # checking flight updation with specific information
    assert session.update_flight(
        flight1.id,  remaining_tickets=250).remaining_tickets == 250

    # update someone else flight
    assert session.update_flight(
        other_flight1.id, remaining_tickets=200) is None

    # remove recently created flight
    assert session.remove_flight(flight1.id) is not None

    # delete someone else flight
    assert session.remove_flight(other_flight1.id) is None


@pytest.mark.django_db
def test_admin_facade(setup_test_environment):
    session = login_to_session("user3", "password3")

    # get all customers
    assert len(session.get_all_customers()) == 2

    # adding airline with correct information
    airline = session.add_airline(
        'PIA', setup_test_environment["Country"][1], 'airline_johndoe', 'password', 'airline_johndoe@gmail.com')
    assert airline is not None

    # adding airline with existing username
    assert session.add_airline(
        'PIA2', setup_test_environment["Country"][1], 'airline_johndoe', 'password1', 'airline_johndoe_1@gmail.com') is None

    # adding airline with invalid password
    assert session.add_airline(
        'PIA3', setup_test_environment["Country"][1], 'airline_johndoe2', 'pass', 'airline_johndoe_2@gmail.com') is None

    # adding customer with correct information
    customer = session.add_customer('cust_johndoe', 'password123', 'cust_johndoe@example.com',
                                    'John', 'Doe', '123 Main St', '555-1230', '1234567812345608')
    assert customer is not None

    # adding customer with existing username
    assert session.add_customer('cust_johndoe', 'password123', 'cust_johndoe_2@example.com',
                                'John', 'Doe', '123 Main St', '555-1234', '1234567812345678') is None

    # adding customer with invalid password
    assert session.add_customer('cust_johndoe', 'pass', 'cust_johndoe_2@example.com',
                                'John', 'Doe', '123 Main St', '555-1234', '1234567812345678') is None

    # adding admin with correct information
    admin = session.add_administrator(
        'admin_johndoe', 'password', 'admin_johndoe@gmail.com', 'Johndoe', 'Admin')
    assert admin is not None

    # adding admin with existing username
    assert session.add_administrator(
        'admin_johndoe', 'password', 'admin_johndoe_2@gmail.com', 'Johndoe', 'Admin') is None

    # adding admin with invalid password
    assert session.add_administrator(
        'admin_johndoe_3', 'pass', 'admin_johndoe_3@gmail.com', 'Johndoe', 'Admin') is None

    # removing airline
    assert session.remove_airline(
        session.dal.get_airline_by_username(airline.username).id) is not None

    # removing customer
    assert session.remove_customer(
        session.dal.get_customer_by_username(customer.username).id) is not None

    # removing admin
    assert session.remove_administrator(
        session.dal.get_admin_by_username(admin.username).id) is not None


@pytest.mark.django_db
def test_overbooked(setup_test_environment):
    session_airline = login_to_session("user2", "password2")
    session_customer = login_to_session("user1", "password1")
    # add flight
    flight1 = session_airline.add_flight(setup_test_environment["Country"][1], setup_test_environment["Country"]
                                         [0], '2023-03-12 12:00:00', '2023-03-12 14:00:00', 1)
    assert flight1 is not None

    # adding new ticket for above flight
    ticket1 = session_customer.add_ticket(flight1.id)
    assert ticket1 is not None

    # adding again new ticket for above flight which is now out of tickets
    ticket1 = session_customer.add_ticket(flight1.id)
    assert ticket1 is None
