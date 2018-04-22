from django.shortcuts import render, redirect, HttpResponse
from io import BytesIO
from blog import models
from blog.utils.check_code import create_validate_code
from blog.forms import RegisterFm, LoginForms
import json

def check_cd(request):
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['check_code'] = code
    return HttpResponse(stream.getvalue())


def register(request):
    if request.method == 'GET':
        rfm_obj = RegisterFm()
        return render(request, 'register.html', {'obj': rfm_obj})
    elif request.method == 'POST':
        rfm_obj = RegisterFm(request.POST)
        if rfm_obj.is_valid():
            if rfm_obj.cleaned_data['verify'].upper() == request.session['check_code'].upper():
                user_obj = models.UserInfo(username=rfm_obj.cleaned_data['username'],password=rfm_obj.cleaned_data['password'])
                user_obj.save()
                # 来同步创建用户博客数据表
                models.Blog.objects.create(owner=user_obj)
                return redirect('/login')
            else:return render(request, 'register.html', {'obj': rfm_obj, 'mess': '验证码错误!'})

        else:
            return render(request, 'register.html', {'obj': rfm_obj})



def login(request):
    # if request.method == 'GET':
    login_obj = LoginForms()
    return render(request, 'login.html', {'login_obj':login_obj})




def center(request):
    if request.method == 'GET':
        if request.session.get('is_login', None):
            # 根据session判断用户登陆过没有,登陆过的话直接返回他的信息
            username = request.session['username']
            v = models.UserInfo.objects.filter(username=username).values('blog__header_pic', 'blog__nic_name',
                                                                         'blog__article__aid', 'blog__bid',
                                                                         'blog__article__title',
                                                                         'blog__article__read_count',
                                                                         'blog__article__c_time',)

            return render(request, 'center.html', {'v': v})
        return redirect('/login')

    if request.method == 'POST':
        login_obj = LoginForms(request.POST)
        if login_obj.is_valid():
            # 如何解决验证表单信息在前,验证码信息验证在后的尴尬?
            # 没有login_obj.is_valid()的判断在,后面提取表单信息会报错..
            if login_obj.cleaned_data['verify'].upper() != request.session['check_code'].upper():
                return render(request, 'login.html', {'login_obj': login_obj, 'mess': '验证码错误'})
            username = login_obj.cleaned_data.get('username')
            request.session['username'] = username
            request.session['is_login'] = True
            # 设置session用户名字段,方便后面重新回来时能拿到用户的信息
            # 需要返回到个人中心的内容包括:Blog(header_pic,nic_name) article
            v = models.UserInfo.objects.filter(username=username).values('blog__header_pic', 'blog__nic_name',
                                                                         'blog__article__aid','blog__bid',
                                                                         'blog__article__title',
                                                                         'blog__article__read_count',
                                                                          'blog__article__c_time',)

            return render(request, 'center.html', {'v': v})
            # 反向跨表,通过username属性得到众多相关属性.
        else:
            return render(request, 'login.html', {'login_obj': login_obj})




def logout(request):
    request.session['is_login'] = False
    return redirect('/login')


def test(request):
    p = request.GET.get('p')
    return HttpResponse(p)



def article(request, aid):
    a = models.Article.objects.filter(aid=aid).values('title', 'c_time', 'author_id','read_count', 'author__nic_name',
                                                       'articledetail__content', 'author__owner__username').first()
    if a['author__nic_name'] is None:
        a['author__nic_name'] = a['author__owner__username']
    models.Article.objects.filter(aid=aid).update(read_count=a['read_count'] + 1)
    a['read_count'] += 1
    return render(request, 'article.html', {'a': a})


def add(request):
    res = {'status': True, 'error_mess': None}
    try:
        blog_bid = request.POST.get('bid')
        title = request.POST.get('title').strip()
        content = request.POST.get('content').strip()
        if len(title) == 0 or len(content) == 0:
            res['status'] = False
            res['error_mess'] = '请填写文章标题并撰写内容'
        else:
            obj_a= models.Article(title=title, author_id=blog_bid)
            obj_a.save()
            models.ArticleDetail.objects.create(content=content, article=obj_a)
    except Exception:
        res['status'] = False
        res['error_mess'] = '请求错误'
    data = json.dumps(res)
    return HttpResponse(data)


def delete_article(request):
    aid = request.POST.get('aid')
    models.Article.objects.filter(aid=aid).delete()
    return HttpResponse('s')

def edit_article(request):
    if request.method == 'GET':
        aid = request.GET.get('aid')
        obj = models.Article.objects.get(aid=aid)
        data = obj.articledetail.content
        # 一对一跨表和一对多跨表的不同之处   一对一不能用表名_set的方法
        return HttpResponse(data)
    if request.method == 'POST':
        res = {'status': True, 'error_mess': None}
        try:
            aid = request.POST.get('aid')
            title = request.POST.get('title').strip()
            content = request.POST.get('content').strip()
            if len(title) == 0 or len(content) == 0:
                res['status'] = False
                res['error_mess'] = '文章标题和内容不能为空'
            else:
                models.Article.objects.filter(aid=aid).update(title=title)
                models.ArticleDetail.objects.filter(article_id=aid).update(content=content)
        except Exception as e:
            res['status'] = False
            res['error_mess'] = '请求错误!'
        data = json.dumps(res)
        return HttpResponse(data)


def home_page(request):
    article_list = models.Article.objects.all().order_by('-c_time').values('title', 'read_count', 'aid',
                                                             'author__nic_name','author__owner__username',
                                                              'articledetail__content', 'c_time','author_id')
    for i in article_list:
        if i['author__nic_name'] is None:
            i['author__nic_name'] = i['author__owner__username']
    # 如果没有昵称就用用户名代替昵称

    cur_page = int(request.GET.get('p', 1))
    # 得到当前页

    if divmod(len(article_list), 8)[1] == 0:
        page_sum = len(article_list)//8
    else:
        page_sum = len(article_list)//8 + 1
    temp_list = []
    for i in range(int(page_sum)):
        if i + 1 == cur_page:
            temp = "<a class='cur_page'  href='/?p=%s'> %s </a>" % (i + 1, i + 1)
        else:
            temp = "<a class='not_cur_page' href='/?p=%s'> %s </a>" % (str(i+1), str(i+1))
        temp_list.append(temp)
    page_str = ''.join(temp_list)
    # 得到标签的字符串
    a_info = article_list[8*(cur_page-1):8*cur_page]
    return render(request, 'home_page.html', {'a_info': a_info, 'page_str': page_str })



def blog_view(request, bid):
    article_list = models.Article.objects.filter(author_id=bid).values('title', 'read_count', 'aid',
                                                                       'articledetail__content', 'c_time')

    return render(request, 'blog_view.html', {'article_list': article_list})


def user_setting(request):
    if request.method == 'GET':
        request.session['bid'] = request.GET.get('bid')
        return render(request, 'user_setting.html')
    if request.method == 'POST':
        bid = request.session['bid']
        nic_name = request.POST.get('nicname')
        models.Blog.objects.filter(bid=bid).update(nic_name=nic_name)
    return redirect('/center')