# Generated by Django 3.1.4 on 2021-01-01 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0013_auto_20210101_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default=1, upload_to='images/'),
            preserve_default=False,
        ),
    ]
