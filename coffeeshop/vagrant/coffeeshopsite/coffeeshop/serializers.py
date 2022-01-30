from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['pk', 'address1', 'address2', 'city', 'postcode', 'country']
