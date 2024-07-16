from django.db import models


class User(models.Model):
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class Finger(models.Model):
    username = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    finger_id = models.IntegerField(primary_key=True, auto_created=True)
    finger_data = models.TextField(max_length=255, null=False, blank=False)


class Device(models.Model):
    device_name = models.TextField(max_length=50, unique=True, null=False, blank=False)
    sn = models.TextField(max_length=50, unique=True, null=False, blank=False)
    vc = models.TextField(max_length=50, unique=True, null=False, blank=False)
    ac = models.TextField(max_length=50, unique=True, null=False, blank=False)
    vkey = models.TextField(max_length=50, unique=True, null=False, blank=False)


class Log(models.Model):
    username = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    log_time = models.DateTimeField()
    data = models.TextField()


