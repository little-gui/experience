from geopy.geocoders import GoogleV3
from django.contrib.auth.models import User
from django.contrib.gis import geos
from django.contrib.gis.db import models as gis_models
from django.db import models


class Article(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=300)
    by_when = models.DateTimeField()
    points = models.IntegerField(default=0)

    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    location = gis_models.PointField(u"longitude/latitude", geography=True, blank=True, null=True)

    gis = gis_models.GeoManager()
    objects = models.Manager()

    # def save(self, **kwargs):
    #     if not self.location:
    #         address = u'%s %s' % (self.city, self.address)
    #         address = address.encode('utf-8')
    #         geocoder = GoogleV3()
    #         try:
    #             _, latlon = geocoder.geocode(address)
    #         except (URLError, GQueryError, ValueError):
    #             pass
    #         else:
    #             point = "POINT(%s %s)" % (latlon[1], latlon[0])
    #             self.location = geos.fromstr(point)
    #     super(Shop, self).save()


class Profile(models.Model):
    user = models.OneToOneField(User)
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=300)
