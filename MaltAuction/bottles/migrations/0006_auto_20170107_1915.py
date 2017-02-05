# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bottles', '0005_auto_20141206_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottle',
            name='comment',
            field=models.TextField(null=True, blank=True),
        ),
    ]
