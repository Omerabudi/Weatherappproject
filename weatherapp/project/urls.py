from django.urls import path
from project import views
#my urls
urlpatterns = [
    path('weather',views.display_weather,name='display'),
    path('create',views.create_user,name='create'),
    path('singleview',views.single_view,name='single'),
    path('favorites',views.show_favorites,name='favorites')
]
