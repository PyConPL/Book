from django.db import models
from django.conf import settings

class Grade(models.Model):
    RANGE = (2,5)

    student = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(auto_now=True, null=False)
    grade = models.IntegerField(null=False)

    def save(self, *args, **kwargs):
        from django.core.exceptions import ValidationError

        if not (Grade.RANGE[0] <= self.grade <= Grade.RANGE[1]):
            raise ValidationError("Invalid grade: {} is not in range [{},{}]".format(self.grade, *Grade.RANGE))

        super(Grade, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{} for {} on {}'.format(self.grade, self.student.username, self.date)
