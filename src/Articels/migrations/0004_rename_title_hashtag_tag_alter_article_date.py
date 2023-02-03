# Generated by Django 4.1.4 on 2023-02-03 13:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Articels', '0003_rename_slug_hashtag_tag_slug_alter_article_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hashtag',
            old_name='title',
            new_name='tag',
        ),
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 3, 13, 42, 39, 853608, tzinfo=datetime.timezone.utc)),
        ),
    ]
