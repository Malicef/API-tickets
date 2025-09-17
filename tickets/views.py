from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from .models import Event, Customer, Ticket, Notification
from .serializers import (
    EventSerializer, CustomerSerializer, TicketSerializer,
    NotificationSerializer, PurchaseTicketSerializer
)
import uuid

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        customer = get_object_or_404(Customer, user=user)
        return Ticket.objects.filter(customer=customer)

class PurchaseTicketView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PurchaseTicketSerializer(data=request.data)
        if serializer.is_valid():
            event_id = serializer.validated_data['event_id']
            quantity = serializer.validated_data['quantity']
            
            try:
                with transaction.atomic():
                    event = Event.objects.select_for_update().get(id=event_id, is_active=True)
                    
                    if event.available_tickets < quantity:
                        return Response(
                            {'error': 'Ingressos insuficientes'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    customer = get_object_or_404(Customer, user=request.user)
                    tickets = []
                    
                    for _ in range(quantity):
                        ticket = Ticket(
                            event=event,
                            customer=customer,
                            ticket_code=f"TKT-{uuid.uuid4().hex[:8].upper()}",
                            price=event.price,
                            status='sold',
                            purchase_date=timezone.now()
                        )
                        tickets.append(ticket)
                    
                    Ticket.objects.bulk_create(tickets)
                    event.available_tickets -= quantity
                    event.save()
                    
                    # Criar notificação
                    Notification.objects.create(
                        customer=customer,
                        title="Compra realizada",
                        message=f"Você comprou {quantity} ingresso(s) para {event.name}",
                        notification_type='purchase'
                    )
                    
                    return Response(
                        {'message': 'Compra realizada com sucesso', 'tickets': len(tickets)},
                        status=status.HTTP_201_CREATED
                    )
                    
            except Event.DoesNotExist:
                return Response(
                    {'error': 'Evento não encontrado ou inativo'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = get_object_or_404(Customer, user=self.request.user)
        return Notification.objects.filter(customer=customer).order_by('-created_at')

class NotificationMarkAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        customer = get_object_or_404(Customer, user=request.user)
        notification = get_object_or_404(Notification, id=pk, customer=customer)
        
        notification.is_read = True
        notification.save()
        
        return Response({'message': 'Notificação marcada como lida'})

class EventTicketsAvailableView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        return Response({
            'event': event.name,
            'available_tickets': event.available_tickets,
            'total_capacity': event.total_capacity
        })