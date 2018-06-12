from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.http import HttpResponse
from .models import *
import datetime
import pyodbc
conn = pyodbc.connect("DSN=TIBERO;UID=DBdotae;PWD=dbdotae")
cursor = conn.cursor()

logined_user = User()
logined_user.username = "null"

cafe = Cafe()
cafe.cafe_id = "null"

location = Location()
location.location_id = 'null'

log = Log()
log.cafe_id = 'null'

coupon = Coupon()

log_user_num = []
menu_list = []
time_result = []
price_result = []

def main(request):
	return render(request, 'blog/main.html', {'logined_user':logined_user})

def search(request):
	if request.method == "POST":
		clickmenu = request.POST.get('image_code_name')

		cafe.cafe_id = int(request.POST.get('cafeID'))
		cursor.execute("SELECT * from cafe where cafe_id = ?", cafe.cafe_id)
		rows = cursor.fetchone()
		cafe.cafe_name = rows.CAFE_NAME
		cafe.cafe_address = rows.CAFE_ADDRESS
		cafe.location_id = int(rows.LOCATION_ID)
		cafe.opentime = str(rows.OPEN_TIME)
		cafe.closetime = str(rows.CLOSE_TIME)
		cafe.image_url = str(rows.IMAGE_URL)

		cursor.execute("SELECT * from location where location_id = ?", cafe.location_id)
		rows = cursor.fetchone()
		location.location_id = rows.LOCATION_ID
		location.address = rows.ADDRESS

		log_user_num = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		time_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		log.cafe_id = int(request.POST.get('cafeID'))
		cursor.execute("SELECT * from LOGTABLE where cafe_id=?", log.cafe_id)
		rows = cursor.fetchall()
		for i in range (len(rows)):
			time = str(rows[i].TIME)
			num = int(rows[i].USER_NUM)
			time = time[:2]
			log_user_num[int(time)] += num
			time_count[int(time)] += 1
		for i in range(0,24):
			if time_count[i] != 0:
				log_user_num[i] = log_user_num[i] // time_count[i]

		cursor.execute("SELECT to_char(sysdate,'hh24') from dual")
		current = cursor.fetchone()
		c_current = int(current[0])
		current = str(current[0])
		current += ":00:00"

		menu_list = []
		cursor.execute("SELECT * from menu where cafe_id = ?", cafe.cafe_id)
		rows = cursor.fetchall()
		for i in range (len(rows)):
			temp = []
			cursor.execute("SELECT * from menucode where menu_code = ?", rows[i].MENU_CODE)
			rows_1 = cursor.fetchone()
			temp.append(rows[i].MENU_NAME)
			temp.append(int(rows[i].PRICE))
			temp.append(rows_1.MENU_URL)
			temp.append(int(rows_1.MENU_CODE))
			menu_list.append(temp)

		time_result = []
		cursor.execute("SELECT * from cafe where cafe_id = ANY (select * from (select cafe_id  from (select * from logtable where cafe_id = ANY (select cafe_id from cafe where location_id = ? )) where time = ? having avg(user_num) < ? group by cafe_id order by avg(user_num)) where rownum <= 2);", cafe.location_id, current, log_user_num[c_current])
		rows = cursor.fetchall()
		for i in range(len(rows)):
			temp = []
			temp.append(rows[i].CAFE_NAME)
			temp.append(rows[i].CAFE_ADDRESS)
			time_result.append(temp)

		price_result = []
		cursor.execute("SELECT * from (select * from cafe where location_id = ? and cafe_id <> ? ) where cafe_id = ANY (select * from  (select cafe_id from menu where menu_code = ( select favorite from usertable where user_id = ? ) order by price ) where rownum <= 1000);", cafe.location_id, cafe.cafe_id, logined_user.user_id)
		rows = cursor.fetchall()
		for i in range(len(rows)):
			if i == 2:
				break
			temp = []
			temp.append(rows[i].CAFE_NAME)
			temp.append(rows[i].CAFE_ADDRESS)
			price_result.append(temp)

	return render(request, 'blog/search.html', {'logined_user':logined_user, "cafe":cafe, "location":location, "log_user_num":log_user_num, "menu_list":menu_list, "time_result":time_result, "price_result":price_result})

