from django.urls import path,include
from . import views
#import for routers
from rest_framework import routers


#add a router
rt=routers.DefaultRouter()
#register the viewset with this router

rt.register(r'category',views.CatViewSet)
rt.register(r'activity',views.ActViewSet)

urlpatterns=[
    path('',include(rt.urls)),

    # ------------- Search the tasks by date range -----------------
    path('activityfilter/', views.ActivityAPIView.as_view(), name='activity-filter'),
    #path('expbycat/', views.catwise_exp, name='exp-by-cat'),
    path('categoryexpfilter/', views.CategoryExpenseAPIView.as_view(), name='exp-by-cat'),
    path('actexpfilter/', views.ActivityExpenseAPIView.as_view(), name='exp-by-act'),
    
    
]