from rest_framework import viewsets
from rest_framework.response import Response
from . models import Category
from .serializers import CatSerializer
from . models import Activity
from .serializers import ActSerializer
#for custom apis
from rest_framework.decorators import action


# Create your views here.
#we create a viewset class by extending viewsets.ModelViewSet which provides default create(),retrieve(),list(),update(),partialupdate(),destroy() actions
class CatViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()#queryset and serializer_class is an inbuilt data object so don't change the name
    serializer_class=CatSerializer


    #companies/{company_id}/employees
    @action(detail=True, methods=['get'])
    def activity(self, request, pk = None):
        #print("get employees of ", pk, "company")


        #-- get the company base on the id (here it is pkey)..Qs. wht if the search criteria is not pkey??
        cat = Category.objects.get(cat_id = pk)
        # == get the list of employees corresponding to that company object
        actlist = Activity.objects.filter(a_cat = cat) # object matching; not just any particular field
        # serialize the list to be displayed
        act_serializer = ActSerializer(actlist, many=True, context = {'request': request})
        """
        many = True --> lots of data 
        """

        return Response(act_serializer.data) # send API response in JSON format


class ActViewSet(viewsets.ModelViewSet):
    queryset=Activity.objects.all()#queryset and serializer_class is an inbuilt data object so don't change the name
    serializer_class=ActSerializer
