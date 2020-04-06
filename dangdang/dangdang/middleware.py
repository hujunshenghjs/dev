from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from home.models import TUser


class MyMiddleware(MiddlewareMixin):  # 自定义的中间件
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)

    # 前端页面发请求   -> 视图函数

    # view处理请求前执行
    def process_request(self, request):  # 某一个view
        if '/' == request.path:  # 直接进入主页
            return redirect('home:index')
        # 从哪来回哪去
        book_id = request.GET.get('id')
        print(book_id, "中间件里书的id")
        if 'index' in request.path or 'book_list' in request.path or 'book_details' in request.path or 'shopping_car' in request.path or 'indent_page' in request.path:       # 从这些路径开始跳转时
            print(request.path, "是当前路径")
            if request.path == '/dangdang/book_details/':  # 如果路径是这个
                request.session['url'] = request.path + '?id=' + book_id  # 将拼接有书的id的路径保存
                print(request.session['url'])
            else:
                request.session['url'] = request.path  # 否则就正常的将path保存
        if request.session.get('flag'):   # 判断是否有标记，有标记不做任何事
            pass
        else:
            if 'index' in request.path or \
                    'book_list' in request.path or\
                    'Book details' in request.path or \
                    'shopping_car' in request.path:
                username = request.COOKIES.get('username')  # 取用户名
                password = request.COOKIES.get('password')  # 取密码
                url = request.session.get('url')
                if username:  # 如果用户名存在，验证用户名密码是否正确
                    if '@' in username:
                        result = TUser.objects.filter(username=username, password=password, status=1)
                    else:
                        result = TUser.objects.filter(phone_number=username, password=password, status=1)
                    if result:
                        print('存了')
                        request.session['flag'] = True
                        request.session['login_status'] = True
                        request.session['username'] = username
                        return redirect(url)
                    request.session['flag'] = True
                    return redirect(url)
                request.session['flag'] = True
                return redirect(url)
        # 强制登录

        if 'indent_page' in request.path or 'indent_ok' in request.path:
            if request.session.get('login_status'):
                pass
            else:
                return redirect('login_registerapp:login')
            # 限制访问页面
            if 'indent_page' in request.path or 'indent_ok' in request.path:
                if request.META.get('HTTP_REFERER') is None:
                    return redirect('home:index')

    # 在process_request之后View之前执行
    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    # view执行之后，响应之前执行
    def process_response(self, request, response):
        # print("response:", request, response, '中间件第38行打印~~~')
        return response  # 必须返回response

    # 如果View中抛出了异常
    def process_exception(self, request, ex):  # View中出现异常时执行
        # print("exception:", request, ex, '中间件第43行打印~~~')
        pass
