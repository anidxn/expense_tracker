from rest_framework import viewsets
from rest_framework.response import Response
from . models import Category, Activity
from .serializers import CatSerializer, ActivitySerializer, ActivityCategoryLinkSerializer

#for custom apis
from rest_framework.decorators import action

# for filteration
from rest_framework import generics, filters

#we create a viewset class by extending viewsets.ModelViewSet which provides default create(),retrieve(),list(),update(),partialupdate(),destroy() actions
class CatViewSet(viewsets.ModelViewSet):
    #queryset and serializer_class is an inbuilt data object so don't change the name
    queryset=Category.objects.all()
    serializer_class=CatSerializer


    # For URL like ../category/{cat_id}/activity
    @action(detail=True, methods=['get'])
    def activity(self, request, pk = None):

        #-- get the category base on the id (here it is pkey)..Qs. wht if the search criteria is not pkey??
        cat = Category.objects.get(cat_id = pk)

        # == get the list of employees corresponding to that company object
        actlist = Activity.objects.filter(a_cat = cat) # object matching; not just any particular field

        # serialize the list to be displayed
        act_serializer = ActivityCategoryLinkSerializer(actlist, many=True, context = {'request': request})
        """
        many = True --> lots of data 
        """

        return Response(act_serializer.data) # send API response in JSON format

#------------------------------------------------------------------------------------
#   Switch between 2 available serializers to deal with Foregn Key Linked Model Data
#   - During GET operation we need the nested object details, but for other operations we don't need that
#-------------------------------------------------------------------------------------
class ActViewSet(viewsets.ModelViewSet):
    queryset=Activity.objects.all()
    # serializer_class=ActSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityCategoryLinkSerializer
        return ActivitySerializer


#-------------------------------------------------------------
#               SEARCH by Date Range
#-------------------------------------------------------------
class ActivityAPIView(generics.ListAPIView):
    serializer_class = ActivityCategoryLinkSerializer
    
    def get_queryset(self):
        queryset = Activity.objects.all()
        start_date  = self.request.query_params.get('start_date', None)
        end_date    = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            queryset = queryset.filter(a_date__range=[start_date, end_date])
        return queryset
    
    """
    http://localhost:8085/finapi/actbydate/?start_date=2023-01-01&end_date=2023-12-31
    """
