# Generated by Django 4.2 on 2023-05-27 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truck_app', '0005_orderbooking_total_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houseshiftingselectedvehicle',
            name='vehicle_image',
            field=models.CharField(blank=True, max_length=1100, null=True),
        ),
        migrations.AlterField(
            model_name='warehouseselectedvehicle',
            name='vehicle_image',
            field=models.CharField(blank=True, max_length=1100, null=True),
        ),
    ]