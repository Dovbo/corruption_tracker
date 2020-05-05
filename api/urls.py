
from django.conf.urls import url, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from api import views, claim, geoinfo

app_name = 'api'


class CustomRouter(DefaultRouter):

    def get_lookup_regex(self, viewset, lookup_prefix=''):
        if getattr(viewset, 'polygon', False):
            if viewset.polygon == 'get_nearest':
                return '(?P<layer>\d+)/(?P<distance>.*)/(?P<coord>.*)'
            elif viewset.polygon in ['check_in', 'fit_bounds']:
                return '(?P<layer>\d+)/(?P<coord>.*)'

        return super(CustomRouter,
                     self).get_lookup_regex(viewset, lookup_prefix)

router = CustomRouter()

router.register(r'sign_up', views.SignUp,
                'sign_up')
router.register(r'claim', claim.ClaimViewSet,
                'claims')
router.register(r'organization', claim.OrganizationViewSet,
                'organizations')
router.register(r'polygon', geoinfo.PolygonViewSet,
                'polygon')
router.register(r'polygon/get_nearest', geoinfo.GetNearestPolygons,
                'get_nearest')
router.register(r'polygon/fit_bounds', geoinfo.FitBoundsPolygons,
                'fit_bounds')
router.register(r'polygon/check_in', geoinfo.CheckInPolygon,
                'check_in')
router.register(r'polygon/get_tree', geoinfo.GetPolygonsTree,
                'get_polygons')
router.register(r'update', views.GetUpdatedViewSet,
                'updated')


urlpatterns = [
    path('', include('oauth2_provider.urls', namespace='oauth2_provider')),
] + router.urls
