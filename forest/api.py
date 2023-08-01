from rest_framework import routers
from .views import  adminViewSet, chiefViewSet, speciesViewSet, distView, nursuriesViewSet, treeLossViewSet

## Register Viewsets as APIs 
router = routers.DefaultRouter()
router.register(r"administrative", adminViewSet)
router.register(r"chiefs", chiefViewSet)
router.register(r"species", speciesViewSet)
router.register(r"distance", distView)
router.register(r"nurseries", nursuriesViewSet)
router.register(r"losses", treeLossViewSet)


urlpatterns = router.urls