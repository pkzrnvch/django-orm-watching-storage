from django.db import models
from django.utils.timezone import localtime


def format_duration(duration):
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = (duration % 3600) % 60
    return f'{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}'


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved='leaved at ' + str(self.leaved_at) if self.leaved_at else 'not leaved'
        )

    def get_duration(self):
        if self.leaved_at is None:
            delta = localtime() - localtime(self.entered_at)
        else:
            delta = localtime(self.leaved_at) - localtime(self.entered_at)
        duration = delta.total_seconds()
        return duration

    def is_long(self, minutes=60):
        seconds_limit = minutes * 60
        return self.get_duration() > seconds_limit
