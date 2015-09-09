
from django.db import models
from django.db.models.expressions import Func
from django.contrib.postgres.fields import ArrayField

class LinearFit(Func):
    contains_aggregate = True
    function = 'linear_fit'
    template = '%(function)s(%(expressions)s order by %(ordering)s)'

    def __init__(self, expression, ordering, **extra):
        super(LinearFit, self).__init__(
            expression,
            output_field=ArrayField(models.FloatField()),
            **extra)
        self.ordering = self._parse_expressions(ordering)[0]

    def resolve_expression(self, *args, **kwargs):
        c = super(Func, self).resolve_expression(*args, **kwargs)
        c.ordering = c.ordering.resolve_expression(*args, **kwargs)
        return c

    def as_sql(self, compiler, connection, function=None, template=None):
        ordering_sql, ordering_params = compiler.compile(self.ordering)
        self.extra['ordering'] = ordering_sql

        return super(LinearFit, self).as_sql(compiler, connection, function, template)

    def get_group_by_cols(self):
        return []
