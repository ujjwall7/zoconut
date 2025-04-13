from rest_framework import serializers
from . models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ClientAppointmentsSerializers(serializers.ModelSerializer):
    client = UserSerializer()
    class Meta:
        model = ClientAppointment
        fields = "__all__"



# abceeeee




