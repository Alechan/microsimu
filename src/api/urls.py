from django.urls import path

from api import views

app_name = "api"

urlpatterns = [
    path('simulations/'                                , views.simulations_list    , name="simulations"),
    path('simulations/<int:pk>/'                       , views.simulations_detail  , name='simulation-detail'),
    path('simulations/<int:simu_pk>/<str:region_name>/', views.region_result_detail, name='regionresult-detail'),
]
