# Generated by Django 3.0.4 on 2020-04-12 18:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20200411_0317'),
    ]

    operations = [
        migrations.AddField(
            model_name='datospersonales',
            name='fecha_nacimiento',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='fecha nacimiento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datospersonales',
            name='genero',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], default='O', max_length=1),
            preserve_default=False,
        ),
    ]
