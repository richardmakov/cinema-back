import uuid
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('duracion', models.PositiveIntegerField(help_text='Duración en minutos')),
                ('genero', models.CharField(max_length=100)),
                ('clasificacion', models.CharField(max_length=50)),
                ('poster_url', models.URLField(blank=True)),
                ('activa', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('sala', models.CharField(max_length=50)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8)),
                ('asientos_totales', models.PositiveIntegerField()),
                ('asientos_disponibles', models.PositiveIntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='api.movie')),
            ],
            options={'ordering': ['fecha', 'hora']},
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cliente', models.CharField(max_length=255)),
                ('email_cliente', models.EmailField(max_length=254)),
                ('telefono_cliente', models.CharField(blank=True, max_length=20)),
                ('asientos_seleccionados', models.JSONField()),
                ('cantidad_asientos', models.PositiveIntegerField()),
                ('precio_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')], default='pendiente', max_length=20)),
                ('codigo_reserva', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True)),
                ('creado_en', models.DateTimeField(default=django.utils.timezone.now)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='api.session')),
            ],
        ),
    ]

