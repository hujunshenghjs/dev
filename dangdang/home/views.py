from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from home.models import TBookClassification, TBooks
# Create your views here.


# 渲染主页面
def index(request):
    request.session['url'] = request.path
    username = request.session.get('username')
    c1 = TBookClassification.objects.filter(level=1)
    c2 = TBookClassification.objects.filter(level=2)
    # 新书上架部分
    books1 = TBooks.objects.all().order_by('-publishing_time')  # 出版时间 倒叙
    # 新书热卖榜
    books2 = TBooks.objects.all().order_by('-sales')[:8]    # 销量 倒叙
    # 主编推荐
    books3 = TBooks.objects.all().order_by('sales')    # 销量
    # 新书热卖榜2
    books4 = TBooks.objects.all().order_by('-sales')
    return render(request, 'index.html', {
        "c1": c1,
        "c2": c2,
        "books1": books1,
        "books2": books2,
        "books3": books3,
        "books4": books4,
        "username": username,
    })


# 渲染书籍列表页面
def book_list(request):
    request.session['url'] = request.path
    username = request.session.get('username')
    l1 = TBookClassification.objects.filter(level=1)  # 获取1级分类
    l2 = TBookClassification.objects.filter(level=2)  # 获取2级分类
    id = request.GET.get('id')  # 获取分类id
    level = request.GET.get('level')  # 获取分类等级
    if id and level:
        request.session['id'] = id
        request.session['level'] = level
    else:
        id = request.session.get('id')
        level = request.session.get('level')
    page_num = request.GET.get('number', default='1')  # 获取前端跳转页数
    queryset = TBookClassification.objects.filter(pk=0).none()  # 获取一个空的QuerySet对象.none()方法置空QuerySet
    if level == '1':
        data = TBookClassification.objects.filter(parent_id=id)  # 查询父类id为这个id的二级分类
        for i in data:
            book = TBooks.objects.filter(category_id=i.id)  # 获取一条数据的id
            queryset |= book  # 将数据合并Queryset
    elif level == '2':
        queryset = TBooks.objects.filter(category_id=id)
    else:
        queryset = TBookClassification.objects.filter(pk=0).none()
    pager_obj = Paginator(queryset, per_page=4)   # 构造分页器对象
    # 验证前端传回的数据是否合法，是不是纯数字，是不是在range范围中
    if page_num.isdigit() is not True or int(page_num) not in pager_obj.page_range:
        page_num = 1
    page_obj = pager_obj.page(int(page_num))  # 根据页数 显示信息
    return render(request, 'book_list.html',
                  {'l1': l1,
                   'l2': l2,
                   'page_obj': page_obj,
                   'username': username})


# 渲染书籍详情页面
def book_details(request):
    try:
        username = request.session.get('username')
        book_id = request.GET.get('id')
        print(book_id, "是书的id")
        book = TBooks.objects.filter(id=book_id)
        return render(request, 'Book details.html', {'book': book[0], 'username': username})
    except Exception as error:
        print(error)
        return HttpResponse('no book')



