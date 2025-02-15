from django.urls import path
from .views import SignUpView, LoginView, ForgotPasswordView,ImageCreateView,ImageSearchView, DestinationListCreateView, DeleteAccountView, PopularDestinationsView, DestinationSearchView, DestinationDetailView, TravelPlanCreateView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='token_obtain_pair'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('delete-account', DeleteAccountView.as_view(), name='delete-account'),


    path('destinations', DestinationListCreateView.as_view(), name='destination-list-create'),
    path('destinations', DestinationSearchView.as_view(), name='search-destinations'),
    path('destinations/popular', PopularDestinationsView.as_view(), name='popular-destinations'),
    path('destinations/<int:destination_id>', DestinationDetailView.as_view(), name='destination-detail'),

    path('travel-plans', TravelPlanCreateView.as_view(), name='travel-plans'),

    path('images', ImageCreateView.as_view(), name='image-create'),
    path('images', ImageSearchView.as_view(), name='image-search-images'),
]
