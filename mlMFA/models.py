from django.db import models
from django.contrib.auth.models import User

class Finger(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE, related_name='msMFA_user')
    image = models.ImageField(upload_to='fingerprints/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.uploaded_at}'

