#encoding: utf-8
import os
import re
import shutil
import sys
import time

import itchat
from itchat.content import *

from FileOperate import FileOperate

'''
@author:llj
项目模块1：
保存微信聊天记录到本地
一天一个文件夹 文件夹包含存放附件的resources文件夹以及一个聊天记录文本 
文本内容以enml的格式进行存放，对于其中的附件类型的内容，将以特定的标识标识出来，
在上传到笔记的时候， 将对应的标记切换成笔记中的标签， 同时整个文件全部上传进去，
目前不考虑一个笔记的大小问题(因为单个笔记最大200m， 对于一个群一天能造成的大小，我觉得应该不会超过200m)
日期：2018年1月1日 增加功能
当微课群中拦截到指定老师的启动微课指令后， 将发言信息转发出去
当拦截到下课指令后，终止群发功能
该功能只是在一段时间内运行，可以考虑用线程的方式， 启动和停止线程进行，或者，通过变量的方式，
在发出上课指令后，该变量变化，用于后续判断，发出下课指令，恢复变量

'''
fo=None;
styleNcStart='<span style="color:red;">'
styleNcEnd='</span>'
# 当天存放路径
RootPath = os.path.join('C:\\', 'wxhistory')
# 文档存放路径 包含压缩包
DocPath = 'doc'
# 动态图存放路径
GifPath = 'gif'
# 图片存放路径
ImgPath = 'img'
# 小视屏存放路径
Mp4Path = 'mp4'
# 语音存放路径
Mp3Path = 'mp3'
# 处理完后挪至该路径
RootPath_History = os.path.join('C:\\', 'wxhistory_history')

def parseMsgAtt(msg_content, noteName, sendUsername, timenow):
    filename = os.path.basename(msg_content)
    filename = filename.encode()
    fileExtension = file_extension(filename)
    print(fileExtension)
    filename=filename.decode();
    filedir = ''
    if '.gif' in fileExtension.lower():
        filedir = '\\resources\\' + GifPath + '\\' + sendUsername + filename
    elif '.mp4' in fileExtension.lower():
        filedir = '\\resources\\' + Mp4Path + '\\' + sendUsername + filename
    elif '.mp3' in fileExtension.lower():
        filedir = '\\resources\\' + Mp3Path + '\\' + sendUsername + filename
    elif '.doc' in fileExtension.lower():
        filedir = '\\resources\\' + DocPath + '\\' + sendUsername + filename
    elif '.txt' in fileExtension.lower():
        filedir = '\\resources\\' + DocPath + '\\' + sendUsername + filename
    elif '.pdf' in fileExtension.lower():
        filedir = '\\resources\\' + DocPath + '\\' + sendUsername + filename
    elif '.docx' in fileExtension.lower():
        filedir = '\\resources\\' + DocPath + '\\' + sendUsername + filename
    elif '.xls' in fileExtension.lower():
        filedir = '\\resources\\' + DocPath + '\\' + sendUsername + filename
    elif '.xlsx' in fileExtension.lower():
        filedir = '\\resources\\' + DocPath + '\\' + sendUsername + filename
    elif '.ppt' in fileExtension.lower():
        filedir = '\\resources\\' + DocPath + '\\' + sendUsername + filename
    elif '.pptx' in fileExtension.lower():
        filedir = '\\resources\\' + DocPath + '\\' + sendUsername + filename
    elif '.zip' in fileExtension.lower():
        filedir = '\\resources\\' + DocPath + '\\' + sendUsername + filename
    elif '.rar' in fileExtension.lower():
        filedir = '\\resources\\' + DocPath + '\\' + sendUsername + filename
    else:
        filedir = '\\resources\\' + ImgPath + '\\' + sendUsername + filename
    destDir = fo.genTodaydirName(timenow + '\\' + noteName) + filedir
    print(destDir)
    shutil.move(filename, destDir);
    msg_content = styleNcStart + sendUsername + styleNcEnd + ':' + 'attachmentFlag:'  + filedir;
    return msg_content


def file_extension(filename):
    file_extension = os.path.splitext(filename)[1]
    return file_extension.decode();


#创建笔记本对应的目录结构和unicodename.txt
def gen_unicodename(timenow, today_title_dir,chatroom):
    today_dir=fo.genTodaydirName(timenow)#
    fo.mkdir(today_dir);
    # 创建今天目录下的unicodename.txt用于保存每个文件夹
    if not os.path.exists(today_title_dir):
        fo.mkdir(today_title_dir)
        if not os.path.exists(os.path.join(today_dir, 'unicodename.txt')):
            fo.mkfile(os.path.join(today_dir, 'unicodename.txt'))
        fo.updatefile(os.path.join(today_dir, 'unicodename.txt'), chatroom)
        if not os.path.exists( today_title_dir+'\\resources'):
            fo.mkdir(today_title_dir + '\\resources');
        if not os.path.exists( today_title_dir+'\\resources\\'+DocPath):
            fo.mkdir( today_title_dir+'\\resources\\'+DocPath);
        if not os.path.exists( today_title_dir+'\\resources\\'+GifPath):
            fo.mkdir( today_title_dir+'\\resources\\'+GifPath);
        if not os.path.exists(today_title_dir +'\\resources\\' + ImgPath):
            fo.mkdir( today_title_dir+'\\resources\\'+ImgPath);
        if not os.path.exists(today_title_dir +'\\resources\\' + Mp4Path):
            fo.mkdir( today_title_dir+'\\resources\\'+Mp4Path);
        if not os.path.exists(today_title_dir +'\\resources\\' + Mp3Path):
            fo.mkdir( today_title_dir+'\\resources\\'+Mp3Path);




