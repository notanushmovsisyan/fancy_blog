from django.db import models
from django.utils import timezone

from accounts.models import CustomUser


class Post(models.Model):
    first_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    last_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='media/', blank=True, null=True)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=100)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'title', 'date']

    def __str__(self):
        return self.title


