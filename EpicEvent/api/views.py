from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from api.serializers import UserSerializer, GroupSerializer, EventStatusDetailSerializers, \
    EventDetailSerializers, ContratDetailSerializers, ClientDetailSerializers
from django.db.models import Q
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import viewsets, status
from rest_framework import permissions
from .models import Client, Contrat, Event, EventStatus
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from api.permissions import IsAdminAuthenticated, ReadOnly

import logging

logger = logging.getLogger('log')


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        user = User.objects.all()
        if user.exists():
            fre = user.all().first()
            my_group = Group.objects.get(name='team_gestion')
            my_group.user_set.add(fre)
            print(fre)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



        hr = User.objects.get(id=self.request.user.id)
        # id_group_from_user = hr.groups.all().values_list('id', flat=True)[0]
        groups = hr.groups.all().values_list('name', flat=True)[0]
        group = Group.objects.get(name='team_gestion').name
        try:
            if groups == group:
                logger.info(f"One user of {group} is here")
                return User.objects.all().order_by('-date_joined')
            else:
                logger.error("You don't have the permission for this part")
                raise NotFound
        except ValueError as e:
            logger.error(e)
            raise e

    def create(self, *args, **kwargs):
        hr = User.objects.get(id=self.request.user.id)
        # id_group_from_user = hr.groups.all().values_list('id', flat=True)[0]
        groups = hr.groups.all().values_list('name', flat=True)[0]
        group = Group.objects.get(name='team_gestion').name
        try:
            if self.request.method == 'POST':
                if groups == group:
                    logger.info(f"The user of {group} is here")
                    user = User.objects.create(
                        username=self.request.data['username'],
                        email=self.request.data['email'],
                        first_name=self.request.data['first_name'],
                        last_name=self.request.data['last_name'],
                        password=make_password(self.request.data['password']),

                    )

                    user.set_password(self.request.data['password'])

                    # Token.objects.get_or_create(user=user)
                    user_group = Group.objects.get(id=self.request.data['groups'])
                    user.groups.add(user_group)
                    user_group.save()
                    user.save()
                    logger.info(f"one user has created")
                    return Response(UserSerializer(user).data)
                else:
                    logger.info("The user haven't the rights for add something here")
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                logger.error("Wrong method")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except ConnectionError as c:
            logger.critical("Be Careful someone try to send data with wrong method")
            raise c


class ClientFilterViewSet(viewsets.ModelViewSet):
    """
        Function get details to all users in API
        """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClientDetailSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_name', 'email']

    def get_queryset(self):
        table_id_for_support = []
        user_for_client = User.objects.get(id=self.request.user.id)
        # id_group_from_user = hr.groups.all().values_list('id', flat=True)[0]
        groups = user_for_client.groups.all().values_list('name', flat=True)[0]
        group = Group.objects.get(name='team_sales').name
        group_2 = Group.objects.get(name='team_gestion').name
        group_3 = Group.objects.get(name='team_support').name
        try:
            if groups == group:
                logger.info(f"One user of {group} is here")
                return Client.objects.filter(sales_contact=user_for_client.id)
            elif groups == group_2:
                logger.info(f"One user of {group_2} is here")
                return Client.objects.all()
            elif groups == group_3:
                logger.info(f"One user of {group_3} is here")
                event = Event.objects.filter(support_contact=user_for_client)
                for i in event.all():
                    table_id_for_support.append(i.client.id)
                return Client.objects.filter(pk__in=table_id_for_support)
            else:
                logger.error("The user has no rights to be here")
                raise NotFound
        except ConnectionRefusedError as e:
            logger.info(e)
            raise e

    def create(self, *args, **kwargs):
        user_for_client = User.objects.get(id=self.request.user.id)
        # id_group_from_user = hr.groups.all().values_list('id', flat=True)[0]
        groups = user_for_client.groups.all().values_list('id', flat=True)[0]
        group = Group.objects.get(name='team_sales').id
        group_2 = Group.objects.get(name='team_gestion').id
        try:

            if (groups == group) or (groups == group_2):
                print('je suis ici')
                logger.info(f"One user of {group} ou {group_2} is here")
                client = Client.objects.create(
                    first_name=self.request.data['first_name'],
                    last_name=self.request.data['last_name'],
                    email=self.request.data['email'],
                    phone=self.request.data['phone'],
                    mobile=(self.request.data['mobile']),
                    company_name=self.request.data['company_name'],
                    date_created=self.request.data['date_created'],
                    date_update=self.request.data['date_update'],
                    sales_contact=get_object_or_404(User, id=user_for_client.id),

                )
                client.save()
                logger.info(f"One client has been created")
                return Response(ClientDetailSerializers(client).data)

            else:
                logger.error(f"User has no rights here")
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except PermissionError as p:
            logger.error(p)
            raise p

    def update(self, request, *args, **kwargs):
        hr = User.objects.get(id=self.request.user.id)
        groups = hr.groups.all().values_list('name', flat=True)[0]
        group = Group.objects.get(name='team_sales').name
        group_2 = Group.objects.get(name='team_gestion').name
        client = Client.objects.get(id=self.kwargs['pk'])
        sale_cont = client.sales_contact.id

        try:
            if request.method == 'PUT':
                if (groups == group_2) or (sale_cont.id == hr.id and groups == group):
                    logger.info(f"One user of {group} or {group_2} is here")

                    client.last_name = request.data['last_name']
                    client.email = request.data['email']
                    client.phone = request.data['phone']
                    client.mobile = request.data['mobile']
                    client.company_name = request.data['company_name']
                    client.date_created = request.data['date_created']
                    client.date_update = request.data['date_update']
                    client.first_name = request.data['first_name']
                    client.save()
                    logger.info(f"One client has been updated")
                    return Response(ClientDetailSerializers(client).data,
                                    status=status.HTTP_200_OK)
                else:
                    logger.error(f"User has no rights here")
                    return Response(status.HTTP_401_UNAUTHORIZED)
            else:
                Response(status.HTTP_400_BAD_REQUEST)
        except PermissionError as p:
            logger.error(p)
            raise p


class ContratFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='client__email', lookup_expr='exact')
    client = filters.CharFilter(field_name='client__last_name', lookup_expr='exact')
    date_created = filters.DateFilter(field_name='date_created', lookup_expr='icontains')
    amount = filters.NumberFilter(field_name='amount', lookup_expr='exact')

    class Meta:
        model: Contrat


class ContratViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ContratDetailSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContratFilter

    def get_queryset(self):
        hr = User.objects.get(id=self.request.user.id)
        # id_group_from_user = hr.groups.all().values_list('id', flat=True)[0]
        groups = hr.groups.all().values_list('name', flat=True)[0]
        group = Group.objects.get(name='team_sales').name
        group_2 = Group.objects.get(name='team_gestion').name
        try:
            if groups == group:
                logger.info(f"One user of {group} is here")
                return Contrat.objects.filter(sales_contact=hr.id)
            elif groups == group_2:
                logger.info(f"One user of {group_2} is here")
                return Contrat.objects.all()
            else:
                logger.info(f"User{hr} has no rights here ")
                raise NotFound
        except PermissionError as p:
            raise p

    def create(self, *args, **kwargs):
        hr = User.objects.get(id=self.request.user.id)
        # id_group_from_user = hr.groups.all().values_list('id', flat=True)[0]
        groups = hr.groups.all().values_list('name', flat=True)[0]
        group = Group.objects.get(name='team_sales').name
        group_2 = Group.objects.get(name='team_gestion').name
        try:
            if (groups == group) or (groups == group_2):
                logger.info(f"User from {group} or {group_2} was here ")
                contrat = Contrat.objects.create(
                    payment_due=self.request.data['payment_due'],
                    amount=(self.request.data['amount']),
                    status=self.request.data['status'],
                    date_created=self.request.data['date_created'],
                    date_update=self.request.data['date_update'],
                    sales_contact=get_object_or_404(User, id=hr.id),
                    client=get_object_or_404(Client, id=self.request.data['client']),

                )

                data = {'client': contrat.client.id,
                        'payment_due': contrat.payment_due,
                        'amount': contrat.amount,
                        'status': contrat.status,
                        'date_created': contrat.date_created,
                        'date_update': contrat.date_update,
                        'sales_contact': contrat.sales_contact.id
                        }
                contrat.save()
                logger.info(f"Contract has been created ")
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"User{hr} has no rights here ")
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except PermissionError as p:
            logger.error(p)
            raise p

    def update(self, request, *args, **kwargs):
        hr = User.objects.get(id=self.request.user.id)
        groups = hr.groups.all().values_list('name', flat=True)[0]
        group = Group.objects.get(name='team_sales').name
        group_2 = Group.objects.get(name='team_gestion').name
        contrat = Contrat.objects.get(id=kwargs['pk'])
        try:
            if request.method == 'PUT':
                if (groups == group_2) or (contrat.sales_contact.id == hr.id and groups == group):
                    logger.error(f'The user is from {group_2} or {group}')
                    contrat.sales_contact = get_object_or_404(User, id=hr.id)
                    contrat.client = get_object_or_404(Client, id=request.data['client'])
                    contrat.amount = request.data['amount']
                    contrat.status = request.data['status']
                    contrat.date_created = request.data['date_created']
                    contrat.date_update = request.data['date_update']
                    contrat.payment_due = request.data['payment_due']
                    contrat.save()
                    logger.info(f'One contract has been updated')
                    return Response(ContratDetailSerializers(contrat).data,
                                    status=status.HTTP_200_OK)
                else:
                    return Response(status.HTTP_401_UNAUTHORIZED)
            else:
                logger.error(f'The user has no rights here')
                Response(status.HTTP_400_BAD_REQUEST)
        except PermissionError as p:
            logger.error(p)
            raise p


