from rest_framework import serializers
from .models import auth

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = auth
        fields = [  "name",
                    "email",
                    "phone",
                    "freelancer",
                    "created_date",
                    "verified",
                    "token",
                    "lastseen" ]