from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

'''@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    else:
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)
'''


class Client(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(null=False)
    date_update = models.DateTimeField(null=True)
    sales_contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} : {self.last_name} {self.first_name}'


class Contrat(models.Model):
    STATUS_CHOICES = (
        (True, 'Signer'),
        (False, 'Pas signer')
    )

    sales_contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(null=False)
    date_update = models.DateTimeField(null=True)
    status = models.BooleanField(choices=STATUS_CHOICES)
    amount = models.FloatField(null=True)
    payment_due = models.DateTimeField(null=True)


class EventStatus(models.Model):
    STATUS_CHOICES = (
        ('Begin', True),
        ('End', False)
    )
    event_statu = models.CharField(max_length=255, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.event_statu}'


class Event(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    date_update = models.DateTimeField()
    support_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_statu = models.ForeignKey(EventStatus, related_name='status', on_delete=models.CASCADE)
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    note = models.TextField()


