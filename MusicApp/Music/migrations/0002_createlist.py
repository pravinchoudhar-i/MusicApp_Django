# Generated by Django 5.0.1 on 2024-01-11 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_name', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
