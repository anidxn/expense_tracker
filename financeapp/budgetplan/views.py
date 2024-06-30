from rest_framework import viewsets
from rest_framework.response import Response
from . models import Category, Activity
from .serializers import CatSerializer, ActivitySerializer, ActivityCategoryLinkSerializer, CategoryExpenditureSerializer

#for custom apis
from rest_framework.decorators import action

# for filteration
from rest_framework import generics, filters

# for category wise total expense
from django.db.models import Sum, F
# for last 6 month aggregate total expenditure
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta

# ---------- for token authentication ----------
# from rest_framework.authentication import TokenAuthentication #==> NOT required if DEFAULT Authentication class is SET GLOBALLY in Settings.py
from rest_framework.permissions import IsAuthenticated


from django.http import JsonResponse

#   ***************************************************************************************
#   we create a viewset class by extending viewsets.ModelViewSet which provides 
#   default create(),retrieve(),list(),update(),partialupdate(),destroy() actions
#   ***************************************************************************************
class CatViewSet(viewsets.ModelViewSet):
    # * * * * * RESTRICT USE of this View class in absence of AUTH TOKEN * * * * *
    # authentication_classes = [TokenAuthentication]  ==> Required ONLY if DEFAULT Authentication class is NOT SET GLOBALLY in Settings.py
    permission_classes = [IsAuthenticated]

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
    # * * * * * RESTRICT USE of this View class in absence of AUTH TOKEN * * * * *
    # authentication_classes = [TokenAuthentication]  ==> Required ONLY if DEFAULT Authentication class is NOT SET GLOBALLY in Settings.py
    permission_classes = [IsAuthenticated]

    queryset=Activity.objects.all()
    # serializer_class=ActSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ActivityCategoryLinkSerializer
        return ActivitySerializer



#   ***************************************************************************************
#   create a view class by extending viewsets.ListAPIView which is specialized view that 
#   only provides read-only access to a list of objects. It supports GET requests to list a queryset.
#   ***************************************************************************************

#   Purpose: SEARCH by direct filtering
#-------------------------------------------------------------
class ActivityAPIView(generics.ListAPIView):
    serializer_class = ActivityCategoryLinkSerializer
    
    # Override the get_queryset()
    def get_queryset(self):
        queryset = Activity.objects.all()  # get all activities from DB

        # check for appropriate query parameters
        # for report
        start_date  = self.request.query_params.get('start_date', None)
        end_date    = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            queryset = queryset.filter(a_date__range=[start_date, end_date])

        # return the final result after filter
        return queryset
        
    
    """
    GET
    http://localhost:8085/finapi/activityfilter/?start_date=2023-01-01&end_date=2023-12-31
    """

#--------------------------------------------------------------------------------------------------
#     AGGREGATE category wise total expense & FILTER out by Tags / min budget / max budget
#-----------------------------------------------------------------------------------------------------

class CategoryExpenseAPIView(generics.ListAPIView):
    # queryset = Category.objects.annotate(total_expenditure=Sum('activity__expense'))  # total_expenditure is the custom field name
    serializer_class = CategoryExpenditureSerializer

    # Override the get_queryset()
    def get_queryset(self):
            # Get Category wise total_expense
            queryset = Category.objects.annotate(total_expenditure=Sum('activity__expense', default=0)) # total_expenditure is the custom field name
            
            # Get query parameters 
            cat_tag = self.request.query_params.get('cat_tag', None)
            min_budget = self.request.query_params.get('min_budget', None)
            max_budget = self.request.query_params.get('max_budget', None)

            # Filter queryset based on query parameters
            if cat_tag:
                queryset = queryset.filter(cat_tags=cat_tag)
            if min_budget:
                queryset = queryset.filter(budget__gte=min_budget)
            if max_budget:
                queryset = queryset.filter(budget__lte=max_budget)


            # return the final result after filter
            return queryset

    """
        http://localhost:8085/finapi/categoryexpfilter/
        http://localhost:8085/finapi/categoryexpfilter/?cat_tag=Want
        http://localhost:8085/finapi/categoryexpfilter/?min_budget=1000
        http://localhost:8085/finapi/categoryexpfilter/?max_budget=5000
        http://localhost:8085/finapi/categoryexpfilter/?cat_tag=Need&min_budget=1000&max_budget=5000
    """
    
