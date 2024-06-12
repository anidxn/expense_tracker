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
    path('',include(rt.urls))
]