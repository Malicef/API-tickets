from django.urls import path
from . import views

urlpatterns = [
    # Eventos
    path('events/', views.EventListCreateView.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventRetrieveUpdateDestroyView.as_view(), name='event-detail'),
    path('events/<int:event_id>/tickets-available/', views.EventTicketsAvailableView.as_view(), name='event-tickets-available'),
    
    # Clientes
    path('customers/', views.CustomerListCreateView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerRetrieveUpdateDestroyView.as_view(), name='customer-detail'),
    
    # Ingressos
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('purchase/', views.PurchaseTicketView.as_view(), name='purchase-ticket'),
    
    # Notificações
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/mark-as-read/', views.NotificationMarkAsReadView.as_view(), name='notification-mark-read'),
]