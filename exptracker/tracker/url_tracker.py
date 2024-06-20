from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('dash/', views.dashboard, name='dashboard'),
    path('addactivity/', views.activity_add, name='add-activity'),
    path('getact/', views.getactdata, name='get-act'),
    path('editactivity/<int:ac_id>/', views.edit_activity, name='edit-activity'),
    path('deleteactivity/<int:ac_id>/', views.del_activity, name='delete-activity'),

    path('savecategory/', views.save_cat, name='save-cat'),
    path('getactbycat/<int:cat_id>/', views.get_act_by_cat, name='get-act-by-cat'),
    path('getcategorylist/', views.get_catlist, name='get-catlist'),
    path('editcategory/<int:cat_id>/', views.edit_cat, name='edit-cat'),
    path('delcategory/<int:cat_id>/', views.del_cat, name='del-cat'),

    #--------- reports-------------
    
    path('detreport/', views.detailed_report, name='det-rep'),
]