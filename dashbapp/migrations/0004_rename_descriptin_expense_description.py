# Generated by Django 4.2.4 on 2023-08-19 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashbapp', '0003_alter_expense_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='descriptin',
            new_name='description',
        ),
    ]
