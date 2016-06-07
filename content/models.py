#-*-coding:utf-8-*-
from django.db import models
from django import forms
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser
)
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from  datetime  import  *
from PIL import Image
from StringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class Auth(AbstractUser):
    subscribe = models.IntegerField(default=1)
    head = models.ImageField(upload_to = "covers",blank=True)
    nickname = models.CharField(max_length=50,blank=True)
    sign = models.CharField(max_length=200,blank=True)
    area = models.CharField(max_length=20,blank=True)
    school = models.CharField(max_length=32,blank=True)
    grade = models.CharField(max_length=32,blank=True)
    regist_from =models.IntegerField(default = 0)
    sns_type = models.IntegerField(default = 0)
    sns_uid = models.CharField(max_length=32,blank=True)
    country = models.CharField(max_length=20,blank=True)

    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name = "注册用户"
        verbose_name_plural = "注册用户"


class Blog(models.Model):
    INT_CHOICES=(
        (0,u'审核中'),
        (1,u'审核通过'),
        (2,u'未通过审核文章'),
        (3,u'发布中'),
        (4,u'草稿'),
    )

    INT_NEW_CHOICES=(
        (0,u'后台编辑'),
        (1,u'用户'),
        (2,u'前端特约记者发稿'),
    )

    INT_BLOGPIC=(
        (0,u'普通模式'),
        (1,u'大图模式'),
    )

    INT_RECOMMEND=(
        (0,u'推荐到APP和网站'),
        (1,u'推荐到APP'),
        (2,u'推荐到网站'),
    )

    title = models.CharField(max_length = 256,verbose_name=u'标题')
    cover = models.ImageField(upload_to = "covers",verbose_name=u'图片',default="covers/Desert.jpg")
    thumb = models.ImageField(upload_to = "thumb",verbose_name=u'缩略图',blank=True)
    index = models.ImageField(upload_to = "covers",verbose_name=u'首页图片',blank=True)
    abstract = models.CharField(max_length = 1024,verbose_name=u'文章概要',blank=True)
    content = models.TextField(max_length = 40480,verbose_name=u'')
    author = models.ForeignKey('Auth',verbose_name=u'作者',blank=True,related_name='author_one')
    editor = models.CharField(max_length = 128,verbose_name=u'编辑',blank=True)
    #tag = models.ForeignKey('Tag',verbose_name=u'标签',blank=True,related_name='tag_one')
    #tagmany = models.ManyToManyField('Tag',verbose_name=u'多标签选择',blank=True,related_name='tag_many')
    #category = models.ForeignKey('Category',verbose_name=u'分类',blank=True)
    date = models.DateField(default=datetime.now().date())
    #comment = models.ManyToManyField('Comment', blank=True)
    hotness = models.IntegerField(default=0,verbose_name=u'审核文章',choices = INT_CHOICES)
    new = models.IntegerField(default=0,verbose_name=u'文章作者属性',choices = INT_NEW_CHOICES)
    #authclassify = models.ManyToManyField('AuthClassify', blank=True,verbose_name=u'可推荐的用户')
    praise_count =  models.IntegerField(default=0,verbose_name=u'推荐到',choices = INT_RECOMMEND)
    read_count = models.IntegerField(default=0)
    is_big = models.IntegerField(default=0,verbose_name=u'文章显示大图模式',choices = INT_BLOGPIC)



    def __unicode__(self):
        return self.title




    def get_absolute_url(self):
        return "/blog/%i/" % self.id

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"




