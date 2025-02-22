import requests
from datetime import datetime, timedelta
from django.db.models import Avg, F
import random
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .weather import get_weather
from .utils import response


User = get_user_model()
print(f"AUTH_USER_MODEL is {User}")

#Signup
class SignUpView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            print(f"Received: username={username}, email={email}, password={password}")
            if User.objects.filter(username=username).exists():
                return response.error(message= "username already exists", status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return response.error(message="email already exists", status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password)
            )
            print(f"User created: {user}")
            # Serializing user data for the response
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            return  response.success(data=user_data)
        except Exception as e:
            print(f"Error occurred: {e}")  # Log the error
            return response.error(message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return response.error(message="invalid credentials", status=status.HTTP_401_UNAUTHORIZED)

        print(f"User authenticated: {user}")
        refresh = RefreshToken.for_user(user)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        login_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user_data
        }
        return response.success(data=login_data) # Assumes response.success is replaced with Response


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return response.error(message="User not found", status=status.HTTP_404_NOT_FOUND)

        # Simulating sending an email (replace with actual email logic)
        reset_token = "RESET12345"  # You can generate a token dynamically
        send_mail(
            'Password Reset Request',
            f'Use this token to reset your password: {reset_token}',
            'noreply@gantabya.com',
            [email],
            fail_silently=False,
        )
        return response.success(message="password reset email sent")


#ImageCreateView
class ImageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        slug = request.query_params.get('slug', None)
        queryset = Image.objects.all()

        if slug is not None:
            queryset = queryset.filter(slug=slug)

        serializer = ImageSerializer(queryset, many=True)
        return response.success(serializer.data)

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.success(data=serializer.data)
        return response.error(message=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#AirlineCreateView
class AirlineCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rating = request.query_params.get('rating', None)
        destinations = Airline.objects.all()
        if rating is not None:
            queryset = queryset.filter(rating=rating)
        serializer = AirlineSerializer(destinations, many=True)
        return response.success(data=serializer.data)

    def post(self, request):
        
        serializer = AirlineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.success(data=serializer.data)
        return response.error(message=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#HotelCreateView
class HotelCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rating = request.query_params.get('rating', None)
        queryset = Hotel.objects.all()
        if rating is not None:
            queryset = queryset.filter(rating=rating)
        serializer = HotelSerializer(queryset, many=True)
        return response.success(data=serializer.data)

    def post(self, request):
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.success(data=serializer.data)
        return response.error(message=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#BusCreateView
class BusCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rating = request.query_params.get('rating', None)
        queryset = Bus.objects.all()
        if rating is not None:
            queryset = queryset.filter(rating=rating)
        serializer = BusSerializer(queryset, many=True)
        return response.success(data=serializer.data)

    def post(self, request):
        serializer = BusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.success(data=serializer.data)
        return response.error(message=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#TravelCost
class TravelCostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        destinations = TravelCost.objects.all()
        serializer = TravelCostSerializer(destinations, many=True)
        return response.success(data=serializer.data)

    def post(self, request):
        serializer = TravelCostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.success(data=serializer.data)
        return response.error(message=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#DestinationListCreateView
class DestinationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = request.query_params.get('name', None)
        queryset = Destination.objects.all()
        if name is not None:
            queryset = queryset.filter(name=name)
        serializer = DestinationSerializer(queryset, many=True)
        return response.success(data=serializer.data)

    def post(self, request):
        serializer = DestinationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.success(data=serializer.data)
        return response.error(message=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Delete account
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return response.success(message="account deleted successfully.")
    

class DeleteDestinationView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, destination_id):
        try:
            destination = Destination.objects.get(id=destination_id)
            destination.delete()
            return response.success(message="destination deleted successfully.")
        except Destination.DoesNotExist:
            return response.error(message="destination not found", status=status.HTTP_404_NOT_FOUND)
    

class DeleteArilineView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, airline_id):  
        try:
            airline = Airline.objects.get(id=airline_id)
            airline.delete()
            return response.success(message="hotel deleted successfully.")
        except Airline.DoesNotExist:
            return response.error(message="airline not found", status=status.HTTP_404_NOT_FOUND)

class DeleteBusView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, bus_id):
        try:
            bus = Bus.objects.get(id=bus_id)
            bus.delete()
            return response.success(message="bus deleted successfully.")
        except Bus.DoesNotExist:    
            return response.error(message="bus not found", status=status.HTTP_404_NOT_FOUND)
        
class DeleteHotelView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, hotel_id):
        try:
            hotel = Hotel.objects.get(id=hotel_id)
            hotel.delete()
            return response.success(message="hotel deleted successfully.")
        except Hotel.DoesNotExist:
            return response.error(message="hotel not found", status=status.HTTP_404_NOT_FOUND)
        
class PopularDestinationsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        popular_destinations = Destination.objects.order_by('-popularity')[:10]
        serializer = DestinationSerializer(popular_destinations, many=True)
        return response.success(data=serializer.data)
    

class ImageSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'slug']
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class AirlineSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'price']
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer

class HotelSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'price']
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class BusSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'price']
    queryset = Bus.objects.all()
    serializer_class = BusSerializer


class DestinationSearchView(ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description', 'location']

class TravelCostSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'price']
    queryset = TravelCost.objects.all()
    serializer_class = TravelCostSerializer


class DestinationDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, destination_id):
        try:
            destination = Destination.objects.get(id=destination_id)
            weather_data = get_weather(destination.name)
            response_data =  {
                "destination": {
                    "name": destination.name,
                    "image":destination.image,
                    "description": destination.description,
                    "location": destination.location,
                    "popularity": destination.popularity,
                    "longitude": destination.longitude,
                    "latitude": destination.latitude
                },
                "weather": weather_data
            }
            return response.success(data=response_data)
        except Destination.DoesNotExist:
            return response.error(message="destination not found", status=status.HTTP_404_NOT_FOUND)
        
class DestinationListAirlineView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, destination_id):
        try:
            data = Airline.objects.filter(destinationID=destination_id)
            serializer = AirlineSerializer(data, many=True)
            return response.success(data=serializer.data)
        except Destination.DoesNotExist:
            return response.error(message="destination not found", status=status.HTTP_404_NOT_FOUND)

class DestinationListHotelView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, destination_id):
        try:
            data = Hotel.objects.filter(destinationID=destination_id)
            serializer = HotelSerializer(data, many=True)
            return response.success(data=serializer.data)
        except Destination.DoesNotExist:
            return response.error(message="destination not found", status=status.HTTP_404_NOT_FOUND)
        
class DestinationListBusView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, destination_id):
        try:
            data = Bus.objects.filter(destinationID=destination_id)
            serializer = BusSerializer(data, many=True)
            return response.success(data=serializer.data)
        except Destination.DoesNotExist:
            return response.error(message="destination not found", status=status.HTTP_404_NOT_FOUND)    
        

class DestinationSearchView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Retrieve the search query; default to empty string if not provided
        query = request.query_params.get('search', '').lower()
        destinations = list(Destination.objects.all())
        if query:
            filtered_destinations = []
            for destination in destinations:
                if (query in destination.name.lower() or 
                    query in destination.description.lower() or 
                    query in destination.location.lower()):
                    filtered_destinations.append(destination)
        else:
            # If no search query, return all destinations
            filtered_destinations = destinations
        
        serializer = DestinationSerializer(filtered_destinations, many=True)
        return response.success(data=serializer.data)

class PopularDestinationsView(APIView):
    permission_classes = [IsAuthenticated]
    def merge_sort_destinations(self, destinations):
        # Base case: if the list has 0 or 1 elements, it is already sorted.
        if len(destinations) <= 1:
            return destinations
        mid = len(destinations) // 2
        left = self.merge_sort_destinations(destinations[:mid])
        right = self.merge_sort_destinations(destinations[mid:])
        return self.merge(left, right)
    def merge(self, left, right):
        sorted_list = []
        i, j = 0, 0

        # Since we want the most popular destinations first,
        # we compare such that higher popularity comes before lower.
        while i < len(left) and j < len(right):
            if left[i].popularity >= right[j].popularity:
                sorted_list.append(left[i])
                i += 1
            else:
                sorted_list.append(right[j])
                j += 1
        # Append any remaining items
        sorted_list.extend(left[i:])
        sorted_list.extend(right[j:])
        return sorted_list

    def get(self, request):
        # Retrieve all destinations from the database
        destinations = list(Destination.objects.all())
        # Sort destinations by popularity in descending order
        sorted_destinations = self.merge_sort_destinations(destinations)
        # Select the top 10 destinations
        popular_destinations = sorted_destinations[:10]
        serializer = DestinationSerializer(popular_destinations, many=True)
        return response.success(data=serializer.data)
    
