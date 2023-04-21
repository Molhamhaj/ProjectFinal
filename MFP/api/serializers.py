from rest_framework import serializers
from .models import Country, UserRoles, User, Customer, AirlineCompany, Administrator, Flight, Ticket


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    user_role = UserRolesSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_role']


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = '__all__'


class AirlineCompanySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    country = CountrySerializer()

    class Meta:
        model = AirlineCompany
        fields = '__all__'


class AdministratorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Administrator
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    airline = AirlineCompanySerializer()
    origin_country = CountrySerializer()
    destination_country = CountrySerializer()

    class Meta:
        model = Flight
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    flight = FlightSerializer()
    customer = CustomerSerializer()

    class Meta:
        model = Ticket
        fields = '__all__'
