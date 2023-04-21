from django.db.models.query import QuerySet
from typing import List, Type
from .models import AirlineCompany, Flight, Customer, Ticket, User, Administrator
from django.db.models import Q
from datetime import datetime, timedelta
import secrets
import logging


class DAL:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='operations_dal.log', level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def get_by_id(self, model: Type, id: int):
        """Returns the instance of a model class with the specified id"""
        self.logger.info(f"Getting {model.__name__} instance with id {id}")
        return model.objects.filter(id=id).first()

    def get_all(self, model: Type) -> QuerySet:
        """Returns all instances of a model class"""
        self.logger.info(f"Getting all {model.__name__} instances")
        return model.objects.all().order_by('-id')

    def add(self, instance) -> None:
        """Saves a single instance to the database"""
        self.logger.info(
            f"Adding {instance.__class__.__name__} instance to the database")
        instance.save()

    def update(self, instance) -> None:
        """Updates a single instance in the database"""
        self.logger.info(
            f"Updating {instance.__class__.__name__} instance in the database")
        instance.save()

    def add_all(self, instances: List):
        """
        Saves multiple instances to the database and returns a dictionary
        mapping the classname to a list of saved instance ids.
        """
        ids_by_classname = {}
        for instance in instances:
            classname = instance.__class__.__name__
            self.logger.info(f"Adding {classname} instance to the database")
            instance.save()
            # Add the saved instance id to the list for this classname
            ids_by_classname.setdefault(classname, []).append(instance.id)
        return ids_by_classname

    def remove(self, instance) -> None:
        """Deletes a single instance from the database"""
        self.logger.info(
            f"Deleting {instance.__class__.__name__} instance from the database")
        instance.delete()

    def delete_all_records(self, model: Type):
        """
        Delete all records from the database table associated with the given model.
        """
        self.logger.info(f"Deleting all {model.__name__} instances")
        model.objects.all().delete()

    def generate_login_token(self):
        """Generates login token of 16 bytes"""
        self.logger.info("Generating login token")
        token = secrets.token_hex(16)
        return token

    def getAirlinesByCountry(self, country_id):
        """Returns all airlines that belong to a specific country"""
        self.logger.info(
            f"Getting all airlines that belong to country with id {country_id}")
        airlines = AirlineCompany.objects.filter(country__id=country_id)
        return airlines

    def getFlightsByOriginCountryId(self, country_id):
        """Returns all flights that depart from a specific country"""
        self.logger.info(
            f"Getting all flights that depart from country with id {country_id}")
        flights = Flight.objects.filter(origin_country__id=country_id)
        return flights

    def getFlightsByDestinationCountryId(self, country_id):
        """Returns all flights that arrive at a specific country"""
        self.logger.info(
            f"Getting all flights that arrive at country with id {country_id}")
        flights = Flight.objects.filter(destination_country__id=country_id)
        return flights

    def getFlightsByDepartureDate(self, date):
        """Returns all flights that depart on a specific date"""
        self.logger.info(f"Getting all flights that depart on date {date}")
        flights = Flight.objects.filter(departure_time=date)
        return flights

    def getFlightsByLandingDate(self, date):
        """Returns all flights that arrive on a specific date"""
        self.logger.info(f"Getting all flights that arrive on date {date}")
        flights = Flight.objects.filter(landing_time=date)
        return flights

    def getFlightsByCustomer(self, customer_id):
        """Returns all flights booked by a specific customer"""
        self.logger.info(
            f"Getting all flights booked by customer with id {customer_id}")
        tickets = Ticket.objects.filter(customer__id=customer_id)
        flights = Flight.objects.filter(ticket__in=tickets)
        return flights

    def get_airline_by_username(self, _username):
        """Returns the airline associated with a specific username"""
        self.logger.info(f"Getting airline for username: {_username}")
        try:
            airline = AirlineCompany.objects.select_related(
                'user').get(user__username=_username)
            return airline
        except AirlineCompany.DoesNotExist:
            self.logger.warning(f"No airline found for username: {_username}")
            return None

    def get_customer_by_username(self, _username):
        """Returns the customer associated with a specific username"""
        self.logger.info(f"Getting customer for username: {_username}")
        try:
            customer = Customer.objects.select_related(
                'user').get(user__username=_username)
            return customer
        except Customer.DoesNotExist:
            self.logger.warning(f"No customer found for username: {_username}")
            return None

    def get_admin_by_username(self, _username):
        """Returns the admin associated with a specific username"""
        self.logger.info(f"Getting admin for username: {_username}")
        try:
            admin = Administrator.objects.select_related(
                'user').get(user__username=_username)
            return admin
        except Administrator.DoesNotExist:
            self.logger.warning(f"No admin found for username: {_username}")
            return None

    def get_user_by_username(self, _username):
        """Returns the user associated with a specific username"""
        self.logger.info(f"Getting user for username: {_username}")
        try:
            user = User.objects.get(username=_username)
            return user
        except User.DoesNotExist:
            self.logger.warning(f"No user found for username: {_username}")
            return None

    def get_flights_by_parameters(self, _origin_country_id, _destination_country_id, _date):
        """Returns all flights that match specific parameters"""
        self.logger.info(
            f"Getting flights for origin country id: {_origin_country_id}, destination country id: {_destination_country_id}, and date: {_date}")
        flights = Flight.objects.filter(
            origin_country__id=_origin_country_id,
            destination_country__id=_destination_country_id,
            departure_time__date=_date
        )
        return flights

    def get_flights_by_airline_id(self, _airline_id):
        """Returns all flights operated by a specific airline"""
        self.logger.info(f"Getting flights for airline id: {_airline_id}")
        flights = Flight.objects.filter(airline__id=_airline_id)
        return flights

    def get_departure_flights(self, _country_id):
        """Returns all flights departing from a specific country within the next 12 hours."""
        self.logger.info(
            f"Getting departure flights for country id: {_country_id}")
        now = datetime.now()
        next_12_hours = now + timedelta(hours=12)
        flights = Flight.objects.filter(
            origin_country__id=_country_id,
            departure_time__range=(now, next_12_hours)
        )
        return flights

    def get_tickets_by_customer(self, _customer_id):
        """Returns all tickets purchased by a specific customer."""
        self.logger.info(f"Getting tickets for customer id: {_customer_id}")
        tickets = Ticket.objects.filter(customer__id=_customer_id)
        return tickets
