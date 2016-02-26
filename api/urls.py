
from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from api import views, views_1_1

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.reverse import reverse


# @api_view(('GET',))
# def api_root(request, format=None):
#     return Response({
#         'get_polygons_tree': reverse('get_polygons_tree', request=request, format=format),
#         'get_nearest_polygons': reverse('get_nearest_polygons', request=request, format=format),
#         'check_in_building': reverse('check_in_building', request=request, format=format)
#     })



router = DefaultRouter()

# -----   v1 api
router.register(r'v1/claims', views.ClaimViewSet)
router.register(r'v1/organizations', views.OrganizationViewSet)
router.register(r'v1/claim_types', views.ClaimTypeViewSet)


urlpatterns = [
	# url(r'^v1/$', api_root),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    url(r'^v1/token/', obtain_auth_token, name='api-token'),
    url(r'^v1/get_polygons_tree/(?P<polygon_id>[\w.]{0,256})/$',
        views.get_polygons_tree, name="get_polygons_tree"),
    url(r'^v1/get_nearest_polygons/(?P<layer>\d+)/(?P<distance>.*)/(?P<coord>.*)$',
        views.get_nearest_polygons, name="get_nearest_polygons"),
    url(r'^v1/check_in_building/(?P<layer>\d+)/(?P<coord>.*)$',
        views.check_in_building, name="check_in_building"),
]

# ----    v1.1 api
router.register(r'v1.1/claims', views_1_1.ClaimViewSet, base_name='claims')
router.register(r'v1.1/organizations', views_1_1.OrganizationViewSet, base_name='organizations')
router.register(r'v1.1/claim_types', views_1_1.ClaimTypeViewSet, base_name='claim_types')
router.register(r'v1.1/get_polygons_tree', views_1_1.GetPolygonsTree, base_name='get_polygons_tree')
router.register(r'v1.1/get_nearest_polygons', views_1_1.GetNearestPolygons, base_name='get_nearest_polygons')
router.register(r'v1.1/check_in_polygon', views_1_1.CheckInPolygon, base_name='check_in_polygon')
router.register(r'v1.1/add_organization', views_1_1.AddOrganization, base_name='add_organization')

urlpatterns += router.urls