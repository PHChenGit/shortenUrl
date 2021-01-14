# Generated by Django 2.0.13 on 2021-01-14 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shortenurl',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Asia/Taipei', null=True, verbose_name='Updated Time')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Asia/Taipei', null=True, verbose_name='Created Time')),
                ('origin_url', models.URLField(max_length=255)),
                ('shorten_url', models.URLField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=8, unique=True)),
            ],
            options={
                'db_table': 'shorten_url',
            },
        ),
        migrations.AlterUniqueTogether(
            name='shortenurl',
            unique_together={('origin_url', 'shorten_url')},
        ),
    ]
