from django.contrib import admin
from django.urls import path
from tickets import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', csrf_exempt(views.no_rest_no_model)),
    path('frommolde/', views.no_rest_from_model),
    path('fbv/', views.FBV_List),
    path('fbv-pk/<int:pk>', views.FBV_pk),
    path('cbv/', views.CBV_LIST.as_view()),
    path('cbv/<int:pk>', views.CBV_pk.as_view()),   
]

