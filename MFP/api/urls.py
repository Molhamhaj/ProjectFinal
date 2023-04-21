from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

app_name = 'api'


urlpatterns = [
    re_path(r'^countries$', views.Countries),
    re_path(r'^flights$', views.Flights),
    re_path(r'^myFlights$', views.MyFlights),
    re_path(r'^myFlights/(?P<pk>[0-9]+)$', views.MyFlights),
    re_path(r'^filter$', views.FilterFlights),
    re_path(r'^register$', views.Register),
    re_path(r'^login$', views.Login),
    re_path(r'^flightById/(?P<pk>[0-9]+)$', views.FlightByID),
    re_path(r'^book$', views.Book),
    re_path(r'^ticketsById$', views.TicketsByID),
]