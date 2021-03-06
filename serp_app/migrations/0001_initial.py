# Generated by Django 3.2.3 on 2021-06-02 15:02

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('search_result_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('query', models.CharField(max_length=200)),
                ('results_total', models.BigIntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('client_ip', models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name='PopularWord',
            fields=[
                ('word_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('word', models.CharField(max_length=100)),
                ('occurances', models.IntegerField()),
                ('search_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serp_app.searchresult')),
            ],
        ),
        migrations.CreateModel(
            name='Link_with_position',
            fields=[
                ('link_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('link', models.CharField(max_length=1000)),
                ('position', models.IntegerField()),
                ('search_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serp_app.searchresult')),
            ],
        ),
    ]
