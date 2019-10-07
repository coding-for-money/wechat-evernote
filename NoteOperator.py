# coding=utf-8
import sys, hashlib, re, time,mimetypes,os
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.NoteStore as NoteStore
import chardet
import Client_Production
'''
@author:llj
笔记本操作模块
'''
reload(sys)
sys.setdefaultencoding('utf8')

class NoteOperator:
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
    flagPos = 0
    def remove_emoji(self,text):
        emoji_pattern = re.compile(
            u"(\ud83d[\ude00-\ude4f])|"  # emoticons
            u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
            u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
            u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
            u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
            "+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
    # 创建笔记本
    def createNotebook(self,notebookname):
        noteStore=Client_Production.noteStore;
        notebook = Types.Notebook();
        notebook.name=notebookname;
        projectnotebookname='AllianceHero'
        notebook.stack=projectnotebookname
        # 搜索是否已经存在笔记本
        notebooks=noteStore.listNotebooks(Client_Production.token)
        isexistnotebook=False
        for nb in notebooks:
            if nb.name==notebookname:
                isexistnotebook=True
                notebook=nb
        # notebook.
        # note.notebookGuid = Client_Production.PROJECT_NOTES_GUID;
        if not isexistnotebook:
         notebook=noteStore.createNotebook(Client_Production.token,notebook);
        return notebook
    # 必须保证notename无乱码
    def createNote(self,notebook,notename):
        isexist = False;  # 是否存在当天的笔记  目前认为不可能存在当天的笔记， 如果有一定要删除
        noteStore = Client_Production.client.get_note_store();
        NOTE_SUFFIX = '</en-note>';
        NOTE_HEADER = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">';
        f = NoteStore.NoteFilter()

        msg_content='<en-note>';
        #根据路径，得到txt
        notetxtpath=self.RootPath+'/'+notebook.name+'/'+notebook.name+notename+"/"+notebook.name+notename+'.txt'
        # notetxtpath=notetxtpath.encode()
        print(notetxtpath)
        if os.path.exists(notetxtpath.decode('utf-8')):
            txtobj=open(notetxtpath.decode('utf-8'),'rb');
            flag = 'attachmentFlag:'
            if txtobj:
                resources = []
                for line in open(notetxtpath.decode('utf-8')):
                    line = line.strip('\n')
                    isattach = flag in line
                    # 读取的内容，如果包含attachmentFlag： 截取后面的内容
                    if isattach:
                        flagPos = line.index(flag)
                        filename = line[flagPos + len(flag):]
                        data = Types.Data()
                        filepath = self.RootPath + '/' + notebook.name + '/' +  notebook.name+notename + filename;
                        #
                        filename = os.path.basename(filepath.encode('utf-8'))
                        data = Types.Data()
                        # try:
                        # 必须保证文件名在生成的时候是gbk， 在读取的时候也是gbk , 没有在linux测试过
                        # print(os.path.exists(filepath.decode('utf-8')))
                        # D:\wxhistory\2017 - 12 - 29\2017 - 12 - 29【联盟家长微课：郭宛灵微课\resources\mp4
                        # 因为抬头已经用utf-8作为编码，open要求传入的path必须是unicode
                        if os.path.exists(filepath.decode('utf-8')):
                            data.body = open(filepath.decode('utf-8'), 'rb').read()
                            data.size = len(data.body)
                            data.bodyHash = hashlib.md5(data.body).hexdigest()
                            resource = Types.Resource()
                            resource.mime = mimetypes.guess_type(filename)[0]
                            resource.data = data
                            attr = Types.ResourceAttributes()
                            attr.fileName = filename
                            resource.attributes = attr
                            hexhash = resource.data.bodyHash
                            # gif肯定是表情符号，限制大小以免影响到阅读
                            minetype = resource.mime
                            msg_content += line[0:flagPos] + '<br />'
                            if ('gif' in minetype):
                                msg_content += "<div style='max-width:20px;max-height:20px'><en-media  type=\"%s\" " \
                                               "hash=\"%s\" /><br /></div>" % \
                                               (resource.mime, hexhash);
                            else:
                                msg_content += "<en-media  type=\"%s\" hash=\"%s\" /><br " \
                                               "/>" % \
                                               (resource.mime, hexhash);
                            # 昵称 默认红色显示
                            resources.append(resource)

                    else:
                        # p = re.compile(r'([\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f])')
                        result, number =re.subn("[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]", "",line)
                        # msg_content += line.decode().encode() + '<br />'
                        msg_content += result + '<br />'
            note = Types.Note();
            note.notebookGuid = notebook.guid
            note.title = notename.encode()
            note.content = NOTE_HEADER;
            #过滤非法字符
            print("过滤前：");
            print(msg_content)
            msg_content=re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+",u"",msg_content);
            errhref='<a href=""></a>';
            msg_content=msg_content.replace(errhref,'#爬虫过滤错误信息#')
            note.content += msg_content.encode('utf-8')
            note.content += NOTE_SUFFIX
            note.resources = resources
            print("过滤后：")
            print(note.content)
            print('将要创建' +notebook.name+'//'+ notename)
            note = noteStore.createNote(Client_Production.token, note);
            print('创建完成')
        else:
            return


            # shutil.move(notename, rootpath_history)
# if __name__ == '__main__':
#  e  = NoteOperator();
#  e.createNotebook('testtest5');



