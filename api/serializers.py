from rest_framework import serializers

from .models import Movie, Session, Booking


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source='movie', write_only=True
    )

    class Meta:
        model = Session
        fields = [
            'id', 'movie', 'movie_id', 'fecha', 'hora', 'sala',
            'precio', 'asientos_totales', 'asientos_disponibles'
        ]


class BookingSerializer(serializers.ModelSerializer):
    session = SessionSerializer(read_only=True)
    session_id = serializers.PrimaryKeyRelatedField(
        queryset=Session.objects.all(), source='session', write_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'session', 'session_id', 'nombre_cliente', 'email_cliente',
            'telefono_cliente', 'asientos_seleccionados', 'cantidad_asientos',
            'precio_total', 'estado', 'codigo_reserva', 'creado_en'
        ]
        read_only_fields = ['precio_total', 'estado', 'codigo_reserva', 'creado_en']

