# Generated by Django 2.0 on 2017-12-09 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deputado',
            fields=[
                ('id_site', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=50)),
                ('partido', models.CharField(max_length=50)),
                ('sigla', models.CharField(max_length=20)),
                ('biografia', models.TextField()),
            ],
        ),
    ]
