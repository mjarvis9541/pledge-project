from django.urls import path

from . import views

app_name = 'pledges'
urlpatterns = [
    path('', views.PledgeListView.as_view(), name='pledge_list'),
    path('<int:pk>/', views.UserPledgeListView.as_view(), name='user_pledge_list'),
]
