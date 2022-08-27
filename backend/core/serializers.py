from rest_framework import serializers
from core.models import  Blotter, User



class BlotterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blotter
        fields=(
                                  "id",
                                  "user",
                                  "ticker",
                                  "volume",
                                  "price"
                )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=(
                                "email",
                                "name",
                )
