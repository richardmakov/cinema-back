from django.db import models
from django.utils import timezone
import uuid


class Movie(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    duracion = models.PositiveIntegerField(help_text="Duración en minutos")
    genero = models.CharField(max_length=100)
    clasificacion = models.CharField(max_length=50)
    poster_url = models.URLField(blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class Session(models.Model):
    movie = models.ForeignKey(Movie, related_name='sessions', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    sala = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    asientos_totales = models.PositiveIntegerField()
    asientos_disponibles = models.PositiveIntegerField()

    class Meta:
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"{self.movie.titulo} - {self.fecha} {self.hora}"


class Booking(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    session = models.ForeignKey(Session, related_name='bookings', on_delete=models.CASCADE)
    nombre_cliente = models.CharField(max_length=255)
    email_cliente = models.EmailField()
    telefono_cliente = models.CharField(max_length=20, blank=True)
    asientos_seleccionados = models.JSONField()
    cantidad_asientos = models.PositiveIntegerField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    codigo_reserva = models.CharField(max_length=36, unique=True, editable=False, default=uuid.uuid4)
    creado_en = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre_cliente} - {self.codigo_reserva}"

