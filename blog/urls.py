from django.conf.urls import url
from . import views 
 
urlpatterns = [
url(r'^$', views.main, name='main'),
url(r'^search/$', views.search, name='search'),
url(r'^mypage/$', views.mypage, name='mypage'),
url(r'^login/$', views.login, name='login'),
url(r'^logout/$', views.logout),
url(r'^cafelist_cafe/$', views.cafelist_cafe, name='cafelist_cafe'),
url(r'^cafelist_location/$', views.cafelist_location, name='cafelist_location'),
url(r'^addresslist/$', views.addresslist, name='addresslist'),
url(r'^addresschoice/$', views.addresschoice, name='addresschoice'),
] 