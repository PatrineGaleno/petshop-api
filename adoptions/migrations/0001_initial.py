# Generated by Django 5.1.6 on 2025-02-22 13:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('race', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('weight', models.DecimalField(decimal_places=2, max_digits=11)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('A', 'Available'), ('C', 'Chosen')], default='A', max_length=1)),
            ],
            options={
                'verbose_name': 'Pet',
                'verbose_name_plural': 'Pets',
                'db_table': 'pets',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Species',
                'verbose_name_plural': 'Species',
                'db_table': 'species',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Adoption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solicitation_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Refused')], default='P', max_length=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='adoptions.pet')),
            ],
            options={
                'verbose_name': 'Adoption',
                'verbose_name_plural': 'Adoptions',
                'db_table': 'adoptions',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='pet',
            name='species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='adoptions.species'),
        ),
    ]
