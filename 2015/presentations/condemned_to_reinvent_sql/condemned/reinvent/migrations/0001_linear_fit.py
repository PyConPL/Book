# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from . import RunSQLFile
import os.path

class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        RunSQLFile(__file__)
    ]
