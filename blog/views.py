from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse
from .models import *
import datetime
import pyodbc
conn = pyodbc.connect("DSN=TIBERO;UID=DBDOTAE;PWD=tibero")
cursor = conn.cursor()

logined_user = User()
logined_user.username = "null"

cafe = Cafe()
cafe.cafe_id = "null"

location = Location()
location.location_id = 'null'
def main(request):
	return render(request, 'blog/main.html', {'logined_user':logined_user})

def search(request):
	if request.method == "POST":
		cafe.cafe_id = int(request.POST.get('cafeID'))
		cursor.execute("select * from cafe where cafe_id = ?", cafe.cafe_id)
		rows = cursor.fetchone()
		cafe.cafe_name = rows.CAFE_NAME
		cafe.cafe_address = rows.CAFE_ADDRESS
		cafe.location_id = int(rows.LOCATION_ID)
		cafe.opentime = str(rows.OPEN_TIME)
		cafe.closetime = str(rows.CLOSE_TIME)
		cafe.image_url = rows.IMAGE_URL

		cursor.execute("select * from location where location_id = ?", cafe.location_id)
		rows = cursor.fetchone()
		location.location_id = rows.LOCATION_ID
		location.address = rows.ADDRESS
	return render(request, 'blog/search.html', {'logined_user':logined_user, "cafe":cafe, "location":location})

def mypage(request):
	return render(request, 'blog/mypage.html', {'logined_user':logined_user})

def login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		logined_user.user_id = int(request.POST.get('user_id'))
		cursor.execute("SELECT * FROM USERTABLE WHERE USER_ID = ?", logined_user.user_id)
		rows = cursor.fetchone()
		if  rows == None:
			return HttpResponse('fail')
		else :
			logined_user.username = rows.USER_NAME
			logined_user.sex = rows.SEX
			logined_user.location_id = rows.LOCATION_ID
			return redirect('search')
	return render(request, 'blog/login.html', {})

def logout(request):
	logined_user.username = "null"
	return redirect('main')


def cafelist_cafe(request):
	if request.method == "POST":
		resultcafe = []
		key = request.POST['_search']
		cursor.execute("select * from cafe where cafe_name like ?", '%'+key+'%')
		rows = cursor.fetchall()
		for i in range (len(rows)):
			temp = []
			temp.append(int(rows[i].CAFE_ID))
			temp.append(rows[i].CAFE_NAME)
			temp.append(rows[i].CAFE_ADDRESS)
			resultcafe.append(temp)
	return render(request, 'blog/cafelist_cafe.html', {'resultcafe':resultcafe})


def cafelist_location(request):
	if request.method == "POST":
		resultcafe = []
		key = request.POST['_search']
		cursor.execute("select * from cafe where cafe_address like ?", '%'+key+'%')
		rows = cursor.fetchall()
		for i in range (len(rows)):
			temp = []
			temp.append(int(rows[i].CAFE_ID))
			temp.append(rows[i].CAFE_NAME)
			temp.append(rows[i].CAFE_ADDRESS)
			resultcafe.append(temp)
	return render(request, 'blog/cafelist_cafe.html', {'resultcafe':resultcafe})
