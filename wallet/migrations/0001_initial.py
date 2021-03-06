# Generated by Django 3.0.6 on 2021-04-12 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('mobile', models.BigIntegerField(null=True, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('password', models.CharField(blank=True, max_length=256)),
                ('name', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'wallet',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=20)),
                ('transaction_type', models.CharField(max_length=15)),
                ('balance', models.BigIntegerField(default=0)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
