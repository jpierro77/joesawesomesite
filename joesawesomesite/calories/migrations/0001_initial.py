# Generated by Django 2.2 on 2019-10-23 00:12

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
            name='UserHealthInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(verbose_name='Current Weight')),
                ('gender', models.CharField(max_length=1, verbose_name='Gender')),
                ('height', models.IntegerField(verbose_name='Height')),
                ('age', models.IntegerField(verbose_name='Age')),
                ('activity_level', models.FloatField(verbose_name='Activity Level')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('limit', models.IntegerField(verbose_name='Daily Limit')),
                ('foods', models.TextField(verbose_name='Food List')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]