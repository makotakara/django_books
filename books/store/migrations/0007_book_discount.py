# Generated by Django 4.1.7 on 2023-02-27 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_userbookrelation_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, null=0),
            preserve_default=False,
        ),
    ]