# -*- coding=UTF-8 -*-
import sys
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('UTF-8')
import xml.etree.ElementTree as ET
import time
import datetime
from haystack.utils import Highlighter
import daily.settings

class DailyHighlighter(Highlighter):
    def render_html(self, highlight_locations=None, start_offset=None, end_offset=None):
        # highlighted_chunk = self.text_block[start_offset:end_offset]
        highlighted = self.text_block[0:]
        for word in self.query_words:
             highlighted = highlighted.replace(word,
                    "<span class='color-green'>%s</span>" % word )
        return highlighted

def parseXml(req):
    xml_tree = ET.fromstring(req.body)
    content = dict()
    for i in xml_tree:
        content[i.tag] = i.text
    return content

def makeXml(dic, root_tag = 'xml'):
    xml_tree = ET.Element(root_tag)
    def _make_node(root, key, val):
        if type(val) == ET.Element:
            root.append(val)
            return
        node = ET.SubElement(root, key)
        if type(val) == str or type(val) == unicode:
            node.text = val
        elif type(val) == dict:
            for i in val:
                _make_node(node, i, val[i])
    for i in dic:
        _make_node(xml_tree, i, dic[i])
    return xml_tree

def makeMsg(req_msg, dic):
    dic.update({
        'ToUserName': req_msg['FromUserName'],
        'FromUserName': req_msg['ToUserName'],
        'CreateTime': str(int(time.time())),
        'FuncFlag': '0',
        })
    return ET.tostring(makeXml(dic), 'utf8')

def makeTextMsg(req_msg, text):
    return makeMsg(req_msg, {
        'MsgType': 'text',
        'Content': text,
        })

def makeMusicMsg(req_msg, url, hqurl = None):
    return makeMsg(req_msg, {
        'MsgType': 'music',
        'MusicUrl': url,
        'HQMusicUrl': hqurl if hqurl else url,
        })

def makeImageMsg(req_msg, images):
    # images := ((picurl, title, desc, url), ...)
    articles = ET.Element('Articles')
    for i in images:
        articles.append(makeXml({
            #'PicUrl': i[0],
            'Title': i[0],
            #'Description': i[1],
            'Url': i[1]}, 'item'))
    return makeMsg(req_msg, {
        'MsgType': 'news',
        'ArticleCount': str(len(images)),
        'Articles': articles,
        })

import requests
def send_simple_message(mailgroup,title,html):
    return requests.post(
        "https://api.mailgun.net/v3/mg.cfyr.org/messages",
        auth=("api", "key-fd03a92639b5aafc2657e7264dcf60b6"),
        data={"from": "北美留学生日报 <postmaster@mg.cfyr.org>",
             #"from": "北美留学生日报 <postmaster@sandbox023bb1a3c5e84a069b3bc7ac25824027.mailgun.org>",
              #"to" : "postmaster@sandbox023bb1a3c5e84a069b3bc7ac25824027.mailgun.org",
              #"to" : "test@sandbox023bb1a3c5e84a069b3bc7ac25824027.mailgun.org",
              "to" : "test@mg.cfyr.org",
              #"bcc": mailgroup,
              "subject": title,
              "html": html})

#TODO 消息中有多图如何实现
def makeItemMsg(req_msg, item):
    name = getattr(item, 'name')
    return makeImageMsg(req_msg, (('#', 'test_title', 'test_description', '#')))



