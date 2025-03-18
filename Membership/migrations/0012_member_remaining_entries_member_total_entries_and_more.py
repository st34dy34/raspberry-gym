# Generated by Django 5.1.3 on 2024-11-26 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Membership', '0011_alter_member_membership_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='remaining_entries',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='member',
            name='total_entries',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='member',
            name='membership_duration',
            field=models.CharField(choices=[('1 měsíc', '1 měsíc'), ('3 měsíce', '3 měsíce'), ('6 měsíců', '6 měsíců'), ('1 rok', '1 rok'), ('10 vstup', '10 vstupů'), ('20 vstup', '20 vstupů')], max_length=20),
        ),
        migrations.AlterField(
            model_name='member',
            name='membership_type',
            field=models.CharField(choices=[('vstupová', 'vstupová'), ('časová', 'časová')], max_length=20),
        ),
    ]