class EventFilter(filters.FilterSet):
    client = filters.CharFilter(field_name='client__last_name', lookup_expr='exact')
    email = filters.CharFilter(field_name='client__email', lookup_expr='exact')
    event_date = filters.DateFilter(field_name='event_date', lookup_expr='icontains')

    class Meta:
        model: Event


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventDetailSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_queryset(self):
        hr = User.objects.get(id=self.request.user.id)
        # id_group_from_user = hr.groups.all().values_list('id', flat=True)[0]
        groups = hr.groups.all().values_list('name', flat=True)[0]
        group = Group.objects.get(name='team_sales').name
        group_2 = Group.objects.get(name='team_gestion').name
        group_3 = Group.objects.get(name='team_support').name
        try:
            if groups == group_3:
                logger.info(f'The user is from {group_3}')
                return Event.objects.filter(support_contact=hr.id)
            elif groups == group:
                logger.info(f'The user is from {group}')
                client = Client.objects.filter(sales_contact=hr.id)
                event = Event.objects.filter(client__in=client)
                return event
                # return  Event.objects.all()
            elif groups == group_2:
                logger.info(f'The user is from {group_2}')
                return Event.objects.all()
            else:
                logger.error(f'User has no rights here for this queryset')
                raise NotFound
        except ValueError as e:
            logger.error(e)
            raise e

    def create(self, *args, **kwargs):
        list_sign = []
        hr = User.objects.get(id=self.request.user.id)
        # id_group_from_user = hr.groups.all().values_list('id', flat=True)[0]
        groups = hr.groups.all().values_list('name', flat=True)[0]
        group = Group.objects.get(name='team_sales').name
        group_2 = Group.objects.get(name='team_gestion').name
        event = Event.objects.all().values_list('client', flat=True)
        contrat = Contrat.objects.filter(Q(client__in=event) & Q(status=False)).values()
        client = get_object_or_404(Client, id=self.request.data['client'])
        contrat_bis = Contrat.objects.get(client = client)
        print(client)
        print(contrat_bis.status)
        for i in contrat:
            list_sign.append(i['client_id'])
        event_id = get_object_or_404(Client, id=self.request.data['client'])

        '''if event_id.id in list_sign:
            print('je suis ici')
            logger.info('The user has try to creat contract but the client has not signed it')
            return Response(data={"You can't create event because this client have not sign the contract"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        else:'''
        if (groups == group) or (groups == group_2):
            logger.error(f'The user is from {group_2} or {group}')
            event = Event.objects.create(
                note=self.request.data['note'],
                event_date=self.request.data['event_date'],
                attendees=self.request.data['attendees'],
                date_created=self.request.data['date_created'],
                date_update=self.request.data['date_update'],
                event_statu=get_object_or_404(EventStatus, id=self.request.data['event_statu']),
                client=get_object_or_404(Client, id=self.request.data['client']),
                support_contact=get_object_or_404(User, id=self.request.data['support_contact']),
            )
            print(contrat_bis.status)
            if contrat_bis.status is True:
                print('tu nai aps sence me voir')
                event.save()
                logger.info(f"One event has been created")
                return Response(EventDetailSerializers(event).data)
            elif contrat_bis.status is False:
                Event.objects.filter(id=event.id).delete()
                print('tu est s=censer enm voire')
                logger.info('The user has try to creat contract but the client has not signed it')
                return Response(data={"You can't create event because this client have not sign the contract"},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            logger.error(f'The user has no rights for create some Events')
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk, *args, **kwargs):
        hr = User.objects.get(id=request.user.id)
        groups = hr.groups.all().values_list('name', flat=True)[0]
        group = Group.objects.get(name='team_support').name
        group_2 = Group.objects.get(name='team_gestion').name
        event = Event.objects.get(id=pk)
        sale_co = Client.objects.get(id=event.client.id)
        vendeur = sale_co.sales_contact.id
        username_current = request.user.username
        try:
            if request.method == 'PUT':
                logger.info(f'Some on has send event updating')
                if (groups == group or group_2) or (event.support_contact == username_current and sale_co.id == hr.id) \
                        or (vendeur == hr.id):
                    logger.info(f'first condition passed by user')
                    if str(event.event_statu) != 'End' or groups == group_2:
                        logger.info(f'last conduition pass by {hr}')
                        logger.error(f'The user is from {group_2} or {group}')
                        event.note = request.data['note']
                        event.event_date = request.data['event_date']
                        event.attendees = request.data['attendees']
                        event.date_created = request.data['date_created']
                        event.date_update = request.data['date_update']
                        event.event_statu = get_object_or_404(EventStatus, id=request.data['event_statu'])
                        event.client = get_object_or_404(Client, id=request.data['client'])
                        event.support_contact = get_object_or_404(User, id=request.data['support_contact'])
                        event.save()
                        logger.info(f'Event has been updating')
                        return Response(EventDetailSerializers(event).data, status.HTTP_200_OK)
                    else:
                        logger.info("the user has no rights to update event")
                        return Response(status.HTTP_401_UNAUTHORIZED)
            else:
                logger.error(f'Wrong method used for update event')
                return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
        except PermissionError as p:
            logger.error(p)
            raise p


class EventStatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = EventStatusDetailSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        stat_event = EventStatus.objects.all()
        return stat_event
