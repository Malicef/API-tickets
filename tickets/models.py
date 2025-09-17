from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

class Event(models.Model):
    EVENT_TYPES = [
        ('concert', 'Concerto'),
        ('theater', 'Teatro'),
        ('sports', 'Esportes'),
        ('conference', 'Conferência'),
        ('other', 'Outro')
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    total_capacity = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Ticket(models.Model):
    TICKET_STATUS = [
        ('available', 'Disponível'),
        ('reserved', 'Reservado'),
        ('sold', 'Vendido'),
        ('cancelled', 'Cancelado')
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    ticket_code = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=TICKET_STATUS, default='available')
    purchase_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket_code} - {self.event.name}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('purchase', 'Compra'),
        ('cancellation', 'Cancelamento'),
        ('event_update', 'Atualização de Evento'),
        ('system', 'Sistema')
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.customer}"
