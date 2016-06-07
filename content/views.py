#-*- coding:utf-8 -*-
import datetime
from django.shortcuts import render, redirect, render_to_response
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse
from models import *
from django.http import HttpResponseRedirect
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder
from PIL import Image
from StringIO import StringIO
from django.template import loader, RequestContext



def reset(req):
    if req.method=='GET':
        return render_to_response('reset.html')

def app(req):
    if req.method=='GET':
        return render_to_response('app.html')



@login_required(login_url="/")
def center(req):
    if req.method=='GET':
        blogs = Blog.objects.filter(author = req.user.pk).exclude(hotness = 4).order_by('-date')
        drafts = Blog.objects.filter(author = req.user.pk,hotness = 4).order_by('-date')
        return render_to_response('personal_center.html',RequestContext(req,{'blogs':blogs,'drafts':drafts}))

@login_required(login_url="/")
def mess(req):
    if req.method=='GET':
        drafts = Blog.objects.filter(author = req.user.pk,hotness = 4).order_by('-date')
        return render_to_response('personal_mess.html',RequestContext(req,{'drafts':drafts,}))

@login_required(login_url="/")
def publish(req):
    if req.method=='GET':
        form = BlogBaiduForm()
        return render_to_response('personal_write.html',RequestContext(req,{'form':form}))
    elif req.method=='POST':
        response_data = {}
        response_data['ret_code'] = 0
        content = req.POST.get("content",None)
        title = req.POST.get("title",None)
        issue = req.POST.get("issue",None)
        addr = req.POST.get("addr",None)
        cate = Category.objects.all()[0]
        blog = Blog()
        blog.author = req.user
        blog.content = content
        blog.title = title
        blog.abstract = title
        blog.category = cate
        blog.new = 2
        blog.hotness = issue
        blog.praise_count = addr
        blog.save()
        if issue != 4:
            webblog = WebBlog()
            appblog = AppBlog()
            webblog.title   = appblog.title = title
            webblog.content = appblog.content = content
            webblog.author  = appblog.author = req.user.email
            webblog.editor  = appblog.editor = req.user.email
            webblog.abstract  = appblog.abstract = title
            webblog.hotness  = appblog.hotness = 1
            if addr == 0:
                webblog.save(using='web')
                appblog.save(using='app')
            if addr == 1:
                appblog.save(using='app')
            if addr == 2:
                webblog.save(using='web')

        response_data['ret_msg'] = blog.pk
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/")
def editblog(req,bid):
    if req.method=='GET':
        blog_count = len(Blog.objects.filter(author = req.user.pk))
        blog = Blog.objects.get(pk = bid)
        return render_to_response('personal_edit.html',RequestContext(req,{'blog_count':blog_count,'blog':blog}))
    elif req.method=='POST':
        response_data = {}
        response_data['ret_code'] = 0
        content = req.POST.get("content",None)
        title = req.POST.get("title",None)
        issue = req.POST.get("issue",None)
        addr = req.POST.get("addr",None)
        #cate = Category.objects.all()[0]
        blog = Blog.objects.filter(pk=bid)
        blog.update(title=title,content=content,hotness=issue,praise_count=addr)
        #blog.save()
        response_data['ret_msg'] = bid
        if issue != '4':
            webblog = WebBlog()
            appblog = AppBlog()
            webblog.title   = appblog.title = title
            webblog.content = appblog.content = content
            webblog.author  = appblog.author = req.user.email
            webblog.editor  = appblog.editor = req.user.email
            webblog.abstract  = appblog.abstract = title
            webblog.hotness  = appblog.hotness = 1
            if addr == '0':
                webblog.save(using='web')
                appblog.save(using='app')
            if addr == '1':
                appblog.save(using='app')
            if addr == '2':
                webblog.save(using='web')
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/")
def deleteblog(req,bid):
    if req.method=='GET':
        blog = Blog.objects.get(pk=bid)
        if blog.author == req.user:
            blog.delete()
        return redirect('/center/')




def index(req):
    if req.method == 'GET':
        if req.user.is_authenticated():
            return redirect('/center/')
        return render_to_response('index.html')

def protocol(req):
    if req.method == 'GET':
        return render_to_response('protocol.html')


def blog(req, bid):
    if req.method == 'GET':
        blog = Blog.objects.get(pk = bid)
        return render_to_response('blog.html', RequestContext(req,
            {'blog':blog}))


def signin(req):
    if req.method == 'POST':
        try:
            logintype = req.POST.get('type', '0')
        except:
            logintype = '0'
        username = req.POST.get('username', None)
        print username
        password = req.POST.get('password', None)
        print password
        user = authenticate(username=username,password=password,email=username)
        response_data = {}
        if user is not None:
            if user.is_active:
                #LOGIN 用户
                login(req, user)
                response_data['ret_code'] = 0
                response_data['ret_msg'] = 'sucess'
                if logintype == '0':
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                error = '用户已被禁用'
                response_data['ret_code'] = 1
                response_data['ret_msg'] = error
                if logintype == '0':
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
        error = '用户名/密码 错误'
        response_data['ret_code'] = 1
        response_data['ret_msg'] = error
        print response_data['ret_msg']
        if logintype == '0':
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    elif req.method == 'GET':
        return render_to_response('login.html', RequestContext(req, {'next':req.GET.get('next', '/')}))

def signup(req):
    if req.method == 'POST':
        try:
            logintype = req.POST.get('type','0')
        except:
            logintype = '0'
        response_data = {}
        if (not req.POST.get('username',None)) or (not req.POST.get('password',None)):
            error = '用户名和密码不能为空'
            response_data['ret_code'] = 1
            response_data['ret_msg'] = error
            if logintype == '0':
                return HttpResponse(json.dumps(response_data), content_type="application/json")

        try:
            form = UserRegisterForm(req.POST)
            form.is_valid()
            form.save()
            username = form.cleaned_data['username']
            #print username
            email=form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password,email=email)
            login(req, user)
            response_data['ret_code'] = 0
            response_data['ret_msg'] = "sucess"
            if logintype == '0':
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                return redirect('/')
        except Exception,e:
            print Exception,':',e
            error = '邮箱已经被使用'
            response_data['ret_code'] = 1
            response_data['ret_msg'] = error
            if logintype == '0':
                return HttpResponse(json.dumps(response_data), content_type="application/json")


    elif req.method == 'GET':
        return render_to_response('signup.html', RequestContext(req, {'next':req.GET.get('next', '/')}))

def signout(req):
    logout(req)
    return HttpResponseRedirect('/')

@login_required(login_url="/")
def updatenickname(req):
    if req.method == 'POST':
        response_data = {}
        try:
            nickname = req.POST.get('name',None)
        except:
            nickname = None
        if nickname is None:
            response_data['ret_code'] = 1
            response_data['ret_msg'] = "昵称不能为空"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        auth = Auth.objects.filter(pk=req.user.pk)
        auth.update(nickname = nickname,)
        response_data['ret_code'] = 0
        response_data['ret_msg'] = "sucess"
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/")
def updatehead(req):
    if req.method == 'POST':
        user = Auth.objects.get(pk  =req.user.pk)
        response_data = {}
        try:
            user.head = req.FILES['Filedata']
            user.save()
        except:
            response_data['ret_code'] = 1
            response_data['ret_msg'] = "头像获取失败"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        response_data['ret_code'] = 0
        response_data['ret_msg'] = user.head.url
        return HttpResponse(json.dumps(response_data), content_type="application/json")
