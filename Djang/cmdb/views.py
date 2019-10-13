from django.shortcuts import render

from django.shortcuts import HttpResponse

from django.shortcuts import HttpResponseRedirect

from cmdb import  models
import  pymysql
import requests
import json
import random

con = pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    password = "123456",
    db = "215",
    charset = "utf8"
)
cursor = con.cursor()


# Create your views here.
def test(request):
    print("进入后台！")
    return HttpResponse("成功！")


def index(request):
    if request.method=='POST':
        return HttpResponse("POST请求")
    else:
        return render(request,"login1.html")


def login(request):
    username = request.GET.get("username",None)
    password = request.GET.get("password",None)
    m = request.GET.get("we",None)
    models.UserInfo.objects.create(user=username,password=password)
    models.UserInfo.objects.create(user='lisi',password='666')
    userList = models.UserInfo.objects.all()
    return  render(request,"info.html",{"data":userList})

def addUser1(request):
    return render(request, "addUser1.html")
def addUs(request):
    username = request.GET.get("username",None)
    password = request.GET.get("password",None)
    cursor.execute("insert into user2(username,password) values('%s','%s')"%(username,password))
    con.commit()
    userList = []
    cursor.execute("select * from user2")
    for y in cursor.fetchall():
        dict1 = {}
        dict1["id"] = y[0]
        dict1["username"] = y[1]
        dict1["password"] = y[2]
        userList.append(dict1)
    return render(request, "login1.html", {"data": userList})

def checkLogin(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    cursor.execute("select * from user2 where username='%s'" % username)
    if cursor.rowcount > 0:
        for x in cursor.fetchall():
            if x[2]==password:
                userList = []
                cursor.execute("select * from user2")
                for y in cursor.fetchall():
                    dict1 = {}
                    dict1["id"] = y[0]
                    dict1["username"] = y[1]
                    dict1["password"] = y[2]
                    userList.append(dict1)
                return render(request, "success.html", {"data": userList,'dqyh':"欢迎" + username + "登录！"})
            else:
                return render(request, "login1.html", {"info": "密码错误！"})
    else:
        return render(request, "login1.html", {"info": "用户名不存在！"})

def addUI(request):
    return render(request,"addUser.html")

def add(request):
    username = request.GET.get("username",None)
    password = request.GET.get("password",None)
    cursor.execute("insert into user2(username,password) values('%s','%s')"%(username,password))
    con.commit()
    return HttpResponseRedirect("/showUsers/")

def delUser(request):
    id = request.GET.get("id",None)
    cursor.execute("delete from user2 where id="+id+"")
    con.commit()
    return HttpResponseRedirect("/showUsers/")

def showUsers(request):
    userList = []
    cursor.execute("select * from user2")
    for y in cursor.fetchall():
        dict1 = {}
        dict1["id"] = y[0]
        dict1["username"] = y[1]
        dict1["password"] = y[2]
        userList.append(dict1)
    return render(request, "success.html", {"data": userList})

def updateUser(request):
    id = request.GET.get("id", None)
    cursor.execute("select * from user2 where id=" + id + "")
    user = []
    for x in cursor.fetchall():
        dict2 = {}
        dict2["id"] = x[0]
        dict2["username"] = x[1]
        dict2["password"] = x[2]
        user.append(dict2)
    return render(request, "updateUser.html", {"user": user})

def update(request):
    id = request.GET.get("id")
    print(id)
    username = request.GET.get("username")
    password = request.GET.get("password")

    #发送sql语句进行修改
    cursor.execute("update user2 set username='"+username+"',password='"+password+"' where id="+id+"")

    #提交
    con.commit()

    #重定向
    return HttpResponseRedirect("/showUsers/")


def  queryUserByUsername(request):
    username =request.GET.get("username")

    #通过username查出用户
    cursor.execute("select * from user2 where  username like '"+username+"%'")
    userList =[]
    for y in cursor.fetchall():
        dict1 = {}
        dict1["id"] = y[0]
        dict1["username"] = y[1]
        dict1["password"] = y[2]
        userList.append(dict1)
    return render(request, "success.html", {"data": userList})



def jumpUI(request):
    return render(request, "success1.html")

def ginUsers(request):
    return render(request, "login1.html")

class Num():
    number = 0
num = Num()

def jsonUsers(request):
    reoponse = requests.get("https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start="+str(num.number)+"")
    data = json.loads(reoponse.text)
    print(type(data))
    movies = data.get("subjects")
    # print(type(movies))
    for x in movies:
        data = (x.get("rate"), x.get("title"), x.get("url"), x.get("cover"))
        cursor.execute("insert into movies(rate,title,url,cover) values('%s','%s','%s','%s')" % data)
        # 提交
        con.commit()
    num.number += 1
    return render(request, "success1.html")

def jsonUser(request):
    userL = []
    cursor.execute("select * from movies")
    for y in cursor.fetchall():
        dict1 = {}
        dict1["id"] = y[0]
        dict1["rate"] = y[1]
        dict1["title"] = y[2]
        dict1["url"] = y[3]
        dict1["cover"] = y[4]
        userL.append(dict1)
    return render(request, "json.html", {"json": userL})

def josnDel(request):
    id = request.GET.get("id", None)
    cursor.execute("delete from movies where id=" + id + "")
    con.commit()

    user = []
    cursor.execute("select * from movies")
    for x in cursor.fetchall():
        dict2 = {}
        dict2["id"] = x[0]
        dict2["rate"] = x[1]
        dict2["title"] = x[2]
        dict2["url"] = x[3]
        dict2["cover"] = x[4]
        user.append(dict2)
    return render(request, "json.html", {"json": user})

def  jsonUserByUsername(request):
    username =request.GET.get("username")

    #通过username查出用户
    cursor.execute("select * from movies where  title like '"+username+"%'")
    userList =[]
    for y in cursor.fetchall():
        dict1 = {}
        dict1["id"] = y[0]
        dict1["rate"] = y[1]
        dict1["title"] = y[2]
        dict1["url"] = y[3]
        dict1["cover"] = y[4]
        userList.append(dict1)
    return render(request, "json.html", {"json": userList})





def Tie(request):
    key = request.GET.get("key")
    list1 = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"
    }
    print(key)
    for x in range(10):
        dict3 = {}
        a = 1 * x
        url = "http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}".format(key,a)
        print(url)
        data = requests.post(url, headers=headers).content.decode()
        ye = "tie/{}吧 第{}页.html".format(key, x+1)
        dict3["ye"] = "{}吧 第{}页.html".format(key, x+1)
        dict3["url"] = "http://localhost:63342/Djang/{}".format(ye)
        list1.append(dict3)
        with open(ye, "w", encoding="utf-8") as f:
            f.write(data)
    return render(request,"success1.html", {"Tie":list1})



def deng(request):
    return render(request, "success1.html")










