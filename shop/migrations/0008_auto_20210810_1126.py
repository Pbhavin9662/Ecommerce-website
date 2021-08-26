# Generated by Django 3.0 on 2021-08-10 05:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_billingaddress_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]