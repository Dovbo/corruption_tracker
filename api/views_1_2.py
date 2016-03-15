import json

from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.contrib.gis.geos import fromstr
from rest_framework import viewsets, filters
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from geoinfo.models import Polygon
from claim.models import Claim, Organization,\
    ClaimType
from api.serializers import ClaimSerializer,\
    OrganizationSerializer, extractor


class IsSafe(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True


class CanPost(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS + ('POST',):
            return True

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS + ('POST',):
            return True




class ClaimViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing and creating Claims.

    - to get claims for organization, use .../claims/_org_id_
    Example:  .../claims/13/

    - to add claim use POST request with next parameters:
        'text', 'live', 'organization', 'servant', 'claim_type',
    Example:
        'text': 'Покусали комарі', 
        'claim_type': '2', 
        'servant': 'Бабця', 
        'live': 'true', 
        'organization': '13'
    .
    """

    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = (CanPost,)

    filter_backends = (
        filters.OrderingFilter,
    )
    ordering_fields = ('created', )

    def list(self, request):
        docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x }
        return Response(docs)

    def retrieve(self, request, pk=None):
        queryset = Claim.objects.filter(organization__id=pk)   
        serializer = ClaimSerializer(queryset, many=True)
        return Response(serializer.data)      

    def perform_create(self, serializer):
        # print(self.request.data)
        user = None if self.request.user.is_anonymous() else self.request.user
        serializer.save(complainer=user)



class OrganizationViewSet(viewsets.ViewSet):
    """
    API endpoint for listing and creating Organizations.

    - to get organizations for polygon, use .../organizations/_polygon_id_    
    Example:  .../organizations/21citzhovt0002/

    - to add organization use POST with next parameters:
    Example:
        'shape': '{'type': 'Polygon', 'coordinates': [ [ [ 36.296753463843954, 50.006170131432199 ], [ 36.296990304344928, 50.006113443092367 ], [ 36.296866409713009, 50.005899627208827 ], [ 36.296629569212049, 50.00595631580083 ], [ 36.296753463843954, 50.006170131432199 ] ] ]}', 
        'org_type': 'prosecutors',
        'layer_id': '21citzhovt',
        'address': 'Shevshenko street, 3',
        'org_name': 'Ministry of defence',
        'centroid': '36.2968099,50.0060348'

    .
    """

    queryset = Organization.objects.all()
    permission_classes = (CanPost,)


    def list(self, request):
        docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x }
        return Response(docs)

    def retrieve(self, request, pk=None):
        queryset = Organization.objects.filter(polygon__polygon_id=pk)   
        serializer = OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # print(request.data)

        layer = Polygon.objects.get(
            polygon_id=request.data['layer_id'])

        polygon = Polygon(
            polygon_id=request.data['centroid'],
            centroid=fromstr("POINT(%s %s)" % tuple(request.data['centroid'].split(','))),
            shape=request.data['shape'],
            address=request.data['address'],
            layer=layer,
            level=Polygon.building,
            zoom=17,
            is_verified=True)
        polygon.save()

        org_type = OrganizationType.objects.get(
            type_id=request.data['org_type'])

        organization = Organization(
            name=request.data['org_name'],
            org_type=org_type)
        organization.save()

        polygon.organizations.add(organization)



class PolygonViewSet(viewsets.ViewSet):
    """
    API endpoint for obtainin poligons.  
    - GET returns all polygons ordered by creation date
    - to get polygons, filtered by layer use .../polygon/_layer_/
    Available layers:
        region = 1
        area = 2
        district = 3
        building = 4
    
    Example:  .../polygon/3/
    .
    """

    queryset = Polygon.objects.all().order_by('created')
    permission_classes = (IsSafe,)

    def list(self, request):
        data = [x.polygon_to_json() for x in self.queryset]
        return Response(data)

    def retrieve(self, request, pk=4):
        selected = self.queryset.filter(level=int(pk))
        data = [x.polygon_to_json() for x in selected]
        return Response(data)



class GetPolygonsTree(viewsets.ViewSet):
    """
    API endpoint for getting polygons ierarchy.
    - GET returns hole tree from 'root' polygon
    - to get tree from certain node, use .../polygon/get_tree/_polygon_id_
    
    Example:  .../polygon/get_tree/21citdzerz/
    .
    """

    queryset = Polygon.objects.all()
    permission_classes = (IsSafe,)


    def list(self, request):
        return Response(extractor('root'))

    def retrieve(self, request, pk='root'):
        return Response(extractor(pk))



class GetNearestPolygons(viewsets.ViewSet):
    """
    API endpoint for getting nearest polygons.  
    - to get nearest polygons, use .../polygon/get_nearest/_layer_/_distance_/_coordinates_
    Available layers:
        region = 1
        area = 2
        district = 3
        building = 4
    
    Example:  .../polygon/get_nearest/4/0.05/36.226147,49.986106/
    .
    """

    queryset = Polygon.objects.all()
    permission_classes = (IsSafe,)
    polygon = 'get_nearest'


    def list(self, request):
        docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x }
        return Response(docs)

    def retrieve(self, request, layer, distance, coord):
        pnt = fromstr("POINT(%s %s)" % tuple(coord.split(',')))
        selected = Polygon.objects.filter(
            centroid__dwithin=(pnt, float(distance)), level=int(layer))

        data = [x.polygon_to_json() for x in selected]
        return Response(data)



class CheckInPolygon(viewsets.ViewSet):
    """
    API endpoint for check if coordinates in polygon.  
    - to check in polygon, use  .../polygon/check_in/_layer_/_coordinates_  
    Available layers:
        region = 1
        area = 2
        district = 3
        building = 4    

    Example:  .../polygon/check_in/4/36.2218621,49.9876059/
    .
    """

    queryset = Polygon.objects.all()
    permission_classes = (IsSafe,)
    polygon = 'check_in'


    def list(self, request):
        docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x }
        return Response(docs)

    def retrieve(self, request, layer, coord):   
        pnt = fromstr("POINT(%s %s)" % tuple(coord.split(',')))
        selected = Polygon.objects.filter(shape__contains=pnt, level=int(layer))

        data = [x.polygon_to_json() for x in selected]
        return Response(data)





# class PolygonViewSet2(viewsets.ViewSet):

#     """
#     API endpoint for getting polygons ierarchy.
#     - GET returns hole tree from 'root' polygon
#     - to get tree from certain node, use .../get_polygons_tree/_polygon_id_
    
#     Example:  .../get_polygons_tree/21citdzerz/
#     .
#     """
#     polygon = True
#     queryset = Polygon.objects.all()
#     permission_classes = (IsSafe,)


#     def list(self, request):
#         docs = {ind:x for ind, x in enumerate(self.__doc__.split('\n')) if x }
#         return Response(docs)

#     @detail_route()
#     def get_tree(self, request, *args, **kwargs):
#         self.lookup_field = 'get_tree'
#         snippet = self.get_object()        
#         return Response(snippet)   

#     @detail_route()
#     def get_nearest(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet)             

#     @detail_route()
#     def check_in(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet)  
