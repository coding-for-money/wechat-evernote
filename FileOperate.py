# encoding: utf-8
import sys, re,os

'''
@author:llj
磁盘文件操作模块
'''
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
class FileOperate:


    # 创建笔记对应的文件夹
    def mkdir(self,path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        # path_vedio = path + '\\vedio';
        # path_pic = path + '\\img'

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            # osmakedirs(path_vedio)
            # osmakedirs(path_pic)
            os.makedirs(path)
            print(path + ' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            # print path + ' 目录已存在'
            return False

    # 创建文本文件 文件名为当天的日期2017-12-19am ， pm这种格式
    def mkfile(self,filename):
     if  os.path.exists(filename):
        pass;
     else:
        fobj=open(filename, 'w')
        fobj.close()
    def genTodaydirName(self,today_title):
        dirName='C:\\wxhistory\\'+today_title;#today_title 是日期加群名
        return dirName;

    # 写记录文件
    def updatefile(self,txtname,msgcontet):
        try:
            fobj = open(txtname, 'a')  # 这里的a意思是追加，这样在加了之后就不会覆盖掉源文件中的内容，如果是w则会覆盖。
            fobj.write('\n')
            fobj.write(str(msgcontet.encode('utf-8').strip()))
            # fobj.write(b"\n"+ msgcontet.encode('utf-8'))  # 这里的\n的意思是在源文件末尾换行，即新加内容另起一行插入。
            fobj.close()  # 特别注意文件操作完毕后要close
        except IOError:
            print('*** file open error:')

    # # 定义要创建的目录
    # mkpath = "d:\\qttc\\web\\"
    # # 调用函数
    # mkdir(mkpath)




    def remove_emoji(self,text):
        emoji_pattern = re.compile(
            u"(\ud83d[\ude00-\ude4f])|"  # emoticons
            u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
            u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
            u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
            u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
            "+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
if __name__ == '__main__':
 fo = FileOperate();
 fo.createXml;