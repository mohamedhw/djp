# Generated by Django 4.1.4 on 2023-01-27 17:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Articels', '0015_rename_save_article_saved_pic_alter_article_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 27, 17, 20, 47, 886830, tzinfo=datetime.timezone.utc)),
        ),
    ]
