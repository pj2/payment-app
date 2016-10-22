# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 12:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=30)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=30)),
                ('dest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_transfers', to='payments.Account')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_transfers', to='payments.Account')),
            ],
        ),
    ]