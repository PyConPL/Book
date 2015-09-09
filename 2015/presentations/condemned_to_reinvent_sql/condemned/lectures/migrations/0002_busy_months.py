# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from reinvent.migrations import RunSQLFile


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0001_initial'),
    ]

    operations = [
        RunSQLFile(__file__)
    ]
