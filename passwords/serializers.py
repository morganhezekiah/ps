from django.db.models import fields
from .models import Passwords
from rest_framework import serializers




class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model =Passwords
        fields ="__all__"