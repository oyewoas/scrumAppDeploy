from django.urls import path,include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'ayooluwaoyewoscrumy'
# Create a router and register our viewsets with it.
router = DefaultRouter()  
router.register('scrumuser', views.ScrumUserViewSet) 
# router.register('user', views.UserViewSet) 
router.register('scrumgoal', views.ScrumGoalViewSet) 


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', views.index, name='index'),
    path(r'api/v1/', include(router.urls)),
    path('scrumygoals/', views.scrumygoals, name='scrumygoals'),
    path('specificscrumygoal/', views.specificgoal, name='specificgoal'),
    path('movegoal/<int:goal_id>/', views.move_goals, name='movegoals'),
    path('addgoal/', views.add_goal, name='addgoal'),
    path('home/', views.home, name='home'),
    path('homepage/', views.homepage, name='homepage'),
    path('accounts/', include('django.contrib.auth.urls'), name='login'),
    url(r'^api-token-auth/', obtain_jwt_token),
   
]
