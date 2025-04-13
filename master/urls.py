from django.urls import path
from . import views


urlpatterns = [
    path('',views.SignIn, name="signin"),

    path('dashboard/',views.dashboard_view, name="dashboard"),
    path('dashboard/api/',views.dashboardAPI, name="dashboardAPI"),
    path('client/add/api/',views.ClientAddAPI, name="add_client_api"),
    path('logout/', views.logout_view, name='logout'),


]


# abcd
