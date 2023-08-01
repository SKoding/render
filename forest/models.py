from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Administration(gis_models.Model):
    gid = models.IntegerField(unique=True, primary_key=True)
    name_4 = models.CharField(_('location'),max_length=24)
    geom = gis_models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'administration'
        managed = False
        verbose_name =('Administration')
        verbose_name_plural = ('Administrations') 
    
    def __str__(self):
        """Return string representation."""
        return self.name_4


class TreeLoss(gis_models.Model):
    id = models.IntegerField(primary_key=True)
    geom = gis_models.MultiPolygonField(srid=4326)
    loss_year = models.IntegerField()

    class Meta:
        db_table = 'tree_loss'
        managed = False
        verbose_name =('tree_loss')
        verbose_name_plural = ('tree_loss') 
    
    def __str__(self):
        """Return string representation."""
        return str(self.id)

class chiefs(models.Model):
    name = models.CharField(max_length=24)
    location = models.CharField(max_length=100)
    natId = models.IntegerField(unique=True, primary_key=True, default=23)
    email = models.EmailField(max_length=256, default='emailaddress@email.com')

    class Meta:
        db_table = 'chief'
        verbose_name =('chief')
        verbose_name_plural = ('chiefs')

    def __str__(self):
        """Return string representation."""
        return self.name

class treeSpecies(gis_models.Model):
    gid = models.IntegerField(unique=True, primary_key=True)
    soiltextur = models.CharField(max_length=256)
    elevation = models.CharField(max_length = 256)
    rainfallto = models.CharField(max_length = 100)
    species = models.CharField(max_length = 256)
    geom = gis_models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'treespecies'
        managed = False
        verbose_name =('Species')
        verbose_name_plural = ('Species') 
    
    def __str__(self):
        """Return string representation."""
        return self.species

class treeNursery (gis_models.Model):
    gid = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=24)
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    #email = models.EmailField(max_length=100)
    #phone = models.IntegerField(max_length=10)
    species = models.CharField(max_length=256)
    geom = gis_models.PointField(blank=True, null=True,srid=4326)

    class Meta:
        db_table = 'tree_nursery_data'
        managed = False
        verbose_name =('TreeNursery')
        verbose_name_plural = ('TreeNursery') 
    
    def __str__(self):
        """Return string representation."""
        return self.name