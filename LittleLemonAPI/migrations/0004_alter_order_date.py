# Generated by Django 4.2.6 on 2023-10-15 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0003_alter_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(db_index=True, null=True),
        ),
    ]
