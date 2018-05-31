from django.shortcuts import render
from .forms import LoginForm
from .models import *
import pyodbc
conn = pyodbc.connect("DSN=TIBERO;UID=sys;PWD=tibero")
cursor = conn.cursor()


logined_user = User()
 
def post_list(request):
    return render(request, 'blog/post_list.html', {})

def login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		logined_user.user_id = int(request.POST.get('user_id'))
		cursor.execute("SELECT USER_ID, USER_NAME, SEX, LOCATION_ID FROM USERTABLE WHERE USER_ID = ?", logined_user.user_id)
		rows = cursor.fetchone()
		if  rows == None:
			print('no')
			#return Httpresponse('fail')
		else :
			logined_user.username = rows.USER_NAME
			logined_user.sex = rows.SEX
			logined_user.location_id = rows.LOCATION_ID
			print(logined_user.user_id, logined_user.username, logined_user.sex, logined_user.location_id)
			return render(request, 'blog/post_list.html', {'logined_user':logined_user})
	return render(request, 'blog/login.html', {})


def cafelist_cafe(request):
	if request.method == "POST":
		key = request.POST['_search']
		sql = "select * from cafe where cafe_name = %" + key + "%;"
		cursor.execute(sql)
	return render(request, 'blog/cafelist_cafe.html', {})

def cafelist_location(request):
	return render(request, 'blog/cafelist_location.html', {})