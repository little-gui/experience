from django.db import models


class Follower(models.Model):
	follower_id = models.CharField(max_length=50)
	followers = models.IntegerField(default=0)

class RetweetUser(models.Model):
	screen_name = models.CharField(max_length=255)
