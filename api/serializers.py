from rest_framework import serializers
from .models import Destination, TravelPlan,Image,Airline,Bus,Hotel

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'

    def validate(self, data):
        """
        Check that the DestinationID exists.
        """
        destination_id = data.get('DestinationID')
        if destination_id:
            try:
                Destination.objects.get(pk=destination_id.id)
            except Destination.DoesNotExist:
                raise serializers.ValidationError("Invalid DestinationID: Destination does not exist.")
        else:
            raise serializers.ValidationError("DestinationID is required.")
        return data

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'
    def validate(self, data):
        """
        Check that the DestinationID exists.
        """
        destination_id = data.get('DestinationID')
        if destination_id:
            try:
                Destination.objects.get(pk=destination_id.id)
            except Destination.DoesNotExist:
                raise serializers.ValidationError("Invalid DestinationID: Destination does not exist.")
        else:
            raise serializers.ValidationError("DestinationID is required.")
        return data


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

    def validate(self, data):
        """
        Check that the DestinationID exists.
        """
        destination_id = data.get('DestinationID')
        if destination_id:
            try:
                Destination.objects.get(pk=destination_id.id)
            except Destination.DoesNotExist:
                raise serializers.ValidationError("Invalid DestinationID: Destination does not exist.")
        else:
            raise serializers.ValidationError("DestinationID is required.")
        return data

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


from rest_framework import serializers
from .models import TravelPlan

class TravelPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPlan
        fields = ['destination', 'food_type', 'lodging', 'individual_count', 'start_date', 'end_date']
