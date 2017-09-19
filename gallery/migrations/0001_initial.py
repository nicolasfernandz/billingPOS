# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-19 23:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Linea_Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=15)),
                ('nombre', models.CharField(max_length=250)),
                ('observaciones', models.CharField(max_length=250)),
                ('foto', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=15)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('Observaciones', models.CharField(max_length=250)),
                ('cantidad_unidades', models.IntegerField(null=True)),
                ('caja', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='linea_venta',
            name='Producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.Producto'),
        ),
        migrations.AddField(
            model_name='linea_venta',
            name='Venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.Venta'),
        ),
    ]
