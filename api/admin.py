from django.contrib import admin

from .models import Movie, Session, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("titulo", "genero", "clasificacion", "activa")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("movie", "fecha", "hora", "sala", "precio")
    list_filter = ("movie", "fecha")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("codigo_reserva", "nombre_cliente", "session", "estado")
    list_filter = ("estado",)
