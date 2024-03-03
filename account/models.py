from django.db import models
from django.contrib.auth.models import User


class Relations(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.from_user} is following {self.to_user}'