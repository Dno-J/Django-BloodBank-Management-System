# Generated by Django 5.2.3 on 2025-07-03 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0006_delete_bloodreceived_alter_donor_donated_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donor',
            name='donated_date',
        ),
    ]
