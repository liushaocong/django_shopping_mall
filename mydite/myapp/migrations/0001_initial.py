# Generated by Django 2.0.1 on 2018-02-01 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('images', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=128)),
                ('price', models.IntegerField()),
                ('num', models.IntegerField()),
                ('price_all', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Commod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('image', models.CharField(max_length=64)),
                ('price', models.IntegerField()),
                ('types', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('times', models.DateTimeField()),
                ('order', models.IntegerField()),
                ('images', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('types', models.BooleanField()),
                ('num', models.IntegerField()),
                ('price', models.IntegerField()),
                ('commod', models.ManyToManyField(to='myapp.Cat')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=24)),
                ('password_hash', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='myapp.User')),
                ('recipient', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=128)),
                ('postcode', models.IntegerField()),
                ('phone', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.User'),
        ),
        migrations.AddField(
            model_name='cat',
            name='commod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Commod'),
        ),
        migrations.AddField(
            model_name='cat',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.User'),
        ),
    ]