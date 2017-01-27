# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entregas', '0002_ruta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ruta',
            name='nombre',
        ),
        migrations.AddField(
            model_name='paquete',
            name='ruta',
            field=models.ForeignKey(default='1', to='entregas.Ruta'),
            preserve_default=False,
        ),
    ]
