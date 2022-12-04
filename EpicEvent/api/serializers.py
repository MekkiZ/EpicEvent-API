from django.contrib.auth.models import User, Group
from .models import Client, Event, EventStatus, Contrat
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name', 'groups')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])

        # Token.objects.get_or_create(user=user)

        user.save()
        return user


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
                  'client_id',
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
                  'client_id',
                  'date_created',
                  'date_update',
                  'support_contact',
                  'event_status',
                  'attendees',
                  'event_date',
                  'note'
                  ]


class EventStatusDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventStatus
        fields = ['id',
                  'event_status',
                  ]
