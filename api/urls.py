from django.urls import path
from .views import *

urlpatterns = [
    #public
    path('user/signup', SignUpView.as_view(), name='signup'),
    path('user/login', LoginView.as_view(), name='token_obtain_pair'),
    path('user/forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('user/delete-account', DeleteAccountView.as_view(), name='delete-account'),
    path('user/<int:user_id>/travel-cost', UserTravelCostView.as_view(), name='travel-cost'),

    #destinations
    path('destinations', DestinationListCreateView.as_view(), name='destination-list-create'),
    path('destinations', DestinationSearchView.as_view(), name='search-destinations'),
    path('destinations/popular', PopularDestinationsView.as_view(), name='popular-destinations'),
    path('destinations/<int:destination_id>', DestinationDetailView.as_view(), name='destination-detail'),
    path('destinations/<int:destination_id>', DeleteDestinationView.as_view(), name='delete-destination'),
    path('destinations/<int:destination_id>/airlines', DestinationListAirlineView.as_view(), name='delete-destination'),
    path('destinations/<int:destination_id>/hotels', DestinationListHotelView.as_view(), name='delete-destination'),
    path('destinations//buses', DestinationListBusView.as_view(), name='delete-destination'),
    path('destinations/<int:destination_id>/optimal-cost', OptimalCostView.as_view(), name='optimal-cost'),
    path('destinations/popular', PopularDestinationsView.as_view(), name='popular-destinations'),
    path('destinations/search', DestinationSearchView.as_view(), name='search-destinations'),

    #images
    path('images', ImageCreateView.as_view(), name='image-create'),
    path('images', ImageSearchView.as_view(), name='image-search-images'),
    path('images/<int:image_id>', ImageDetailView.as_view(), name='image-detail'),

    #airlines
    path('airlines', AirlineCreateView.as_view(), name='airlines'),
    path('airlines', AirlineSearchView.as_view(), name='search-airlines'),
    path('airlines/<int:airline_id>', AirlineDetailView.as_view(), name='airline-detail'),
    path('airlines/<int:airline_id>', DeleteArilineView.as_view(), name='delete-airline'),

    #buses
    path('buses', BusCreateView.as_view(), name='buses'),
    path('buses', BusSearchView.as_view(), name='search-buses'),
    path('buses/<int:bus_id>', BusDetailView.as_view(), name='bus-detail'),
    path('buses/<int:bus_id>', DeleteBusView.as_view(), name='delete-bus'),

    #hotels
    path('hotels', HotelCreateView.as_view(), name='hotels'),
    path('hotels', HotelSearchView.as_view(), name='search-hotels'),
    path('hotels/<int:hotel_id>', HotelDetailView.as_view(), name='hotel-detail'),
    path('hotels/<int:hotel_id>', DeleteHotelView.as_view(), name='delete-hotel'),

    # TravelCost
    path('travel-cost', TravelCostCreateView.as_view(), name='travel-cost'),
    path('travel-cost', TravelCostSearchView.as_view(), name='search-travel-cost'),
]
