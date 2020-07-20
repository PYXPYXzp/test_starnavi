# Generated by Django 2.2.1 on 2020-07-20 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_auto_20200713_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attsubscription',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='subscriptions.Device'),
        ),
        migrations.AlterField(
            model_name='attsubscription',
            name='effective_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attsubscription',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='plans.Plan'),
        ),
        migrations.AlterField(
            model_name='sprintsubscription',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='subscriptions.Device'),
        ),
        migrations.AlterField(
            model_name='sprintsubscription',
            name='effective_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sprintsubscription',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='plans.Plan'),
        ),
        migrations.AlterField(
            model_name='sprintsubscription',
            name='sprint_id',
            field=models.CharField(blank=True, default='', max_length=16),
            preserve_default=False,
        ),
    ]
