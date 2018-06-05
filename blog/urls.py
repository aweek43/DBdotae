from django.conf.urls import url
from . import views 
 
urlpatterns = [
url(r'^$', views.post_list, name='post_list'),
url(r'^login/$', views.login, name='login'),
url(r'^logout/$', views.logout),
url(r'^cafelist_cafe/$', views.cafelist_cafe, name='cafelist_cafe'),
url(r'^cafelist_location/$', views.cafelist_location, name='cafelist_location'),
] 