from django.db import models


class Location(models.Model):
	ip = models.GenericIPAddressField()
	latitude = models.DecimalField(max_digits=9, decimal_places=6)
	longitude = models.DecimalField(max_digits=9, decimal_places=6)