class Tag(models.Model):
    name = models.CharField(max_length = 32)
    content = models.CharField(max_length = 100,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"


class Category(models.Model):
    name = models.CharField(max_length = 32)
    cover = models.ImageField(upload_to = "covers",verbose_name=u'图片')
    introduction = models.CharField(max_length = 256)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "专栏"
        verbose_name_plural = "专栏"


class WebBlog(models.Model):
    INT_CHOICES=(
        (0,u'通过审核文章'),
        (1,u'未审核文章'),
        (2,u'未通过审核文章'),
    )

    INT_NEW_CHOICES=(
        (0,u'后台编辑'),
        (1,u'用户'),
        (2,u'前端特约记者发稿'),
    )

    INT_BLOGPIC=(
        (0,u'普通模式'),
        (1,u'大图模式'),
    )

    title = models.CharField(max_length = 256,verbose_name=u'标题')
    cover = models.ImageField(upload_to = "covers",verbose_name=u'图片',default="covers/Desert.jpg")
    thumb = models.ImageField(upload_to = "thumb",verbose_name=u'缩略图',blank=True)
    index = models.ImageField(upload_to = "covers",verbose_name=u'首页图片',blank=True)
    abstract = models.CharField(max_length = 1024,verbose_name=u'文章概要')
    content = models.TextField(max_length = 40480,verbose_name=u'')
    author = models.CharField(max_length = 128,verbose_name=u'作者')
    editor = models.CharField(max_length = 128,verbose_name=u'编辑')
    date = models.DateField(default=datetime.now().date())
    hotness = models.IntegerField(default=0,verbose_name=u'审核文章',choices = INT_CHOICES)
    new = models.IntegerField(default=0,verbose_name=u'文章作者属性',choices = INT_NEW_CHOICES)




    def __unicode__(self):
        return self.title


    class Meta:
        db_table = 'content_blog'
        verbose_name = "文章"
        verbose_name_plural = "文章"


class AppBlog(models.Model):
    INT_CHOICES=(
        (0,u'通过审核文章'),
        (1,u'未审核文章'),
        (2,u'未通过审核文章'),
    )

    INT_BLOGPIC=(
        (0,u'普通模式'),
        (1,u'大图模式'),
    )

    INT_BLOGOUT=(
        (0,u'自有文章'),
        (1,u'外部文章直接连接'),
	    (2,u'外部文章跳转原文'),
    )
    title = models.CharField(max_length = 256,verbose_name=u'标题')
    cover = models.ImageField(upload_to = "covers",verbose_name=u'图片',default="covers/Desert.jpg")
    thumb = models.ImageField(upload_to = "thumb",verbose_name=u'缩略图不用上传',blank=True)
    index_pic = models.ImageField(upload_to = "covers",verbose_name=u'首页图片',blank=True)
    abstract = models.CharField(max_length = 1024,verbose_name=u'文章概要')
    content = models.TextField(max_length = 40480,verbose_name=u'')
    author = models.CharField(max_length = 128,verbose_name=u'作者')
    editor = models.CharField(max_length = 100,verbose_name=u'编辑',blank=True)
    date = models.DateField(default=datetime.now().date())
    hotness = models.IntegerField(default=0,verbose_name=u'审核文章',choices = INT_CHOICES)
    new = models.IntegerField(default=0,verbose_name=u'文章作者,0为后台编辑,1为用户')



    def __unicode__(self):
        return self.title


    def get_absolute_url(self):
        return "/blog/%i/" % self.id

    class Meta:
        db_table = 'content_blog'
        verbose_name = "文章"
        verbose_name_plural = "文章"

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = Auth
        fields = ( 'username', 'password')
        #fields = ( 'email', 'password')

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        cleaned_data['email'] = cleaned_data['username']
        return cleaned_data

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Auth
        fields = ('head','sign','nickname','area')

    def clean(self):
        cleaned_data=super(UserUpdateForm,self).clean()
        return cleaned_data

    def update(self,id):
        user=Auth.objects.get(pk=id)


class BlogBaiduForm(forms.ModelForm):
    class Meta:
        model = Blog
        #fields = ('title','cover','thumb','index','content','tag','category','author')
        #fields = ('title','content','praise_count')
        #widgets = {'content': UEditorWidget( {'imagePath':'uploads/','filePath':'uploads/'}),}
        fields = ('content',)
        widgets = {'content': UEditorWidget( {'imagePath':'uploads/','filePath':'uploads/'}),}

    def __init__(self, *args, **kwargs):
        super(BlogBaiduForm,self).__init__( *args, **kwargs)
        #self.fields['cover'].required = False



