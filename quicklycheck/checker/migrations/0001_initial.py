# Generated by Django 4.2.1 on 2023-05-29 03:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=2)),
                ('letter', models.CharField(max_length=2)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField()),
                ('pattern', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='checker.class')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='checker.class')),
            ],
        ),
        migrations.CreateModel(
            name='Blank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_blank', models.CharField(max_length=2)),
                ('var', models.IntegerField()),
                ('image', models.ImageField(upload_to='blanks/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='works', to='checker.student')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blanks', to='checker.test')),
            ],
        ),
    ]
