from django.db import models
from users.models import User 
from django.utils import timezone


class Passwords(models.Model):
    acount_name =models.TextField(null=False, blank=False)
    value = models.TextField(null=False, blank=False)
    value_id = models.TextField(null=False, blank=False)
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-id"]
        def __str__(self) -> str:
            return self.value

