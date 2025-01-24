from rest_framework import serializers
from .models import Destination, TravelPlan

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'



from rest_framework import serializers
from .models import TravelPlan

class TravelPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPlan
        fields = ['destination', 'food_type', 'lodging', 'individual_count', 'start_date', 'end_date']
