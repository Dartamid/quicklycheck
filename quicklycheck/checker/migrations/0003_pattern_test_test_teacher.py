# Generated by Django 4.2.1 on 2023-05-29 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('checker', '0002_student_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='pattern',
            name='test',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='patterns', to='checker.test'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='test',
            name='teacher',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='tests', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
