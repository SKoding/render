from django.contrib import admin
from django.contrib.gis import admin as gisAdmin
from .models import Administration, treeSpecies,treeNursery,TreeLoss

# Register your models here.
class locationAdmin(gisAdmin.OSMGeoAdmin):
    list_display = ('gid','name_4',)
    search_fields = ('name_4',)
    ordering = ('gid',)

class speciesAdmin(gisAdmin.OSMGeoAdmin):
    list_display = ('gid','soiltextur','elevation','rainfallto','species')
    search_fields = ('species',)
    ordering = ('gid',)

class nurseryAdmin(gisAdmin.OSMGeoAdmin):
    list_display = ('gid','name','first_name','last_name','species')
    search_fields = ('name',)
    ordering = ('gid',)

class lossesAdmin(gisAdmin.OSMGeoAdmin):
    list_display = ('id','loss_year')
    search_fields = ('loss_year',)
    ordering = ('id',)

admin.site.register(Administration,locationAdmin)
admin.site.register(TreeLoss,lossesAdmin)
admin.site.register(treeSpecies,speciesAdmin)
admin.site.register(treeNursery,nurseryAdmin)