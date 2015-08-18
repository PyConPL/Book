from django.db import migrations
import os.path

class RunSQLFile(migrations.RunSQL):
    def __init__(self, filename):
        directory = os.path.dirname(os.path.realpath(filename))

        basename, _ = os.path.splitext(os.path.basename(filename))

        with open(os.path.join(directory, basename + '.sql')) as sql_file:
            super(RunSQLFile, self).__init__(sql_file.read())

