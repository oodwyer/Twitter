# Generated by Django 2.2.7 on 2019-11-26 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_hashtag'),
    ]

    operations = [
        migrations.AddField(
            model_name='hashtag',
            name='tweets',
            field=models.ManyToManyField(to='core.Tweet'),
        ),
    ]
