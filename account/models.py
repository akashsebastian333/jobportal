from django.db import models

import random
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

class Notes(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.CharField(max_length=255, blank=True)



    def save(self, *args,  **kwargs):
        self.date = f"{self.date_created.strftime('%B')} {self.date_created.strftime('%D').split('/')[1]} 20{self.date_created.strftime('%D').split('/')[2]}"
        if not self.slug:
            self.slug = self.title+str(random.randint(0,100))
        super(Notes, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-date_created'),


    def __str__(self):
        return f"{self.title}"
