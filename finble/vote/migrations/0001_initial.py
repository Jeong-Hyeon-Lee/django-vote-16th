# Generated by Django 3.0.8 on 2022-12-04 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('vote_num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('part', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=10)),
                ('part_voted', models.BooleanField(default=False)),
                ('demo_voted', models.BooleanField(default=False)),
                ('vote_num', models.IntegerField(default=0)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote.Team')),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