def mypage(request):
	if request.method == "POST":
		favorite = request.POST.get('choice')
		cursor.execute("SELECT * FROM MENUCODE WHERE MENU_NAME = ?", favorite)
		rows = cursor.fetchone()
		logined_user.favorite = favorite
		menuc = rows.MENU_CODE
		cursor.execute("UPDATE USERTABLE SET FAVORITE = ? where user_id = ?", menuc, logined_user.user_id)		
	cursor.execute("SELECT * from coupon c1, cafe c2 where c1.user_id = ? and c1.cafe_id = c2.cafe_id", logined_user.user_id)
	rows = cursor.fetchall()
	couponlist = []
	for i in range (len(rows)):
			temp = Coupon()
			temp.user_id = rows[i].USER_ID
			temp.cafe_name = rows[i].CAFE_NAME
			temp.count = int(rows[i].COUNT)
			couponlist.append(temp)
	cursor.execute("SELECT * from MENUCODE")
	rows = cursor.fetchall()
	favoritelist = []
	for i in range (len(rows)):
		favoritelist.append(rows[i].MENU_NAME)
	return render(request, 'blog/mypage.html', {'logined_user':logined_user, 'couponlist':couponlist, 'favoritelist':favoritelist})

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
			favorite_code = rows.FAVORITE
			cursor.execute("SELECT address FROM LOCATION WHERE location_id = ?", logined_user.location_id)
			row = cursor.fetchone()
			logined_user.address = row.ADDRESS
			cursor.execute("SELECT MENU_NAME FROM MENUCODE WHERE MENU_CODE = ?", favorite_code)
			row = cursor.fetchone()
			logined_user.favorite = row.MENU_NAME
			return redirect('main')
	return render(request, 'blog/login.html', {})

def logout(request):
	logined_user.username = "null"
	return redirect('main')


def cafelist_cafe(request):
	if request.method == "POST":
		resultcafe = []
		key = request.POST['_search']
		cursor.execute("SELECT * from cafe where cafe_name like ?", '%'+key+'%')
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
		cursor.execute("SELECT * from cafe where cafe_address like ?", '%'+key+'%')
		rows = cursor.fetchall()
		for i in range (len(rows)):
			temp = []
			temp.append(int(rows[i].CAFE_ID))
			temp.append(rows[i].CAFE_NAME)
			temp.append(rows[i].CAFE_ADDRESS)
			resultcafe.append(temp)
	return render(request, 'blog/cafelist_location.html', {'resultcafe':resultcafe})

def  addresslist(request):
	if request.method == "POST":
		resultaddress = []
		key = request.POST['_address']
		cursor.execute("SELECT * from location where ADDRESS like ?", '%'+key+'%')
		rows = cursor.fetchall()
		for i in range (len(rows)):
			temp = []
			temp.append(int(rows[i].LOCATION_ID))
			temp.append(rows[i].ADDRESS)
			resultaddress.append(temp)
	return render(request, 'blog/addresslist.html', {'resultaddress':resultaddress})

def  addresschoice(request):
	if request.method == "POST":
		key = request.POST.get('addressID')
		cursor.execute("SELECT * FROM LOCATION WHERE location_id = ?", key)
		rows = cursor.fetchone()
		logined_user.location_id = rows.LOCATION_ID
		logined_user.address = rows.ADDRESS
		cursor.execute("UPDATE USERTABLE SET LOCATION_ID = ? where user_id = ?",logined_user.location_id , logined_user.user_id)
	return redirect('mypage')

def price_choice(request):
	price_result = []
	if request.method == "POST":
		clickmenu = request.POST.get('image_code_name')
		price_result = []
		cursor.execute("SELECT * from (select * from cafe where location_id = ? and cafe_id <> ? ) where cafe_id = ANY (select * from  (select cafe_id from menu where menu_code = ? order by price ) where rownum <= 1000);", cafe.location_id, cafe.cafe_id, clickmenu)
		rows = cursor.fetchall()
		for i in range(len(rows)):
			if i == 2:
				break
			temp = []
			temp.append(rows[i].CAFE_NAME)
			temp.append(rows[i].CAFE_ADDRESS)
			price_result.append(temp)
	return render(request, 'blog/price_choice.html', {"price_result":price_result})