from django.contrib import admin
from .models import Event, Customer, Ticket, Notification

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_type', 'date', 'location', 'available_tickets', 'is_active']
    list_filter = ['event_type', 'is_active', 'date']
    search_fields = ['name', 'location']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'birth_date', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_code', 'event', 'customer', 'status', 'price', 'purchase_date']
    list_filter = ['status', 'event']
    search_fields = ['ticket_code', 'event__name']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']
    search_fields = ['title', 'message', 'customer__user__username']