# Generated by Django 4.0.4 on 2022-06-12 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_car_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'ordering': ('available',)},
        ),
        migrations.AddField(
            model_name='car',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(blank=True, default=None, upload_to='store/%Y/%m/%d'),
            preserve_default=False,
        ),
    ]
