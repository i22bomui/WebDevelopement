# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entregas', '0003_auto_20170127_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='ruta',
            name='nombre',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
