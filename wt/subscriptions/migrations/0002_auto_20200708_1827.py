# Generated by Django 2.2.1 on 2020-07-08 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attsubscription',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('active', 'Active'), ('expired', 'Expired')], default='new', max_length=10),
        ),
        migrations.AlterField(
            model_name='sprintsubscription',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('active', 'Active'), ('suspended', 'Suspended'), ('expired', 'Expired')], default='new', max_length=10),
        ),
    ]