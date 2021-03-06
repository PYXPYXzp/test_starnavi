# Generated by Django 2.2.1 on 2020-07-13 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0002_auto_20200708_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attsubscription',
            name='device_id',
        ),
        migrations.RemoveField(
            model_name='attsubscription',
            name='phone_model',
        ),
        migrations.RemoveField(
            model_name='attsubscription',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='attsubscription',
            name='user',
        ),
        migrations.RemoveField(
            model_name='sprintsubscription',
            name='device_id',
        ),
        migrations.RemoveField(
            model_name='sprintsubscription',
            name='phone_model',
        ),
        migrations.RemoveField(
            model_name='sprintsubscription',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='sprintsubscription',
            name='user',
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(blank=True, default='', max_length=20)),
                ('phone_number', models.CharField(blank=True, default='', max_length=20)),
                ('phone_model', models.CharField(blank=True, default='', max_length=128)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='attsubscription',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='subscriptions.Device'),
        ),
        migrations.AddField(
            model_name='sprintsubscription',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='subscriptions.Device'),
        ),
    ]
