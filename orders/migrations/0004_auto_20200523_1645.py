# Generated by Django 2.1.5 on 2020-05-23 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20200523_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customisedpizza',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pizzas', to='orders.Order'),
        ),
    ]