# OptimalCost
class OptimalCostView(APIView):
    def get(self, request, destination_id):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        budget = request.query_params.get("budget")

        if not all([destination_id, start_date_str, end_date_str, budget]):
            return response.error(message="Missing required parameters", status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            budget = float(budget)
            destination_id = int(destination_id) #ensure it is an integer for querying
        except ValueError:
            return response.error(message="Invalid date format", status=status.HTTP_400_BAD_REQUEST)

        response_data = cost_estimation(destination_id, start_date, end_date, budget)

        return response.success(data={"estimated_cost": response_data})

class UserTravelCostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        total_cost = 0.0
        days=0.0
        try:
            data = TravelCost.objects.filter(userID=user_id)
            for i in data:
                duration_days = (i.end_date - i.start_date).days
                total_cost += i.price*duration_days
            serializer = TravelCostSerializer(data, many=True)
            response_data = {
                "items": serializer.data,
                "total_cost": total_cost
                }
            return response.success(data=response_data)
        except Destination.DoesNotExist:
            return response.error(message="destination not found", status=status.HTTP_404_NOT_FOUND)
              
class AirlineDetailView(APIView):
    def get(self, request, airline_id):
        try:
            data = Airline.objects.get(id=airline_id)
            print("data ",data.destinationID,data.id)
            response_data =  {
                    "id": data.id,
                    "createdAt": data.createdAt,
                    "name": data.name,
                    "price":data.price,
                    "rating": data.rating,
                    "timeTaken": data.timeTaken,
                    "remarks": data.remarks,
                    "destinationID": data.destinationID.id,
                    "location": data.destinationID.name,
                }
            return response.success(data=response_data)
        except Destination.DoesNotExist:
            return response.error(message="airline not found", status=status.HTTP_404_NOT_FOUND)
        
class ImageDetailView(APIView):
    def get(self, request, image_id):
        try:
            data = Image.objects.get(id=image_id)
            response_data =  {
                    "id": data.id,
                    "createdAt": data.createdAt,
                    "name": data.name,
                    "slug":data.slug,
                    "url": data.url
                }
            return response.success(data=response_data)
        except Destination.DoesNotExist:
            return response.error(message="image not found", status=status.HTTP_404_NOT_FOUND)
        
class HotelDetailView(APIView):
    def get(self, request, hotel_id):
        try:
            data = Hotel.objects.get(id=hotel_id)
            response_data =  {
                    "id": data.id,
                    "createdAt": data.createdAt,
                    "name": data.name,
                    "Price":data.price,
                    "rating": data.rating,
                    "remarks": data.remarks,
                    "anemeties":data.anemeties,
                    "destinationID": data.destinationID.id,
                     "location": data.destinationID.name,
                }
            return response.success(data=response_data)
        except Destination.DoesNotExist:
            return response.error(message="hotel not found", status=status.HTTP_404_NOT_FOUND)
        
class BusDetailView(APIView):
    def get(self, request, bus_id):
        try:
            data = Bus.objects.get(id=bus_id)
            response_data =  {
                    "id": data.id,
                    "createdAt": data.createdAt,
                    "name": data.name,
                    "price":data.price,
                    "rating": data.rating,
                    "timeTaken": data.timeTaken,
                    "remarks": data.remarks,
                    "destinationID": data.destinationID.id,
                    "location": data.destinationID.name,
                }
            return response.success(data=response_data)
        except Destination.DoesNotExist:
            return response.error(message="bus not found", status=status.HTTP_404_NOT_FOUND)

def calculate_cost(travel_plan):
    base_food_cost = 10 if travel_plan.food_type == 'Veg' else 15
    base_lodging_cost = {
        'Hotel': 100,
        'Lodge': 70,
        'Resort': 200
    }.get(travel_plan.lodging, 0)

    # Calculate duration in days
    start_date = travel_plan.start_date
    end_date = travel_plan.end_date
    duration = (end_date - start_date).days

    # Calculate Total Cost
    total_cost = (
        base_food_cost * travel_plan.individual_count +
        base_lodging_cost * duration
    )
    return total_cost

def calculate_pricing_segment(total_cost):
    """Determine pricing segment based on total cost."""
    if total_cost < 500:
        return "Budget"
    elif 500 <= total_cost < 1000:
        return "Standard"
    else:
        return "Premium"

def fetch_travel_options(destination, food_type, lodging):
    """Return travel options based on input criteria."""
    # Simulating travel options based on the destination
    options = {
        "Local": ["Bus", "Train", "Car"],
        "International": ["Flight", "Cruise"]
    }
    return options.get(destination.destination_type, ["Unknown"])


def fetch_weather_data(city_name):
    """Fetch weather data from an external API."""
    api_key = "7f5b5289cf6bb8fbb9342592f2adeee6"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # Optional: Change to 'imperial' for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    except requests.exceptions.HTTPError as http_err:
        return {
            "error": "Unable to fetch weather data",
            "details": str(http_err)
        }
    except requests.exceptions.RequestException as req_err:
        return {
            "error": "Request failed",
            "details": str(req_err)
        }
    
def cost_estimation(destination_id, start_date, end_date, budget):
    """
    Estimates the optimized travel cost for a given destination, returning
    a list of dictionaries, each containing a title and optimized cost.
    """
    date_range_start = start_date - timedelta(days=365)
    date_range_end = start_date + timedelta(days=365)

    historical_data = TravelCost.objects.filter(
        destinationID=destination_id,
        start_date__range=[date_range_start, date_range_end]
    ).annotate(
        year=F('start_date__year'),
        month=F('start_date__month')
    ).values('title', 'price', 'start_date')

    optimized_costs = []
    total_optimized_cost = 0.0

    for item in historical_data:
        title = item['title']
        price = item['price']

        # Apply seasonality adjustment (example logic)
        month = item['start_date'].month
        peak_season_months = [6, 7, 8, 12, 1]
        if month in peak_season_months:
            price *= random.uniform(1.1, 1.2)
        else:
            price *= random.uniform(0.9, 0.95)

        # Apply budget constraint (example logic)
        if price > budget:
            price = budget * 0.9

        optimized_costs.append({"title": title, "cost": price})
        total_optimized_cost += price

    return optimized_costs, total_optimized_cost