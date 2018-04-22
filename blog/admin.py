from django.contrib import admin
from .models import UserInfo, Article, ArticleDetail, Blog
# Register your models here.
admin.site.register([UserInfo, ArticleDetail, Article, Blog])