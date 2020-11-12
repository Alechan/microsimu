from django.urls import path
from django.views.generic import RedirectView

from api import views

app_name = "api"

simulate_endpoints = views.SimulateViewSet.as_view({
    'get': 'retrieve',
    'post': 'create'
})

urlpatterns = [
    path(''                                                     , views.ApiRoot.as_view()            , name="api_root"),
    path('simulate/'                                            , simulate_endpoints                 , name="simulate"),
    path('simulations/'                                         , views.SimulationList.as_view()     , name="simulations"),
    path('simulations/<int:pk>/'                                , views.SimulationDetail.as_view()   , name='simulation-detail'),
    path('simulations/<int:simu_pk>/<str:region_name>/'         , views.RegionResultDetail.as_view() , name='regionresult-detail'),
    path('simulations/<int:simu_pk>/<str:region_name>/visualize', views.VisualizeView.as_view()      , name='visualize'),
]

