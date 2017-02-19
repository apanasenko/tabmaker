from django.db import models


class Motion(models.Model):
    motion = models.TextField()
    infoslide = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return '%d: (%d) %s' % (self.id, self.is_public, self.motion)

