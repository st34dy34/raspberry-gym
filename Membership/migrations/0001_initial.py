# Generated by Django 5.1.3 on 2024-11-23 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('membership_type', models.CharField(max_length=50)),
                ('join_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
