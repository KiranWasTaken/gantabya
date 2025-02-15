from django.urls import path
from .views import *

urlpatterns = [
    #public
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='token_obtain_pair'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('delete-account', DeleteAccountView.as_view(), name='delete-account'),

    #destinations
    path('destinations', DestinationListCreateView.as_view(), name='destination-list-create'),
    path('destinations', DestinationSearchView.as_view(), name='search-destinations'),
    path('destinations/popular', PopularDestinationsView.as_view(), name='popular-destinations'),
    path('destinations/<int:destination_id>', DestinationDetailView.as_view(), name='destination-detail'),

    path('travel-plans', TravelPlanCreateView.as_view(), name='travel-plans'),

    #images
    path('images', ImageCreateView.as_view(), name='image-create'),
    path('images', ImageSearchView.as_view(), name='image-search-images'),

    #airlines
    path('airlines', AirlineCreateView.as_view(), name='airlines'),
    path('airlines', AirlineSearchView.as_view(), name='search-airlines'),

    #buses
    path('buses', BusCreateView.as_view(), name='buses'),
    path('buses', BusSearchView.as_view(), name='search-buses'),

    #hotels
    path('hotels', HotelCreateView.as_view(), name='hotels'),
    path('hotels', HotelSearchView.as_view(), name='search-hotels'),
]
