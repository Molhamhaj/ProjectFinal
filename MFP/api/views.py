
from rest_framework.decorators import api_view
from . import serializers
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from . import facades


# Some utility functions
def getSession(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        role_name = request.META.get('HTTP_AUTHORIZATION').split()[2]
    except Exception as e:
        print(e)
        return None
    if role_name == 'customer':
        return facades.CustomerFacade(token)
    elif role_name == 'airline':
        return facades.AirlineFacade(token)
    return None
# Create your views here.


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def Countries(request):
    if request.method == 'GET':
        session = facades.AnonymousFacade()
        object_serializer = serializers.CountrySerializer(
            session.get_all_countries(), many=True)
        return JsonResponse(object_serializer.data, safe=False)


@api_view(['GET', 'POST', 'PUT'])
@authentication_classes([])
@permission_classes([])
def Flights(request):
    if request.method == 'GET':
        session = facades.AnonymousFacade()
        object_serializer = serializers.FlightSerializer(
            session.get_all_flights(), many=True)
        return JsonResponse(object_serializer.data, safe=False)
    if request.method == 'POST':
        session = getSession(request)
        if session is None:
            return JsonResponse({'message': "Not logged in!"}, status=status.HTTP_200_OK)
        data = JSONParser().parse(request)
        flight = session.add_flight(int(data['origin_country']), int(data['destination_country']),
                                    data['departure_time'], data['landing_time'], int(data['remaining_tickets']))
        if flight is None:
            return JsonResponse({'message': "System error!"}, status=status.HTTP_200_OK)
        object_serializer = serializers.FlightSerializer(
            flight, many=False)
        return JsonResponse(object_serializer.data, safe=False)
    if request.method == 'PUT':
        session = getSession(request)
        if session is None:
            return JsonResponse({'message': "Not logged in!"}, status=status.HTTP_200_OK)
        data = JSONParser().parse(request)
        flight = session.update_flight(int(data['id']), int(data['origin_country']), int(data['destination_country']),
                                       data['departure_time'], data['landing_time'], int(data['remaining_tickets']))
        if flight is None:
            return JsonResponse({'message': "System error!"}, status=status.HTTP_200_OK)
        object_serializer = serializers.FlightSerializer(
            flight, many=False)
        return JsonResponse(object_serializer.data, safe=False)


@api_view(['GET', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def MyFlights(request, pk=None):
    if request.method == 'GET':
        session = getSession(request)
        if session is None:
            return JsonResponse({'message': "Not logged in!"}, status=status.HTTP_200_OK)
        object_serializer = serializers.FlightSerializer(
            session.get_my_flights(), many=True)
        return JsonResponse(object_serializer.data, safe=False)
    if request.method == 'DELETE':
        session = getSession(request)
        if session is None:
            return JsonResponse({'message': "Not logged in!"}, status=status.HTTP_200_OK)
        if pk is None:
            return JsonResponse({'message': "Flight id is required!"}, status=status.HTTP_200_OK)
        if session.remove_flight(int(pk)) is None:
            return JsonResponse({'message': "System error!"}, status=status.HTTP_200_OK)
        return JsonResponse({}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def FilterFlights(request):
    if request.method == 'POST':
        session = facades.AnonymousFacade()
        data = JSONParser().parse(request)
        origin_country_id = data['origin_country_id']
        destination_country_id = data['destination_country_id']
        date = data['date']
        all_data = session.get_flights_by_parameters(int(origin_country_id), int(
            destination_country_id), date)
        object_serializer = serializers.FlightSerializer(
            all_data, many=True)
        return JsonResponse(object_serializer.data, safe=False)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def Register(request):
    if request.method == 'POST':
        session = facades.AnonymousFacade()
        data = JSONParser().parse(request)
        if data["user_role"] == "customer":
            customer = session.add_customer(data['username'], data['password'], data['email'], data['first_name'],
                                            data['last_name'], data['address'], data['phone_no'], data['credit_card_no'])
            if customer is not None:
                object_serializer = serializers.UserSerializer(
                    customer, many=False)
                facade = session.login(data['username'], data['password'])
                return JsonResponse(object_serializer.data, safe=False)
            return JsonResponse({'message': "Username/Email/Phone/Credit Card should be unique!"}, status=status.HTTP_200_OK)
        if data["user_role"] == "airline":
            airline = facades.AdministratorFacade().add_airline(
                data['name'], int(data['country']), data['username'], data['password'], data['email'])
            if airline is not None:
                object_serializer = serializers.UserSerializer(
                    airline, many=False)
                facade = session.login(data['username'], data['password'])
                return JsonResponse(object_serializer.data, safe=False)
            return JsonResponse({'message': "Username/Email should be unique!"}, status=status.HTTP_200_OK)
        return JsonResponse({'message': "Invalid user role!"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def Login(request):
    if request.method == 'POST':
        session = facades.AnonymousFacade()
        data = JSONParser().parse(request)
        facade = session.login(data['username'], data['password'])
        if facade:
            if type(facade).__name__ == "CustomerFacade":
                object_serializer = serializers.UserSerializer(
                    session.dal.get_user_by_username(data['username']), many=False)
            if type(facade).__name__ == "AirlineFacade":
                object_serializer = serializers.UserSerializer(
                    session.dal.get_user_by_username(data['username']), many=False)
            return JsonResponse(object_serializer.data, safe=False)
        return JsonResponse({'message': "Invalid Username/Password!"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def FlightByID(request, pk):
    if request.method == 'GET':
        session = getSession(request)
        if session is None:
            return JsonResponse({'message': "Not logged in!"}, status=status.HTTP_200_OK)
        flight = session.get_flight_by_id(int(pk))
        if flight is not None:
            object_serializer = serializers.FlightSerializer(
                flight, many=False)
            return JsonResponse(object_serializer.data, safe=False)
        return JsonResponse({'message': "No flight with this ID!"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def Book(request):
    if request.method == 'POST':
        session = getSession(request)
        if session is None:
            return JsonResponse({'message': "Not logged in!"}, status=status.HTTP_200_OK)
        if isinstance(session, facades.CustomerFacade) is not True:
            return JsonResponse({'message': "Not a appropriate role!"}, status=status.HTTP_200_OK)
        data = JSONParser().parse(request)
        ticket = session.add_ticket(int(data['flight']), 1)
        if ticket is None:
            return JsonResponse({'message': "System error!"}, status=status.HTTP_200_OK)
        object_serializer = serializers.TicketSerializer(
            ticket, many=False)
        return JsonResponse(object_serializer.data, safe=False)


@api_view(['GET'])
def TicketsByID(request):
    if request.method == 'GET':
        session = getSession(request)
        if session is None:
            return JsonResponse({'message': "Not logged in!"}, status=status.HTTP_200_OK)
        try:
            tickets = session.get_my_tickets()
        except:
            return JsonResponse({'message': "No ticket with this ID!"}, status=status.HTTP_200_OK)
        object_serializer = serializers.TicketSerializer(
            tickets, many=True)
        return JsonResponse(object_serializer.data, safe=False)
