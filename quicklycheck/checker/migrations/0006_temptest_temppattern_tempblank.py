# Generated by Django 5.0 on 2024-01-14 12:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0005_alter_student_options_alter_blank_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=None, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TempPattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField()),
                ('pattern', models.CharField(max_length=500)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patterns', to='checker.temptest')),
            ],
        ),
        migrations.CreateModel(
            name='TempBlank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_blank', models.CharField(blank=True, max_length=2, null=True)),
                ('var', models.IntegerField()),
                ('image', models.ImageField(upload_to='blanks/', verbose_name='Фотография бланка')),
                ('answers', models.CharField(max_length=254)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blanks', to='checker.temptest')),
            ],
        ),
    ]
