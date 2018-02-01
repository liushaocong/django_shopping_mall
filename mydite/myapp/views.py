from django.shortcuts import HttpResponse,render,redirect,HttpResponseRedirect
# Create your views here.
from .models import User,Commod,Detail,Cat,Orders
from django import forms
from werkzeug.security import generate_password_hash
from django.contrib.auth import authenticate
import time,random

def register(request):
    return render(request ,'register.html')

def login(request):
    # name = request.COOKIES.get('name')
    # if name:
    #     return redirect('/index/',{"username":name})

    username = None
    if request.method == 'POST':
        username = request.POST.get("username")
        pwd = request.POST.get("pwd")
        user = User.objects.filter(username=username)
        # =================认证结束====================
        if user and user[0].verify_password(pwd):
            # response = redirect('/index',{"username":'lsc'})
            response = HttpResponseRedirect('/index')
            response.set_cookie('name',username,60*60*24*1)
            return response
                # return render(request,'feedback.html')
              # 这里直接写模版渲染，就不能设置cookie的过期时间了
        else:
            return render(request,'login.html')

    return render(request,'login.html')


def logout(request):
    response = redirect('/index')
    #清理cookie里保存username
    response.delete_cookie('name')
    return response




    # if request.method == "POST":
    #     username = request.POST.get("username")
    #     pwd = request.POST.get("pwd")
    #     user = User.objects.filter(username=username)
    #     if len(user) == 0:
    #         print("登录失败")
    #     elif len(user) == 1:
    #         if user[0].username == username and user[0].verify_password(pwd):
    #             print("登录成功")
    #             return redirect('/index/')
    #         else:
    #             print("登录失败")
    #
    # return render(request,'login.html')

# 注册
def userinfo(request):
    if request.method == "POST":
        username = request.POST.get("user_name")
        pwd = request.POST.get("pwd")
        cpwd = request.POST.get("cpwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")
        # print(username,pwd,cpwd,email,allow)
        print(allow)
        if allow == "on" and pwd == cpwd:
            user = User(username=username,password=pwd,email=email)
            user.save()
            return redirect('/login/')
        else:
            return redirect('/register/')
        return HttpResponse("ok")

def index(request):
    username = request.COOKIES.get('name', '')
    com = Commod.objects.filter(types="饰品")[:4]
    flower = Commod.objects.filter(types="鲜花")
    arts = Commod.objects.filter(types="工艺品")
    birs = Commod.objects.filter(types="结婚礼物")
    products = Commod.objects.filter(types="保健用品")
    elder = Commod.objects.filter(types="长辈礼物")
    return render(request,'index.html',{"username":username,"com":com,"flower":flower,"arts":arts,"birs":birs,"products":products,"elder":elder})

def user_center_info(request):
    username = request.COOKIES.get('name', '')
    user = User.objects.filter(username=username).first()
    phone = Detail.objects.filter(user=user).first()

    if user:
        name = user.username
    else:
        name = ""

    if phone:
        phone1 = phone.phone
        address = phone.address
    else:
        phone1 = ""
        address = ""
    return render(request,'user_center_info.html',{"username":username,"name":name,"phone":phone1,"address":address})

def user_center_order(request):
    otimes = ""
    ocode = ""
    btimes = ""
    bcode = ""
    price = 0
    b_proce = 0
    username = request.COOKIES.get('name', '')
    user = User.objects.filter(username=username).first()
    if username:
        orders = Orders.objects.filter(user=user).filter(types=False)
        buys = Orders.objects.filter(user=user).filter(types=True)
        if buys:
            for b in buys:
                b_proce += b.price
                btimes = b.times
                bcode = b.order
        if orders:
            for o in orders:
                price += o.price
                otimes = o.times
                ocode = o.order

        return render(request,'user_center_order.html',{"username":username,"orders":orders,"price":price,"otimes":otimes,"ocode":ocode,"btimes":btimes,"bcode":bcode,"buys":buys,"b_price":b_proce})
    return render(request, 'user_center_order.html',{"username":username})
def user_center_site(request):
    username = request.COOKIES.get('name', '')
    user = User.objects.filter(username=username).first()
    detail = Detail.objects.filter(user=user).first()
    if detail:
        address = detail.address
    else:
        address = ""

    print(address)

    return render(request,'user_center_site.html',{"username":username,"address":address})

def site_add(request):
    username = request.COOKIES.get('name', '')
    users = User.objects.filter(username=username)

    # if username:
    #     return redirect("/register")
    if request.method == "POST":
        user = users[0]
        recipient = request.POST.get("recipient")
        address = request.POST.get("address")
        postcode = request.POST.get("postcode")
        phone = request.POST.get("phone")
        detail = Detail(user=user,recipient=recipient,address=address,postcode=postcode,phone=phone)
        detail.save()
    return HttpResponseRedirect("/user_center_site")

def detail(request,id):
    commod = Commod.objects.filter(id=id)

    if commod:
        commods = commod
        # print(commods.image)
    else:
        return redirect('/index')
    return render(request,'detail.html',{"commods":commods})

def add_cat(request,id):
    username = request.COOKIES.get('name', '')
    users = User.objects.filter(username=username).first()

    commod = Commod.objects.filter(id=id).first()
    cat = Cat(commod=commod,user=users,images=commod.image,title=commod.title,price=commod.price,num=1,price_all=1)
    cat.save()
    return redirect('/cart')

def cart(request):
    username = request.COOKIES.get('name', '')
    price = 0
    username = request.COOKIES.get('name', '')
    users = User.objects.filter(username=username).first()
    cat = Cat.objects.filter(user = users)
    for c in cat:
        price += c.price
    print(price)
    nums = len(cat)
    return render(request,'cart.html',{"username":username,"cat":cat,"price":price,"nums":nums})

def place(request):
    username = request.COOKIES.get('name', '')
    users = User.objects.filter(username=username).first()
    cat = Cat.objects.filter(user = users)
    orders = Orders.objects.filter(types=False).all()
    if cat:
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        ran = int(random.random()*10**15)
        for c in cat:
            # print(c.images)
            order = Orders(commod=c,user=users,times=localtime,order=ran,images=c.images,title=c.title,types=False,num=c.num,price=c.price)
            order.save()
        Cat.objects.filter(user=users).delete()

        # print(c)
    return redirect("/user_center_order")

def go(request):
    orders = Orders.objects.filter(types=False).all().update(types=True)
    return redirect("/user_center_order")