from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('account_holder', 'Account Holder'),
    )
    name = models.CharField(max_length=100, null=True)
    primary_number = models.CharField(max_length=15, null=True)
    country_code = models.CharField(max_length=5, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

class ClientAppointment(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    )

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', null=True)
    appointment_datetime = models.DateTimeField(null=True)
    account_holder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_user', null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed', null=True)
    timestamp = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.client.name} - {self.status} - {self.appointment_datetime.strftime('%Y-%m-%d %H:%M')}"
    

# abcooo