# Generated by Django 2.2.4 on 2019-08-20 18:25

from django.db import migrations, models
import django.db.models.deletion
import files.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HiddenMixIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(default=uuid.uuid1, max_length=64, unique=True)),
                ('expires_at', models.DateTimeField(default=files.models.tomorrow)),
                ('click_count', models.IntegerField(default=0)),
                ('password', models.CharField(max_length=120)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FileHolder',
            fields=[
                ('hiddenmixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='files.HiddenMixIn')),
                ('file', models.FileField(upload_to='')),
            ],
            options={
                'abstract': False,
            },
            bases=('files.hiddenmixin',),
        ),
        migrations.CreateModel(
            name='UrlHolder',
            fields=[
                ('hiddenmixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='files.HiddenMixIn')),
                ('url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
            bases=('files.hiddenmixin',),
        ),
    ]