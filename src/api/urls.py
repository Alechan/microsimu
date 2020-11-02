from django.urls import path
from django.views.generic import RedirectView

from api import views

app_name = "api"

urlpatterns = [
    path(''                                            , RedirectView.as_view(url='simulations/')),
    path('simulations/'                                , views.SimulationList.as_view()     , name="simulations"),
    path('simulations/<int:pk>/'                       , views.SimulationDetail.as_view()   , name='simulation-detail'),
    path('simulations/<int:simu_pk>/<str:region_name>/', views.RegionResultDetail.as_view() , name='regionresult-detail'),
]

