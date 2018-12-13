import hashlib
import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtype, Goods, User, Cart, Order, OrderGoods


def home(request):

    # 获取轮播图数据
    wheels = Wheel.objects.all()

    # 获取导航数据
    navs = Nav.objects.all()

    # 获取每日必购数据
    mustbuys = Mustbuy.objects.all()

    # 商品部分数据
    shops = Shop.objects.all()  # 所有
    shophead = shops[0]
    shoptabs = shops[1:3]
    shopclass = shops[3:7]
    shopcommends = shops[7:11]

    # 商品列表
    mainShows = MainShow.objects.all()

    data = {
        'wheels':wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shophead': shophead,
        'shoptabs': shoptabs,
        'shopclass': shopclass,
        'shopcommends': shopcommends,
        'mainShows': mainShows
    }

    return render(request, 'home/home.html', context=data)

def marketbase(request):
    # 默认是热销榜， 全部分类， 综合排序
    return redirect('axf:market', 104749, 0, 0)

# 参数1: categoryid 分类
# 参数2: childid 子类
# 参数3: sortid 排序方式
def market(request, categoryid, childid, sortid):
    # 分类信息
    foodtypes = Foodtype.objects.all()

    # 获取 分类下标  >>> typeIndex
    # 没有时，默认为0  >>> 默认热销数据
    typeIndex = int(request.COOKIES.get('typeIndex', 0))
    # 根据下标   获取  分类id
    categoryid = foodtypes[typeIndex].typeid

    # 子类信息
    childtypenames = foodtypes[typeIndex].childtypenames
    childtypelist = []
    for item in childtypenames.split('#'):
        # 子类名称: 子类ID
        # print(item)
        temp = item.split(':')
        dir = {
            'childname': temp[0],
            'childid': temp[1]
        }
        childtypelist.append(dir)

    # 商品信息
    # goodslist = Goods.objects.all()[0:10]
    # 商品信息 -- 分类
    # goodslist = Goods.objects.filter(categoryid=categoryid)
    if childid == '0':  # 全部分类
        goodslist = Goods.objects.filter(categoryid=categoryid)
    else:
        goodslist = Goods.objects.filter(categoryid=categoryid).filter(childcid=childid)

    # 0 综合排序
    if sortid == '1':   # 销量排序
        goodslist = goodslist.order_by('-productnum')
    elif sortid == '2': # 价格最低
        goodslist = goodslist.order_by('price')
    elif sortid == '3': # 价格最高
        goodslist = goodslist.order_by('-price')


    token = request.session.get('token')
    carts = []
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user)



    data = {
        'foodtypes': foodtypes,
        'goodslist': goodslist,
        'childtypelist': childtypelist,
        'categoryid': categoryid,
        'childid': childid,
        'carts':carts
    }

    return render(request, 'market/market.html', context=data)


def cart(request):
    token = request.session.get('token')
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)

        data = {
            'carts':carts
        }

        return render(request, 'cart/cart.html',context=data)
    else:
        return redirect('axf:login')



def mine(request):
    # 获取用户信息
    token = request.session.get('token')

    data = {}

    if token:
        user = User.objects.get(token=token)
        data['name'] = user.name
        data['img'] = user.img
        data['rank'] = user.rank

        orders = Order.objects.filter(user=user)
        data['waitpay'] = orders.filter(status=0).count()
        data['paydone'] = orders.filter(status=1).count()


    return render(request, 'mine/mine.html', context=data)


import time
def generate_token():
    md5 = hashlib.md5()
    temp = str(time.time()) + str(random.random())
    md5.update(temp.encode('utf-8'))
    return  md5.hexdigest()


def generate_password(param):
    md5 = hashlib.md5()
    md5.update(param.encode('utf-8'))
    return md5.hexdigest()


