from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # challenge: add flag image field
    flag = models.ImageField(upload_to='flags/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class UserRoles(models.Model):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('airline', 'Airline'),
        ('manager', 'Manager'),
    )
    role_name = models.CharField(
        max_length=50, unique=True, choices=ROLE_CHOICES)
    # challenge: add thumbnail field
    thumbnail = models.ImageField(
        upload_to='thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.role_name

    class Meta:
        verbose_name_plural = "User Roles"


class User(AbstractUser):
    username = models.CharField(
        max_length=50, unique=True, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False)
    email = models.CharField(
        max_length=50, unique=True, blank=False, null=False)
    user_role = models.ForeignKey(
        UserRoles, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.username} ({self.user_role})'

    class Meta:
        verbose_name_plural = "Users"


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=20, unique=True)
    credit_card_no = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name_plural = "Customers"


class AirlineCompany(models.Model):
    name = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Airline Companies"


class Administrator(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name_plural = "Admins"


class Flight(models.Model):
    airline = models.ForeignKey(AirlineCompany, on_delete=models.CASCADE)
    origin_country = models.ForeignKey(
        Country, related_name='origin_country', on_delete=models.CASCADE)
    destination_country = models.ForeignKey(
        Country, related_name='destination_country', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    landing_time = models.DateTimeField()
    remaining_tickets = models.IntegerField()

    def __str__(self):
        return f'{self.origin_country.name} to {self.destination_country.name}'

    class Meta:
        verbose_name_plural = "Flights"


class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'Ticket ID: {self.id}, Flight: {self.flight}, Customer: {self.customer}'

    class Meta:
        verbose_name_plural = "Tickets"
