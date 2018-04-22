from django.db import models


# Create your models here.


class UserInfo(models.Model):
    def __str__(self):
        return self.username
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=12)


class Blog(models.Model):
    def __str__(self):
        if self.nic_name:
            return self.nic_name
        else:
            return self.owner.username
    bid = models.AutoField(primary_key=True)
    header_pic = models.BinaryField(null=True)
    nic_name = models.CharField(max_length=25, null=True)
    owner = models.OneToOneField(to='UserInfo', to_field='uid')


class ArticleDetail(models.Model):
    def __str__(self):
        return self.article.title
    content = models.CharField(max_length=5000)
    article = models.OneToOneField(to='Article', to_field='aid')


class Article(models.Model):
    def __str__(self):
        return self.title
    aid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    read_count = models.IntegerField(default=0)
    c_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to='Blog', to_field='bid')



