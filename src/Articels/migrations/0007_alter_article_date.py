# Generated by Django 4.1.4 on 2023-01-14 09:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Articels', '0006_alter_article_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 14, 9, 54, 6, 169481, tzinfo=datetime.timezone.utc)),
        ),
    ]