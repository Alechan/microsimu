from django.urls import path
from django.views.generic import RedirectView

from api import views

app_name = "api"

urlpatterns = [
    path(''                                            , RedirectView.as_view(url='simulations/')),
    path('simulations/'                                , views.simulations_list    , name="simulations"),
    path('simulations/<int:pk>/'                       , views.simulations_detail  , name='simulation-detail'),
    path('simulations/<int:simu_pk>/<str:region_name>/', views.region_result_detail, name='regionresult-detail'),
]
