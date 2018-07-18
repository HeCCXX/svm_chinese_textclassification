#-*- coding=gbk -*-
import jieba
import jieba.analyse
import os
#读取每个文件中txt的全路径
def readfullnames(file_name):
    fullname_list=[]
    #遍历文件夹
    m=os.listdir(file_name)
    #print(m)
    for dir in os.listdir(file_name):
        print(dir)
        for filename in os.listdir(file_name+"\\"+dir):
            #print(filename)

            fullname=file_name+"\\"+dir+"\\"+filename
            #print(fullname)
            # 将文件夹中文本路径添加到列表
            fullname_list.append(fullname)
    return fullname_list
# def readfullnames():
#     fullname_list=[]
#     m=os.listdir('./文本分类语料库')
#     #print(m)
#     for dir in os.listdir('./文本分类语料库'):
#         print(dir)
#         for filename in os.listdir('./文本分类语料库'+"\\"+dir):
#             #print(filename)
#             fullname='./文本分类语料库'+"\\"+dir+"\\"+filename
#
#             fullname_list.append(fullname)
#     return fullname_list
#读取每个文件中的字典路径
def readfillnames():
    fillname_list=[]
    for dir in os.listdir("./解词"):
        fillname="./解词\\"+dir+'\\'+dir+'.txt'
        if 'txt.txt' not in fillname:
            fillname_list.append(fillname)
    return fillname_list
#读取每个文件中的词频字典路径
def readcipin_fullnames():
    fillname_list=[]
    for dir in os.listdir("./解词"):
        fillname="./解词\\"+dir+"\\词频"+dir+".txt"
        if 'txt.txt' not in fillname:
            fillname_list.append(fillname)
    return fillname_list
#读取停用词表
def read_stopwords():
    stopwords_list=[]
    f1=open('./stopword.txt','r',encoding='gb18030')
    for line in f1.readlines():
        line=line.strip()
        stopwords_list.append(line)
    return stopwords_list
#写进文件方法，参数对应的文件和字典
def write_words(words_dic,dfs):
    for k in words_dic.items():
        st=''.join(['%s : %s' %k])
        dfs.write(st)
        dfs.write('\n')
#txt 进行分词，统计词频，将类的总字典和词频字典写入每个类中，保存为txt
#统计每个文章中的词在多少篇文章中出现，保存到***。txt
def segfile(fullname_list):
    all_stopwords_list=read_stopwords()
    words_dic={}
    all_words={}
    name_temp='历史'
    for fullname in fullname_list:
        dfs=open("./解词\\"+name_temp+'\\'+name_temp+'.txt','w',encoding='gb18030')    #***.txt
        ddfs=open("./解词\\"+name_temp+'\\词频'+name_temp+'.txt','w',encoding='gb18030')   #词频***.txt
        dirname=fullname.split("/文本分类语料库\\")[1].split('\\')[0]
        if name_temp!=dirname:
            write_words(words_dic,dfs)
            write_words(all_words,ddfs)
            words_dic.clear()
            all_words.clear()
            name_temp=dirname
        filename=fullname.split('\\')[-1]
        print(fullname+"==============")
        ifs=open(fullname,'r',encoding='gb18030',errors='ignore')     #文本分类语料库中每个类中的txt
        ofs=open('./解词\\'+dirname+'\\'+filename,'w',encoding='gb18030')     #分词处理后的文件写入txt
        words_tmp=[]
        for line in ifs.readlines():
            line=line.strip()
            try:
                #进行关键词模式分词
                words = jieba.cut_for_search(line)
            except:
                continue
            for w in words:
                if w.strip()=='':
                    continue
                #过滤停用词
                if w in all_stopwords_list:
                    continue
                #过滤数字类型
                if w.isdigit():
                    continue
                if w not in words_tmp:
                    words_tmp.append(w)
                #统计词频，后续类词频统计
                if w not in all_words.keys():
                    all_words[w]=1
                else:
                    all_words[w]+=1
                #print(w)
                ofs.write(w+' ')
            ofs.write('\n')
        for t in words_tmp:
            if t not in words_dic.keys():
                words_dic[t]=1
            else:
                words_dic[t]+=1
        ifs.close()
        ofs.close()
        dfs.close()
        ddfs.close()
    dfs= open('./解词\\'+name_temp+'\\'+name_temp+'.txt','w',encoding='gb18030')    #***。txt
    write_words(words_dic,dfs)
    dfs.close()
    ddfs=open('./解词\\'+name_temp+'\\词频'+name_temp+'.txt','w',encoding='gb18030')   #词频***.txt
    write_words(all_words,ddfs)
    ddfs.close()
#将读取的字典和词频字典，统计总字典
def sumdic(fillname_list):
    dic={}
    fillname_list=readfillnames()
    for file in fillname_list:
        dfs=open(file,'r',encoding='gb18030',errors='ignore')
        for line in dfs.readlines():
            key=line.split(':')[0].strip()
            value=int(line.split(':')[-1].strip())
            if key not in dic.keys():
                dic[key]=value
            else:
                dic[key]+=value
    for t in list(dic.keys()):
        if dic[t]<8 :
            del dic[t]
    afs=open('./字典.txt','w',encoding='gb18030')
    write_words(dic,afs)
    afs.close()
#统计总词频
def sumcipindic():
    cipin_dic={}
    cipin_fullnamelist=readcipin_fullnames()
    for file in cipin_fullnamelist:
        dfs=open(file,'r',encoding='gb18030',errors='ignore')
        for line in dfs.readlines():
            key=line.split(':')[0].strip()
            value=int(line.split(':')[-1].strip())
            if key not  in cipin_dic.keys():
                cipin_dic[key]=value
            else:
                cipin_dic[key]+=value
    afs=open('./词频字典.txt','w',encoding='gb18030')
    write_words(cipin_dic,afs)
    afs.close()

if __name__=='__main__':
    for dir in os.listdir('./文本分类语料库'):
        print(dir)
        if not os.path.exists('./解词\\'+dir):
            os.mkdir('./解词/'+dir)
    fullname_list=readfullnames()
    fillname_list=readfillnames()
    segfile(fullname_list)
    sumdic(fillname_list)
    sumcipindic()

