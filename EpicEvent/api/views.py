from django.shortcuts import render
from django.contrib.auth.models import User, Group
from api.serializers import UserSerializer, GroupSerializer, EventStatusDetailSerializers, \
    EventDetailSerializers, ContratDetailSerializers, ClientDetailSerializers
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import viewsets, status
from rest_framework import permissions, generics
import jwt, datetime
from .models import Client, Contrat, Event, EventStatus
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
    """
    Function get details to all users in API
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    """
    This function have to purpose to display the register part
    """

    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientViewSet(generics.ListAPIView):
    """
        Function get details to all users in API
        """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClientDetailSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_name', 'email']

    def get_queryset(self):
        queryset = Client.objects.all()
        return queryset

    def post(self, request, *args, **kwargs):
        if self.kwargs['last_name'] and self.kwargs['email']:
            client = Client()
            client.first_name = request.data['first_name']
            client.last_name = request.data['last_name']
            client.email = request.data['email']
            client.phone = request.data['phone']
            client.mobile = request.data['mobile']
            client.company_name = request.data['company_name']
            client.date_created = request.data['date_created']
            client.date_update = request.data['date_update']
            client.sales_contact = get_object_or_404(User, id=request.data['sales_contact'])
            data = {'first_name': client.first_name,
                    'last_name': client.last_name,
                    'email': client.email,
                    'phone': client.phone,
                    'mobile': client.mobile,
                    'company_name': client.company_name,
                    'date_created': client.date_created,
                    'date_update': client.date_update,
                    'sales_contact': client.sales_contact.id
                    }
            client.save()
            return Response(data, status=status.HTTP_201_CREATED)


class ContratViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def get(self, request, *args, **kwargs):
        contrat = Contrat.objects.all()
        serializer = ContratDetailSerializers(contrat, many=True)
        return Response(serializer.data)


class EventViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def get(self, request, *args, **kwargs):
        event = Event.objects.all()
        serializer = EventDetailSerializers(event, many=True)
        return Response(serializer.data)


class EventStatusViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def get(self, request, *args, **kwargs):
        stat_event = EventStatus.objects.all()
        serializer = EventStatusDetailSerializers(stat_event, many=True)
        return Response(serializer.data)