#*********************************************************************************
# Filtering + Output JSON data formating
#*********************************************************************************
"""
    return month-wise total expenditure group by cat_tag and for the last 6 months.
"""
class ActivityExpenseAPIView(generics.ListAPIView):
    serializer_class = CategoryExpenditureSerializer

    def get_queryset(self):

        # Get query parameters 
        grouping    = self.request.query_params.get('grpby', None)  # either cat_tags or cat_name
        num_months  = self.request.query_params.get('num_months', None)

        if num_months:
            num_months = int(num_months)
        else:
            num_months = 6
            
        # Calculate the date for Num (6) months ago
        num_months_ago = datetime.today() - timedelta(days = num_months * 30)   # 6 * 30

        # Filter ACTIVITIES in the last Num (6) months
        queryset = Activity.objects.filter(a_date__gte=num_months_ago)

        # Annotate month and group by month and cat_tag & get total_expense
        queryset = queryset.annotate(
                month=TruncMonth('a_date')
            ).values(
                'month', 'a_cat__' + grouping       # 'a_cat__cat_tags' or 'a_cat__cat_name'
            ).annotate(
                total_expenditure=Sum('expense')
            ).order_by('month', 'a_cat__' + grouping)

        
        # return the final result after filter
        return queryset
    
    # --------- overriding the list() to output our specific format ------------
    def list(self, request, *args, **kwargs):
        grouping    = request.query_params.get('grpby', None)
        
        queryset = self.get_queryset()
        #print(queryset)

        if grouping == 'cat_tags':
            # Get all unique cat_tags
            all_tags = dict(Category.C_TAGS).keys()  # temporarily convert it to a dictionary
        else:
            # Get all unique category names by scrolling through the table records *******************
            all_categories = Category.objects.values_list('cat_name', flat=True)

        # Process the data to group by month and cat_tag
        # result = {}
        result = []
        month_data = {}
        for expenditure in queryset:
            # extract month data from date
            month  = expenditure['month'].strftime('%Y-%m')
            month_name = expenditure['month'].strftime('%B')

            if grouping == 'cat_tags':
                cat_tag = expenditure['a_cat__cat_tags']  # list of tags
            else:
                cat_name = expenditure['a_cat__cat_name']

            if month not in month_data:
                month_data[month] = {tag: 0 for tag in all_tags} if grouping == 'cat_tags' else {cat: 0 for cat in all_categories}

                month_data[month]['month_name'] = month_name
            
            if grouping == 'cat_tags':
                month_data[month][cat_tag] += expenditure['total_expenditure']
            else:
                month_data[month][cat_name] += expenditure['total_expenditure']

        # Convert month_data to the required format
        for month_str, data in month_data.items():
            month_name = data.pop('month_name')
            result.append({
                'month': month_str,
                'month_name': month_name,
                'expenditures': data
            })

            # if month not in result:
            #     # ------ result[month] = {}
            #     result[month] = {tag: 0 for tag in all_tags}
            # if cat_tag not in result[month]:
            #     result[month][cat_tag] = 0
            # result[month][cat_tag] += expenditure['total_expenditure']

        return Response(result)
    
"""
    http://localhost:8085/finapi/actexpfilter/?grpby=cat_tags
    http://localhost:8085/finapi/actexpfilter/?grpby=cat_tags&num_months=6
    http://localhost:8085/finapi/actexpfilter/?grpby=cat_name
    http://localhost:8085/finapi/actexpfilter/?grpby=cat_name&num_months=6
"""
"""
ORIGINAL
--------------------
def get_queryset(self):
        # Calculate the date for 6 months ago
        six_months_ago = datetime.today() - timedelta(days=6*30)

        # Filter activities in the last 6 months
        queryset = Activity.objects.filter(a_date__gte=six_months_ago)

        # Annotate month and group by month and cat_id
        queryset = queryset.annotate(
            month=TruncMonth('a_date')
        ).values(
            'month', 'a_cat__cat_name'
        ).annotate(
            total_expenditure=Sum('expense')
        ).order_by('month', 'a_cat__cat_name')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Get all unique category names
        all_categories = Category.objects.values_list('cat_name', flat=True)

        # Process the data to group by month and category
        result = []
        month_data = {}
        for expenditure in queryset:
            month_str = expenditure['month'].strftime('%Y-%m')
            month_name = expenditure['month'].strftime('%B')
            cat_name = expenditure['a_cat__cat_name']
            if month_str not in month_data:
                month_data[month_str] = {cat: 0 for cat in all_categories}
                month_data[month_str]['month_name'] = month_name
            month_data[month_str][cat_name] += expenditure['total_expenditure']

        # Convert month_data to the required format
        for month_str, data in month_data.items():
            month_name = data.pop('month_name')
            result.append({
                'month': month_str,
                'month_name': month_name,
                'expenditures': data
            })

        return Response(result)
"""



# # -------------------------------------------------------------------
# #       Dashboard Data
# # -------------------------------------------------------------------
# from rest_framework.decorators import api_view
# from rest_framework import status


# @api_view(['GET'])
# def catwise_exp(request):
#     categories = Category.objects.annotate(total_expenditure=Sum('activity__expense'))
#     # serializer = Cat(task_list, many = True)  # many = True --> bcz of many record objects are populated

#     return Response(
#         {
#             "message": "Record fetched",
#             "Data" : categories
#         },
#         status = status.HTTP_200_OK
#         )

