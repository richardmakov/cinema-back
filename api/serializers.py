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
    asientos_ocupados = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = [
            'id', 'movie', 'movie_id', 'fecha', 'hora', 'sala',
            'precio', 'asientos_totales', 'asientos_disponibles', 'asientos_ocupados',
        ]

    def get_asientos_ocupados(self, obj):
        qs = obj.bookings.exclude(estado='cancelada') \
                         .values_list('asientos_seleccionados', flat=True)
        ocupadas = []
        for arr in qs:
            if isinstance(arr, list):
                ocupadas.extend(arr)
        return ocupadas


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id', 'session', 'nombre_cliente', 'email_cliente', 'telefono_cliente',
            'asientos_seleccionados', 'cantidad_asientos', 'precio_total',
            'estado', 'codigo_reserva', 'creado_en'
        ]
        read_only_fields = ['precio_total', 'codigo_reserva', 'creado_en', 'estado']

    def validate(self, attrs):
        session = attrs['session']
        seats = attrs.get('asientos_seleccionados') or []
        cantidad = attrs.get('cantidad_asientos') or 0

        if cantidad != len(seats):
            raise serializers.ValidationError(
                {'cantidad_asientos': 'Debe coincidir con la cantidad de asientos seleccionados.'}
            )

        # Asientos ocupados (no canceladas)
        qs = Booking.objects.filter(session=session) \
                            .exclude(estado='cancelada') \
                            .values_list('asientos_seleccionados', flat=True)
        ocupadas = set()
        for arr in qs:
            if isinstance(arr, list):
                ocupadas.update(arr)

        conflicto = ocupadas.intersection(seats)
        if conflicto:
            raise serializers.ValidationError(
                {'asientos_seleccionados': f'Las butacas ya están ocupadas: {sorted(conflicto)}'}
            )

        if session.asientos_disponibles < cantidad:
            raise serializers.ValidationError('No hay suficientes asientos disponibles.')

        return attrs
