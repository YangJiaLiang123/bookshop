# Generated by Django 3.2 on 2022-03-21 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_shopcar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myorder',
            name='product',
        ),
    ]
