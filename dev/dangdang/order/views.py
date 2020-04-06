from django.shortcuts import render, redirect
from django.http import JsonResponse
from home.models import TUser, TAddress, TOrder, TOrderDetail, TShoppingCart
from django.db import transaction
import re
from shopping_car.car import Book, Car
from django.db.models import Sum
from datetime import datetime
from order.generate_order_number import generate_order_number

# Create your views here.


# 渲染订单页面
def indent_page(request):
    username = request.session.get('username')  # 获取session中的用户名
    if '@' in username:
        user_id = TUser.objects.filter(username=username)[0].id
    else:
        user_id = TUser.objects.filter(phone_number=username)[0].id

    address = TAddress.objects.filter(user_id=user_id)  # 获取相应用户的地址信息
    car = TShoppingCart.objects.filter(user_id=user_id)  # 获取相应用户的购物车
    order = Car()

    for book in car:
        order.add_shopping_car(book.book_id, book.quantity)
    total_price = 0
    for book in order.book_items:
        total_price += book.total_price
    request.session['total_price'] = total_price
    request.session['order'] = order
    print(request.session.get('order'), "这是存进去的order")
    return render(request, 'indent.html', {
        'username': username,
        'address': address,
        'total_price': total_price,
        'order': order,
    })


def select_address(request):
    addr_id = request.POST.get('addr_id')  # 获取地址id
    address = TAddress.objects.filter(id=addr_id)[0]  # 通过地址id找到地址信息

    def address_default(addr):
        if isinstance(addr, TAddress):
            return {
                'id': addr.id,  # 地址id
                'consignee': addr.consignee,  # 名字
                'address': addr.address,  # 地址信息
                'postcode': addr.postcode,  # 邮编
                'phone_number': addr.phone_number,  # 电话号码
                'telephone': addr.telephone,  # 邮箱
                'user_id': addr.user_id  # 用户id
            }

    return JsonResponse({'msg': address, 'status': 1}, json_dumps_params={"default": address_default})


# 提交地址信息
def submit_address(request):
    addr_id = request.POST.get('addr_id')  # 获取地址id
    consignee = request.POST.get('ship_man')  # 获取收货人
    print(consignee, "是收货人")
    address = request.POST.get('address')  # 获取详细地址
    zip_code = request.POST.get('zip_code')  # 获取邮编
    phone = request.POST.get('phone')  # 获取手机
    telephone = request.POST.get('telephone')  # 获取固定电话
    username = request.session.get('username')  # 获取用户名
    print(username, "是session中的名字")
    if '@' in username:
        user_id = TUser.objects.filter(username=username)[0].id  # 查询用户id
    else:
        user_id = TUser.objects.filter(phone_number=username)[0].id
    print(addr_id, consignee, address, zip_code, phone, telephone, user_id)

    if addr_id:  # 如果地址id存在
        res = TAddress.objects.filter(id=int(addr_id), user_id=int(user_id))  # 查找这条地址的详细信息
        if res:  # 如果存在
            address_obj = res[0]  # address_obj就是地址详情
        else:
            return JsonResponse({'msg': '...', 'status': 0})
    else:
        if consignee != '' and ('省' in address or '市' in address) and ('区' in address or '县' in address) and\
                re.match(r"[0-9]\d{5}(?!\d)", zip_code) and (re.match(r"^1[35678]\d{9}$", phone) or re.match("^0\\d{2,3}-\\d{7,8}$", telephone)):
            with transaction.atomic():  # 事务控制
                address_obj = TAddress.objects.create(consignee=consignee, address=address, postcode=zip_code,
                                                      phone_number=phone, telephone=telephone, user_id=user_id)  # 存地址
        else:
            return JsonResponse({'msg': '请检查信息是否填写正确', 'status': 0})
    with transaction.atomic():
        order_obj = TOrder.objects.create(order_number=generate_order_number(), generated_time=datetime.now(),
                                          total_price=request.session.get('total_price'), user_id=user_id,
                                          address_id=address_obj.id, status=0)  # 创建订单
        order = request.session.get('order')
        print(order, '这order哪去了')
        for book in order.book_items:
            TOrderDetail.objects.create(book_id=book.book_id, price=book.book_price, books_number=book.book_number,
                                        order_id=order_obj.id)
        del request.session['order']
        TShoppingCart.objects.filter(user_id=user_id).delete()
        return JsonResponse({'msg': '/order/indent_ok/', 'status': 1})


# 渲染订单完成页面
def indent_ok(request):
    username = request.session.get('username')
    if '@' in username:
        user_id = TUser.objects.filter(username=username)[0].id
    else:
        user_id = TUser.objects.filter(phone_number=username)[0].id
    print(user_id, 110)
    order = TOrder.objects.filter(user_id=user_id, status=0)
    print(order, '111行')
    if order:
        order_number = order[0].order_number
        total_price = order[0].total_price
        # books_number = order[0].torderdetail_set.all().aggregate(books_number=Sum('book_number'))['book_number']
        books_number = 123
        address = TAddress.objects.filter(id=order[0].address_id)[0]
        books = Car()
        for order_detail in TOrderDetail.objects.filter(order_id=order[0].id):
            books.add_shopping_car(order_detail.book_id, order_detail.books_number)
        order[0].status = 1
        order[0].save()
        return render(request, 'indent ok.html',{
            'username': username,
            'order_number': order_number,
            'total_price': total_price,
            'books_number': books_number,
            'address': address,
            'books': books.book_items
        })

    return redirect('shopping_car:shopping_car')


