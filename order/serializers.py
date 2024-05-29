from rest_framework import serializers
from .models import user
from .utils import isEmailValid, isPhoneValid

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model=user
        fields='__all__'
    def validate(self, attrs):
        if  not (attrs['email']==None or attrs['email']=='' or isEmailValid(attrs['email']) ):
            raise serializers.ValidationError(
            {"error": "Email isn't valid."})
        if not (attrs['phoneNumber']==None or attrs['phoneNumber']=='' or isPhoneValid(attrs['phoneNumber']) ):
            raise serializers.ValidationError(
            {"error": "phone no. isn't valid."})
        return attrs

        


class contactSerializer(serializers.Serializer):
    primaryContatctId = serializers.IntegerField(default=None)
    emails = serializers.ListField(
        child = serializers.EmailField(max_length=100)
    )
    phoneNumbers = serializers.ListField(
        child = serializers.CharField(max_length=15)
    )
    secondaryContactIds = serializers.ListField(
        child = serializers.IntegerField()
    )