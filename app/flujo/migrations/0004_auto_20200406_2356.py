# Generated by Django 3.0.4 on 2020-04-06 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20200406_2119'),
        ('flujo', '0003_auto_20200406_2251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flujo',
            name='pregunta_actual',
        ),
        migrations.AddField(
            model_name='flujo',
            name='pregunta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pregunta_de_flujo', to='home.Pregunta'),
            preserve_default=False,
        ),
    ]
