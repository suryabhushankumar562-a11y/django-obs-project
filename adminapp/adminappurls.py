from django.urls import path
from . import views

urlpatterns = [
    path('admindash/', views.admindash, name='admindash'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('viewenq/', views.viewenq, name='viewenq'),
    path('delenq/<id>/', views.delenq, name='delenq'),
    path('adminchangepwd/', views.adminchangepwd, name='adminchangepwd'),
    
    
     path('viewcat/', views.viewcat,name='viewcat'),
    
    path('addcat/', views.addcat,name='addcat'),
    
    path('addbook/', views.addbook,name='addbook'),
    
    path('viewbook/', views.viewbook,name='viewbook'),
    path('adminorders/',views.adminorders,name='adminorders'),
    
    
    
    
    
    
    
    
    
  #  path('add_category/', views.add_category, name='add_category'),
   # path('view_category/', views.view_category, name='view_category'),
    path('editcat/<int:id>/', views.edit_category, name='edit_category'),
    #path('delete_category/<int:id>/', views.delete_category, name='delete_category'), 
    
]