@itchat.msg_register(['Text', 'Note', 'Picture', 'Attachment', 'Card', 'Video','Recording','Sharing'], isFriendChat=False,
                     isGroupChat=True,
                     isMpChat=True)
def print_content(msg):
    chatroom_id = msg['FromUserName']
    # 群名 部分群名含有emoji码， 保存到磁盘的时候 默认格式保存，不需要特意编码
    chatroom_name = msg['User']['NickName'];
    #为了合理保存文件， 去掉emoji 缺点：有的群就是用emoji来区分的，这样做就没法区分不同的群了
    # chatroom_name=fo.remove_emoji(chatroom_name)
    # 发送者的昵称 群内名称
    sendUsername = msg['ActualNickName']
    # sendUserNickname=msg['NickName']
    # 真实名称ID
    username_id = msg['ActualUserName']
    timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()));
    # 验证是否已经创建当天的笔记
    noteName = timenow + chatroom_name;
    today_title_dir=fo.genTodaydirName(timenow+'\\'+noteName);#绝对路径
    gen_unicodename(timenow, today_title_dir,chatroom_name)
    txtname = today_title_dir + '\\' + noteName + ".txt"
    fo.mkfile(txtname)




    if msg['Type'] == 'Text' or msg['Type'] == 'Friends':
        msg_content = styleNcStart+sendUsername+styleNcEnd + ':' + msg['Text'];
        msg_content=msg_content.replace('&','&amp;');
        # 如果发送的消息是附件、视屏、图片、语音
    elif msg['Type'] == "Attachment" or msg['Type'] == "Video" or msg['Type'] == 'Picture' or msg[
        'Type'] == 'Recording':
        msg_content = msg['FileName']  # 内容就是他们的文件名
        msg['Text'](str(msg_content))  # 下载文件
        # filename = os.path.basename(msg_content)
        # shutil.move(filename, fo.genTodaydirName(timenow+'\\'+noteName)+'\\resources\\'+filename);
        # msg_content=styleNcStart+sendUsername+styleNcEnd + ':' +'attachmentFlag:'+filename;
        msg_content = parseMsgAtt(msg_content, noteName, sendUsername, timenow)

    elif msg['Type'] == 'Card':  # 如果消息是推荐的名片
        msg_content = msg['RecommendInfo']['NickName'] + '的名片'  # 内容就是推荐人的昵称和性别
    elif msg['Type'] == 'Map':  # 如果消息为分享的位置信息
        x, y, location = re.search(
            "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()  # 内容为详细的地址
        else:
            msg_content = r"" + location
    elif msg['Type'] == 'Sharing':  # 如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
        msg_content = styleNcStart+sendUsername+styleNcEnd + ':<a href="'+msg['Url']+'">' + msg['Text']+'</a>';
        msg_content += '<br />'
    else:
        msg_content=msg['Text']
    print(msg_content)
    fo.updatefile(txtname,msg_content)#txtname为绝对路径
   #……………………
    chatroom_id = msg['ToUserName']

    # 发送者的昵称
    username = msg['ActualNickName']

    # 消息并不是来自于需要同步的群
    if not chatroom_id in chatroom_ids:
        return

        # 根据消息类型转发至其他需要同步消息的群聊
    if msg['Type'] == TEXT:
        for item in chatrooms:
            if not item['UserName'] == chatroom_id:
                if '测试' in item['NickName']:
                    print('找到')
                    itchat.send('%s\n%s' % (username, msg['Content']), item['UserName'])
    elif msg['Type'] == SHARING:
        for item in chatrooms:
            if not item['UserName'] == chatroom_id:
                if '测试' in item['NickName']:
                    itchat.send('%s\n%s\n%s' % (username, msg['Text'], msg['Url']), item['UserName'])
    else :
        # 如果为gif图片则不转发
        if msg['FileName'][-4:] == '.gif':
            return
        # 下载图片等文件
        msg['Text'](msg['FileName'])
        # 转发至其他需要同步消息的群聊
        for item in chatrooms:
            if not item['UserName'] == chatroom_id:
                if '测试' in item['NickName']:
                    print('找到')
                    # itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']),
                    itchat.send( msg['Content'],
                                item['UserName'])
                    # itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'],
                    #                                                                                  'fil'),
                    #                         msg['FileName']),
                    #             item['UserName'])
   #…………………………

if __name__ == '__main__':
 fo = FileOperate();
 itchat.auto_login(hotReload=True)
 # 获取所有通讯录中的群聊
 # 需要在微信中将需要同步的群聊都保存至通讯录
 chatrooms = itchat.get_chatrooms(update=True, contactOnly=True)
 chatroom_ids = [c['UserName'] for c in chatrooms]
 for c in chatrooms:
     if '微课' in c['NickName']:
         chatroom_ids = [c['UserName']]
 itchat.run()
 print_content;
