# Generated by Django 3.1.7 on 2021-10-09 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='0', help_text='Status of order matching or not, 1 or 0', max_length=1),
        ),
    ]