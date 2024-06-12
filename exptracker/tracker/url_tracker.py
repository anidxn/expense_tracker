from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('dash/', views.dashboard),
    path('addactivity/', views.activity_add, name='add-activity'),
    path('getact/', views.getactdata, name='get-act'),
    path('savecategory/', views.save_cat, name='save-cat'),
    path('getcategorylist/', views.get_catlist, name='get-catlist'),
    path('editcategory/<int:cat_id>/', views.edit_cat, name='edit-cat'),
    path('delcategory/<int:cat_id>/', views.del_cat, name='del-cat')
    
]