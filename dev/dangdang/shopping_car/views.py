from django.http import JsonResponse
from django.shortcuts import render
from home.models import TBooks, TUser, TShoppingCart
# Create your views here.
from shopping_car.car import Book, Car
from home.models import TBooks
from django.db import transaction


# 购物车添加
def add_car(request):
    book_id = request.POST.get('book_id')  # 获取要添加的书的id
    number = request.POST.get('num', '1')
    car = request.session.get('car')
    if str(number).isdigit() and int(number) in range(1, 201):
        if request.session.get('login_status'):  # 如果登录了，获取用户id，检查session中cart是否存在
            username = request.session.get('username')  # 获取用户名
            if '@' in username:
                user_id = TUser.objects.filter(username=username)[0].id
            else:
                user_id = TUser.objects.filter(phone_number=username)[0].id
            with transaction.atomic():
                user_book = TShoppingCart.objects.filter(book_id=int(book_id), user_id=user_id)
                if user_book:
                    user_book[0].quantity += int(number)
                    user_book[0].save()
                else:
                    TShoppingCart.objects.create(quantity=int(number), book_id=int(book_id), user_id=user_id)
        else:
            if car:
                car.add_book(int(book_id), int(number))
                request.session['car'] = car
            else:
                car = Car()
                car.add_book(int(book_id), int(number))
                request.session['car'] = car
        return JsonResponse({'msg': '添加成功', 'status': 1})
    return JsonResponse({'msg': '添加失败，添加的数量要在1-200之间', 'status': 0})


# 渲染购物车页面
def shopping_car(request):
    username = request.session.get('username')
    if request.session.get('login_status'):
        print(request.session.get('login_status'), "是登录状态")
        if '@' in username:
            user_id = TUser.objects.filter(username=username)[0].id  # 获取用户id
        else:
            user_id = TUser.objects.filter(phone_number=username)[0].id  # 获取用户id
        books = TShoppingCart.objects.filter(user_id=user_id)
        car = Car()
        for book in books:
            car.add_shopping_car(book.book_id, book.quantity)
    else:
        print(request.session.get('login_status'), "是登录状态")
        car = request.session.get('car')
    return render(request, 'car.html', {
        'username': username,
        'car': car,
    })


def reduce_car(request):
    book_id = request.POST.get('book_id')  # 获取书籍id
    number = request.POST.get('num', '1')  # 获取添加的数量，默认为1
    car = request.session.get('car')  # 获取session中存储的购物车
    if str(number).isdigit() and int(number) in range(1, 201):  # 验证前端传回来的数字是否合法并且在（1~200）以内
        if request.session.get('login_status'):  # 如果登录了，获取用户id
            username = request.session.get('username')  # 获取用户名
            if '@' in username:
                user_id = TUser.objects.filter(username=username)[0].id  # 获取用户id
            else:
                user_id = TUser.objects.filter(phone_number=username)[0].id  # 获取用户id
            with transaction.atomic():  # 添加事务控制
                user_book = TShoppingCart.objects.filter(book_id=int(book_id), user_id=user_id)
                if user_book:
                    user_book[0].quantity -= int(number)
                    user_book[0].save()
        else:
            car.reduce_book(int(book_id), int(number))  # 注意传过去的值需是int类型
            request.session['car'] = car
        return JsonResponse({'msg': '减少成功', 'status': 1})
    return JsonResponse({'msg': '添加失败，添加的数量要在1-200之间', 'status': 0})


# 删除购物车逻辑
def del_car(request):
    book_id = request.POST.get('book_id')
    car = request.session.get('car')  # 获取session中存储的购物车
    if request.session.get('login_status'):  # 如果登录了，获取用户id
        username = request.session.get('username')  # 获取用户名
        if '@' in username:
            user_id = TUser.objects.filter(username=username)[0].id  # 获取用户id
        else:
            user_id = TUser.objects.filter(phone_number=username)[0].id  # 获取用户id
        with transaction.atomic():  # 添加事务控制
            user_book = TShoppingCart.objects.filter(book_id=int(book_id), user_id=user_id)
            if user_book:
                user_book[0].delete()
    else:
        car.del_book(int(book_id))  # 注意传过去的值需是int类型
        request.session['car'] = car
    return JsonResponse({'msg': '删除成功', 'status': 1})
