# Generated by Django 3.0 on 2021-08-10 02:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210808_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(default='xyz123@gmail.com', max_length=100)),
                ('country', models.CharField(default='INDIA', max_length=7)),
                ('address1', models.CharField(max_length=150, null=True)),
                ('address2', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('state', models.CharField(max_length=50, null=True)),
                ('zipcode', models.CharField(max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
