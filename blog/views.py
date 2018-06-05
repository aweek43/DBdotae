from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse
from .models import *
import pyodbc
conn = pyodbc.connect("DSN=TIBERO;UID=DBDOTAE;PWD=tibero")
cursor = conn.cursor()


logined_user = User()
logined_user.username = "ana"

def post_list(request):
    return render(request, 'blog/post_list.html', {'logined_user':logined_user})

#def login(request):
	#return render(request, 'blog/login.html', {})
 
def login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		logined_user.user_id = int(request.POST.get('user_id'))
		cursor.execute("SELECT USER_ID, USER_NAME, SEX, LOCATION_ID FROM USERTABLE WHERE USER_ID = ?", logined_user.user_id)
		rows = cursor.fetchone()
		if  rows == None:
			return HttpResponse('fail')
		else :
			logined_user.username = rows.USER_NAME
			logined_user.sex = rows.SEX
			logined_user.location_id = rows.LOCATION_ID
			print(logined_user.user_id, logined_user.username, logined_user.sex, logined_user.location_id)
			return redirect('post_list')
	return render(request, 'blog/login.html', {})

def logout(request):
	logined_user.username = "ana"
	return redirect('post_list')


def cafelist_cafe(request):
	if request.method == "POST":
		resultcafe = []
		key = request.POST['_search']
		cursor.execute("select * from cafe where cafe_name like ?", '%'+key+'%')
		rows = cursor.fetchall()
		for i in range (len(rows)):
			temp = []
			temp.append(rows[i].CAFE_NAME)
			temp.append(rows[i].CAFE_ADDRESS)
			resultcafe.append(temp)

	return render(request, 'blog/cafelist_cafe.html', {'resultcafe':resultcafe})


def cafelist_location(request):
	return render(request, 'blog/cafelist_location.html', {})