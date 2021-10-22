from rest_framework import serializers

from register.models import Client, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["first_name", "last_name", "cpf", "email", "document"]


#class CompanySerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Company
#        fields = ["useres", "cnpj"]


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}