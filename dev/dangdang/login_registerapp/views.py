import random, string
from django.db import transaction
from captcha.image import ImageCaptcha
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from home.models import TUser, TShoppingCart
import re
import hashlib
from django.core.mail import send_mail


# Create your views here.


# 渲染注册页面
def register(request):
    return render(request, 'register.html')


# 注册操作
def register_logic(request):
    name = request.POST.get('txt_username')  # 获取前端输入框中的名字
    pwd = request.POST.get('txt_password')  # 获取登录密码
    sha = hashlib.sha1()
    sha.update(pwd.encode())
    pwd = sha.hexdigest()   # 给密码加密
    try:
        with transaction.atomic():  # 开始一个事务环境，with结束时，如果没有异常，事务提交，否则回滚
            if '@' in name:  # 如果@符号在用户名中
                TUser.objects.create(username=name, password=pwd, status=1)  # 创建一条数据 邮箱的
                request.session['login_status'] = True  # 存储登录状态
                request.session['username'] = name  # 存储用户名
                return JsonResponse({'msg': '注册成功', 'status': 1})  # JsonResponse对象返回的是json对象就不需要做反序列化了  Http返回的是字符串
            else:
                TUser.objects.create(phone_number=name, password=pwd, status=1)  # 手机号的
                request.session['login_status'] = True  # 存储登录状态
                request.session['username'] = name  # 存储用户名
                return JsonResponse({'msg': '注册成功', 'status': 1})
    except Exception as error:
        print(error, "有错误")
        return JsonResponse({'msg': '注册失败', 'status': 0})  # 否则就是失败了


# 检查用户名
def checkname(request):
    username = request.POST.get('username')  # 获取名字
    if username == '':  # 如果名字是空
        return JsonResponse({'msg': '账号不可以为空', 'status': 0})
    if '@' in username:
        if re.match(r'^[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+){0,4}$', username):
            res = TUser.objects.filter(username=username)
            if res:
                return JsonResponse({'msg': '账号存在', 'status': 0})
            return JsonResponse({'msg': '邮箱格式正确', 'status': 1})
        return JsonResponse({'msg': '邮箱格式错误', 'status': 0})
    else:
        if re.match(r"^1[35678]\d{9}$", username):
            res = TUser.objects.filter(phone_number=username)
            if res:
                return JsonResponse({'msg': '此账号已存在', 'status': 0})
            return JsonResponse({'msg': '手机号可用', 'status': 1})
        return JsonResponse({'msg': '手机号格式错误', 'status': 0})


# 渲染登录页面
def login(request):
    username = request.COOKIES.get('username')
    password = request.COOKIES.get('password')
    print("名字是", username, "密码是", password)
    url = request.session.get('url')
    print("路径是", url, "888888888888899888888888")
    if username:
        if '@' in username:
            result = TUser.objects.filter(username=username, password=password)
        else:
            result = TUser.objects.filter(phone_number=username, password=password)
        if result:
            request.session['login_status'] = True
            request.session['username'] = username
            return redirect(url)
        return render(request, 'login.html')
    return render(request, 'login.html')


# 登录操作
def login_logic(request):
    # send_mail('x', 'gq', '1733874830@qq.com',
    #           ['1733874830@qq.com'], fail_silently=False)   # 给邮箱发验证码
    username = request.POST.get('username')
    password = request.POST.get('password')  # 获取名字和密码
    sha = hashlib.sha1()
    sha.update(password.encode())
    password = sha.hexdigest()   # 将密码加密
    remember = request.POST.get('auto_login')  # 获取自动登录
    url = request.session.get('url')  # 获取session中的路径
    if url == None:  # 如果是None
        url = '/dangdang/index'  # 就跳到主页面
    if '@' in username:
        result = TUser.objects.filter(username=username, password=password)
    else:
        result = TUser.objects.filter(phone_number=username, password=password)
    if result:
        request.session['login_status'] = True  # 存储登录状态
        request.session['username'] = username  # 存储用户名
        response = JsonResponse({'msg': url, 'status': 1})
        if remember:
            response.set_cookie('username', username, max_age=7 * 24 * 3600)
            response.set_cookie('password', password, max_age=7 * 24 * 3600)
            return response  # 将url 和 status发到前端
        car = request.session.get('car')  # 获取session的购物车
        if car:
            with transaction.atomic():
                for book in car.book_items:
                    user_book = TShoppingCart.objects.filter(book_id=book.book_id, user_id=result[0].id)
                    if user_book:
                        user_book[0].quantity += book.book_number
                        user_book[0].save()
                    else:
                        TShoppingCart.objects.create(quantity=book.book_number, book_id=book.book_id)
                del request.session['car']
        return response
    return JsonResponse({'msg': '帐号或密码错误', 'status': 0})


# 验证码
def captcha(request):
    image = ImageCaptcha()
    code = random.sample(string.ascii_letters + string.digits, 2)  # 生成验证码
    code = ''.join(code)  # 将验证码转换为字符串
    request.session['code'] = code  # 将验证码存入session中，以备后续验证
    print(code, '11111111111111111')  # 将验证码打印出来
    data = image.generate(code)  # 将随机码画到图片上去  二进制数据
    return HttpResponse(data, 'image/png')


# 检查验证码
def check_captcha(request):
    captcha_code = request.POST.get('code')
    if captcha_code.lower() == request.session.get('code').lower():
        return JsonResponse({'msg': '验证码正确', 'status': 1})
    return JsonResponse({'msg': '验证码错误', 'status': 0})


# 渲染注册成功页面
def register_ok(request):
    url = request.session.get('url')
    if url == None:
        url = '/dangdang/index/'
    username = request.session.get('username')
    return render(request, 'register ok.html', {'username': username, 'url': url})


# 退出登录
def sign_out(request):
    response = redirect('home:index')
    response.delete_cookie('username')
    response.delete_cookie('password')
    request.session.flush()
    return response