def register(request):
    if request.method == 'GET':
        return render(request, 'mine/register.html')
    elif request.method == 'POST':
        user = User()
        user.email = request.POST.get('email')
        user.password = generate_password(request.POST.get('password'))
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')

        # 状态保持
        user.token = generate_token()
        user.save()
        request.session['token'] = user.token

        return redirect('axf:mine')


def checkemail(request):

    # 邮箱
    email = request.GET.get('email')

    users = User.objects.filter(email=email)
    if users.exists():
        return JsonResponse({'msg': '账号已被占用!', 'status': 0})
    else:
        return JsonResponse({'msg': '账号是可以使用!', 'status': 1})


def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(generate_password(password))

        try:
            # 不存在，会抛出异常
            # 多个时，会抛出异常　【email是唯一约束】
            user = User.objects.get(email=email)
            if user.password == generate_password(password):
                user.token = generate_token()
                user.save()
                request.session['token'] = user.token
                return redirect('axf:mine')
            else:
                return render(request, 'mine/login.html', context={'p_err': '密码错误'})
        except:
            return render(request, 'mine/login.html', context={'u_err': '账号不存在'})


def logout(request):
    request.session.flush()
    return redirect('axf:mine')


def addcart(request):
    token = request.session.get('token')

    goodsid = request.GET.get('goodsid')

    data = {}

    if token:
        user = User.objects.get(token=token)

        goods = Goods.objects.get(pk=goodsid)

        carts = Cart.objects.filter(user=user).filter(goods=goods)

        if  carts.exists():
            cart = carts.first()
            cart.number = cart.number + 1
            cart.save()

        else:
            cart = Cart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()
        return JsonResponse({'msg':'{},添加购物车成功'.format(goods.productlongname), 'number':cart.number, 'status': 1})

    else:
        data['msg'] = '请登录后操作!'
        data['status'] = -1
        return JsonResponse(data)



def subcart(request):
    token = request.session.get('token')
    goodsid = request.GET.get('goodsid')

    user = User.objects.get(token=token)
    goods = Goods.objects.get(pk=goodsid)

    cart = Cart.objects.filter(user=user).filter(goods=goods).first()

    cart.number = cart.number - 1
    cart.save()

    data = {
        'msg':'购物车删减成功',
        'status':1,
        'number':cart.number,
    }


    return JsonResponse(data)


def changecartstatus(request):
    cartid = request.GET.get('cartid')

    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()

    data = {
        'msg':'修改状态成功',
        'status':1,
        'isselect':cart.isselect,
    }

    return JsonResponse(data)



def changecartisall(request):
    token = request.session.get('token')
    user = User.objects.get(token=token)
    carts = Cart.objects.filter(user=user)

    isall = request.GET.get('isall')

    if isall == 'true':
        isall = True
    else:
        isall = False


    for cart in carts:
        cart.isselect = isall
        cart.save()

    data = {
        'msg':'全选/取消全选',
        'status':1
    }

    return JsonResponse(data)


def generate_identifier():
    temp = str(random.randrange(1000,10000)) + str(int(time.time())) + str(random.randrange(1000,10000))
    return temp

def generateorder(request):
    token = request.session.get('token')
    user = User.objects.get(token=token)

    order = Order()
    order.user = user
    order.identifier = generate_identifier()
    order.save()


    carts = Cart.objects.filter(user=user).filter(isselect=True)
    for cart in carts:
        orderGoods = OrderGoods()
        orderGoods.order = order
        orderGoods.goods = cart.goods
        orderGoods.number = cart.number
        orderGoods.save()

        cart.delete()


    data = {
        'msg':'下单成功',
        'status':1,
        'identifier':order.identifier
    }

    return JsonResponse(data)


def orderdetail(request,identifier):
    order = Order.objects.get(identifier=identifier)

    return render(request,'order/orderdetail.html',context={'order':order})


def orderlist(request,stu):
    token = request.session.get('token')
    user = User.objects.filter(token=token)

    orders = Order.objects.filter(user=user).filter(status=stu)

    return render(request,'order/orderlist.html',context={'orders':orders})