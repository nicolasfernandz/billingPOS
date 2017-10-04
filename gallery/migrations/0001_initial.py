# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 20:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AperturaCaja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_apertura_Caja', models.DateTimeField(auto_now_add=True)),
                ('fecha_cierre_Caja', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Descripcion', models.CharField(max_length=250)),
                ('ubicacion', models.CharField(max_length=250)),
                ('modelo', models.CharField(max_length=250, null=True)),
                ('numero_serie', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImpuestosProductoFecha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField(auto_now_add=True)),
                ('fecha_fin', models.DateTimeField(auto_now_add=True)),
                ('porcentaje_impuesto', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Linea_Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ImpuestosProductoFecha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.ImpuestosProductoFecha')),
            ],
        ),
        migrations.CreateModel(
            name='PreciosProductoFecha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('precio_sin_iva', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('observaciones', models.CharField(max_length=250)),
                ('foto', models.FileField(upload_to='')),
                ('aplica_impuesto', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total_sin_iva', models.DecimalField(decimal_places=2, max_digits=15)),
                ('monto_iva', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total', models.DecimalField(decimal_places=2, max_digits=15)),
                ('AperturaCaja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.AperturaCaja')),
            ],
        ),
        migrations.AddField(
            model_name='preciosproductofecha',
            name='Producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod', to='gallery.Producto'),
        ),
        migrations.AddField(
            model_name='linea_venta',
            name='PreciosProductoFecha',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.PreciosProductoFecha'),
        ),
        migrations.AddField(
            model_name='linea_venta',
            name='Venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.Venta'),
        ),
        migrations.AddField(
            model_name='impuestosproductofecha',
            name='Producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.Producto'),
        ),
        migrations.AddField(
            model_name='aperturacaja',
            name='Caja',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.Caja'),
        ),
    ]
