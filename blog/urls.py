from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    url(r'login', views.login),
    url(r'register', views.register),
    url(r'check_code', views.check_cd),
    url(r'article/(\d+)', views.article),
    url(r'test', views.test),
    url(r'center', views.center),
    url(r'logout', views.logout),
    url(r'delete', views.delete_article),
    url(r'add', views.add),
    url(r'edit', views.edit_article),
    url(r'blog_view/(\d+)', views.blog_view),
    url(r'setting', views.user_setting),
]