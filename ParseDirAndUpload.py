#encoding:utf-8
import shutil
from NoteOperator import NoteOperator
import time,datetime
import os,sys
import chardet
'''
@author:llj
项目模块2：
解析模块1生成的历史文件，
上传至印象笔记。
参数 h，m表示 每天的h时m分（24小时制）
即每天h:m执行一次定时任务
'''
reload(sys)
sys.setdefaultencoding('utf-8')
h=23
m=55
# 当天存放路径
RootPath = os.path.join('C:\\', 'wxhistory')
# 文档存放路径 包含压缩包
DocPath = 'doc'
# 动态图存放路径
GifPath = 'gif'
# 图片存放路径
ImgPaht = 'img'
# 小视屏存放路径
Mp4Path = 'mp4'
# 语音存放路径
Mp3Path = 'mp3'
# 处理完后挪至该路径
RootPath_History = os.path.join('C:\\', 'wxhistory_history')
class ParseDirAndUpload:

    def __init__(self):
        print('启动')
    def task(self):
        noteOperator = NoteOperator();
        rootpath_history = "C:\\wxhistory_history"
        #读取指定的目录D:\\wxhistory\\  获取该目录下的所有的文件夹
        # rootpath="D:\\wxhistory"
        daysList = os.listdir(RootPath);
        timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()));
        print(daysList)
        if(daysList):
            for everDayDir in daysList:
                print(everDayDir)
                print(timenow)
                if(everDayDir!=timenow):
                    # 从得到的数组中选择昨天（任务在当天0点执行，这时候应该没有人聊天了）的文件,遍历改文件夹-->在印象笔记中创建notebooks（名字为日期名字） ,
                    notebook=noteOperator.createNotebook(everDayDir);
                    # 需要再次遍历目录里的文件夹，获取归类对话后的文件夹
                    daypath=os.path.join(RootPath,everDayDir);#拼合对应的路径 日期
                    print(daypath)
                    # daypathDir=os.listdir(daypath)#精确到每个聊天窗口  编码混乱 日期文件夹下面的列表
                    # 不打算用listdir了，改为在各自的文件夹下面用一个txt存放对应的文件目录名
                    unicodenamepath=os.path.join(daypath,'unicodename.txt');
                    if os.path.exists(unicodenamepath):
                     for line in open(unicodenamepath, 'rb'):
                         noteName = line.strip('\n')
                         noteName = noteName.strip('\r')
                    # for noteName in daypathDir:
                    #     print(unicode(noteName,'gb2312'))
                        # noteName=noteName.decode('gbk')#解决中文乱码 这么做会将表情符变成？
                        # noteName=line.decode().encode()
                        #日期文件夹下面的子文件夹，每个文件夹为一个note  , 将msgtxt里的文本信息中的附件类型的内容进行整理，切换对应的en-note,并upload对应的resource
                         if noteName:
                             noteOperator.createNote(notebook,noteName)
                         #生成后，移动目录文件到历史文件夹 ，为了一致性， 移动的是日期目录

                         # 判断是否已经存在文件夹，如果存在文件夹，需要挪走
                     if(os.path.exists(os.path.join(RootPath_History,everDayDir))):
                       print("已经存在文件夹，建议手工处理"+os.path.join(RootPath_History,everDayDir))
                     else:
                        print('移动'+os.path.join(RootPath,everDayDir));
                        shutil.move(os.path.join(RootPath,everDayDir),RootPath_History);
            daysList = os.listdir(RootPath);
            if daysList:
                for dir in daysList:
                    print('没移动成功'+dir)
if __name__ == '__main__':
    e=ParseDirAndUpload()
    e.task()
    while True:
        now=datetime.datetime.now()
        if now.hour==2 and now.minute==28:
            e.task()
            time.sleep(60)#暂停1分钟，以避免还没完成
            print('执行完成')
        else:
         time.sleep(20)
