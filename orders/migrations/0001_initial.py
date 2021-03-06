# Generated by Django 2.0.3 on 2020-05-21 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('num_of_orders', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomisedPizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill', models.DecimalField(decimal_places=2, max_digits=6)),
                ('order_time', models.TimeField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=64)),
                ('topping_num', models.IntegerField()),
                ('size', models.CharField(max_length=2)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topping', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='customisedpizza',
            name='pizza_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Pizza'),
        ),
        migrations.AddField(
            model_name='customisedpizza',
            name='toppings',
            field=models.ManyToManyField(blank=True, to='orders.Topping'),
        ),
    ]
