import requests
from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from .serializers import DestinationSerializer, TravelPlanSerializer,ImageSerializer,AirlineSerializer,HotelSerializer,BusSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from .models import Destination,Image,TravelPlan,Airline,Hotel,Bus
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
            return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)

        # Simulating sending an email (replace with actual email logic)
        reset_token = "RESET12345"  # You can generate a token dynamically
        send_mail(
            'Password Reset Request',
            f'Use this token to reset your password: {reset_token}',
            'noreply@gantabya.com',
            [email],
            fail_silently=False,
        )
        return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)




#ImageCreateView
class ImageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        destinations = Image.objects.all()
        serializer = ImageSerializer(destinations, many=True)
        return response.success(data=serializer.data)

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
        destinations = Airline.objects.all()
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
        destinations = Hotel.objects.all()
        serializer = HotelSerializer(destinations, many=True)
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
        destinations = Bus.objects.all()
        serializer = BusSerializer(destinations, many=True)
        return response.success(data=serializer.data)

    def post(self, request):
        serializer = BusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.success(data=serializer.data)
        return response.error(message=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#DestinationListCreateView
class DestinationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        destinations = Destination.objects.all()
        serializer = DestinationSerializer(destinations, many=True)
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
    def get(self, request):
        popular_destinations = Destination.objects.order_by('-popularity')[:10]
        serializer = DestinationSerializer(popular_destinations, many=True)
        return Response(serializer.data, status=200)
    

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


class DestinationDetailView(APIView):
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

# class DestinationDetailView(RetrieveAPIView):
#     queryset = Destination.objects.all()
#     serializer_class = DestinationSerializer
#     lookup_field = 'id'  # ID to be used in the URL


# #Travel Plan
# class TravelPlanCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = TravelPlanSerializer(data=request.data)
#         if serializer.is_valid():
#             travel_plan = serializer.save(user=request.user)
#             total_cost = calculate_cost(travel_plan)  # Calculate cost
#             travel_plan.total_cost = total_cost
#             travel_plan.save()  # Save the total cost to the database
#             return Response(
#                 {"message": "Travel plan created", "total_cost": total_cost},
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def calculate_cost(travel_plan):
    # Example Base Costs
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

class TravelPlanCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TravelPlanSerializer(data=request.data)
        if serializer.is_valid():
            travel_plan = serializer.save()
            travel_plan.total_cost = calculate_cost(travel_plan)  # Calculate Cost
            # Calculate the total cost
            duration = (travel_plan.end_date - travel_plan.start_date).days
            base_cost = {
                'Veg': 100,
                'Non-Veg': 200,
            }[travel_plan.food_type] * travel_plan.individual_count

            lodging_cost = {
                'Hotel': 1000,
                'Lodge': 500,
                'Resort': 2000,
            }[travel_plan.lodging] * duration * travel_plan.individual_count

            total_cost = base_cost + lodging_cost
            # Apply discounts
            discount = 0
            if duration > 7:
                discount += 0.10 * total_cost  # 10% duration discount
            if travel_plan.individual_count > 5:
                discount += 0.15 * total_cost  # 15% group discount

            discounted_total = total_cost - discount

            travel_plan.pricing_segment = calculate_pricing_segment(travel_plan.total_cost)  # Determine Pricing Segment
            travel_plan.travel_options = fetch_travel_options(travel_plan.destination, travel_plan.food_type, travel_plan.lodging)  # Fetch Travel Options
            travel_plan.save()
            # return Response({"message": "Travel plan created", "total_cost": travel_plan.total_cost,
            #         "pricing_segment": travel_plan.pricing_segment,
            #         "travel_options": travel_plan.travel_options,}, status=status.HTTP_201_CREATED)
            return Response({
                "message": "Travel plan created successfully.",
                "total_cost": total_cost,
                "discount": discount,
                "final_price": discounted_total,
                "details": {
                    "destination": travel_plan.destination.name,
                    "duration": duration,
                    "individual_count": travel_plan.individual_count,
                    "lodging": travel_plan.lodging,
                    "food_type": travel_plan.food_type,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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