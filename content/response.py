#-*-coding:utf-8-*-
import sys
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('UTF-8')
from utils import *
from models import *
import datetime
import re

def handle_text(req_msg):
    text = req_msg['Content']

    if re.match(ur'^(\d+)(\.|月)(\d+)$', text):
        m = re.search(ur'^(\d+)(\.|月)(\d+)$', text)
        month, day = m.group(1), m.group(3)
        year = str(datetime.datetime.now().year)
        if int(month) < 12 and int(day) <= 31:
            date = datetime.datetime.strptime(month+date+year, "%m%d%Y").date()
        blogs = Blog.objects.filter(date = date)
        bucket = []
        for blog in blogs:
            bucket.add([blog.title ,
                        'www.collegedaily.cc'+blog.get_absolute_url()])
        return makeImageMsg(req_msg, bucket)
    else:
        return makeTextMessage(req_msg, u'欢迎订阅北美留学生日报')

def handle_image(req_msg):
    pass

def handle_link(req_msg):
    pass

