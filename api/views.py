from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Movie, Session, Booking
from .serializers import MovieSerializer, SessionSerializer, BookingSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            qs = qs.filter(activa=True)
        return qs

    @action(detail=True, methods=['get'])
    def sessions(self, request, pk=None):
        movie = self.get_object()
        serializer = SessionSerializer(movie.sessions.all(), many=True)
        return Response(serializer.data)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related('movie').all()
    serializer_class = SessionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            qs = qs.filter(movie__activa=True, asientos_disponibles__gt=0)
        return qs

    @action(detail=False, methods=['get'], url_path='by_movie')
    def by_movie(self, request):
        movie_id = request.query_params.get('movie_id')
        if not movie_id:
            return Response([], status=status.HTTP_200_OK)
        qs = self.get_queryset().filter(movie_id=movie_id)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('session').all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = serializer.validated_data['session']
        cantidad = serializer.validated_data['cantidad_asientos']
        if session.asientos_disponibles < cantidad:
            return Response(
                {'detail': 'No hay suficientes asientos disponibles.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        session.asientos_disponibles -= cantidad
        session.save()
        instance = serializer.save(precio_total=session.precio * cantidad)
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_serializer(instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        data = Booking.objects.values('estado').annotate(total=Count('id'))
        return Response({item['estado']: item['total'] for item in data})

    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm(self, request, pk=None):
        booking = self.get_object()
        if booking.estado != 'pendiente':
            return Response({'detail': 'La reserva no puede ser confirmada.'}, status=400)
        booking.estado = 'confirmada'
        booking.save()
        return Response({'status': 'confirmada'})

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.estado == 'cancelada':
            return Response({'detail': 'La reserva ya está cancelada.'}, status=400)
        if booking.estado == 'confirmada':
            session = booking.session
            session.asientos_disponibles += booking.cantidad_asientos
            session.save()
        booking.estado = 'cancelada'
        booking.save()
        return Response({'status': 'cancelada'})

