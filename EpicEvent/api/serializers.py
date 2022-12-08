from django.contrib.auth.models import User, Group
from .models import Client, Event, EventStatus, Contrat
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2',
                  'email', 'first_name', 'last_name', 'groups')

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ClientDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'mobile',
                  'company_name',
                  'date_created',
                  'date_update',
                  'sales_contact']


class ContratDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contrat
        fields = ['id',
                  'sales_contact',
                  'client',
                  'date_created',
                  'date_update',
                  'status',
                  'amount',
                  'payment_due'
                  ]


class EventDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id',
                  'client',
                  'date_created',
                  'date_update',
                  'support_contact',
                  'event_statu',
                  'attendees',
                  'event_date',
                  'note'
                  ]


class EventStatusDetailSerializers(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = EventStatus
        fields = ('id',
                  'event_statu',
                  'status',)
