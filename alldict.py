import os
import math
#获取每个文件下txt的路径
def get_fullname_list():
    path="./解词"
    dirname_list=os.listdir("./解词")
    fullname_list=[]
    for dirname in dirname_list:
        new_path=path+"\\"+dirname
        filename_list=os.listdir(new_path)
        for filename in filename_list:
            fullname=new_path+'\\'+filename
            fullname_list.append(fullname)
    return fullname_list
#将字典写入对应的文件中
def write_words(words_dic,dfs):
    for k in words_dic.items():
        st=''.join(['%s : %s' %k])
        dfs.write(st)
        dfs.write('\n')

# 读取训练文档总数目
def getN():
    n = 0
    fullname_list = []
    m = os.listdir("./文本分类语料库")
    for dir in os.listdir("./文本分类语料库"):
        for filename in os.listdir("./文本分类语料库\\" + dir):
            n += 1
    return n
# def getworddict():
#     fullname_list=get_fullname_list()
#     worddict={}
#     dfs=open("./ffile.txt",'w')
#     for fullname in fullname_list:
#         print(fullname)
#         ifs=open(fullname,'r')
#         wordset=set()
#         for line in ifs.readlines():
#             words=line.strip().split()
#             wordset=set(words)
#         for w in wordset:
#             if w in worddict.keys():
#                 worddict[w]+=1
#             else:
#                 worddict[w]=1
#     write_words(worddict,dfs)
#     return worddict
#读取总字典。txt
def get_worddict():
    dic={}
    afs=open("./字典.txt",'r',encoding='gb18030')
    for line in afs.readlines():
        key=line.split(':')[0].strip()
        value=int(line.split(':')[-1].strip())
        dic[key]=value
    afs.close()
    return dic
#读取总词频。txt
def get_cipinworddict():
    dic={}
    afs=open("./词频字典.txt",'r',encoding='gb18030')
    for line in afs.readlines():
        key=line.split(":")[0].strip()
        value=int(line.split(":")[-1].strip())
        dic[key]=value
    afs.close()
    return dic
#读取每个类的类词频
def get_class_cipinworddict(name_temp):
    dic={}
    afs=open("./解词\\"+name_temp+'\\词频'+name_temp+'.txt','r',encoding='gb18030')
    for line in afs.readlines():
        key=line.split(':')[0].strip()
        value=int(line.split(':')[-1].strip())
        dic[key]=value
    afs.close()
    return dic
#创建标签
def create_classname_dict():
    #标签字典  标签对应的数字
    classname_dict={}
    classname_dict["艺术"] = 1
    classname_dict["教育"] = 2
    classname_dict["演讲"] = 3
    classname_dict["历史"] = 4
    classname_dict["哲学"] = 5
    classname_dict["宇航"] = 6
    classname_dict["核能"] = 7
    classname_dict["计算机"] = 8
    classname_dict["交通"] = 9
    classname_dict["运动"] = 10
    return classname_dict
#创建特征文件
def create_feature_file():
    classname_dict=create_classname_dict()
    worddict=get_worddict()
    cipin_dict=get_cipinworddict()
    array_worddict=list(worddict.keys())
    fullname_list=get_fullname_list()
    N=getN()
    ofs=open("./featurefile.txt",'w',encoding="gb18030")
    temp_class=''
    for fullname in fullname_list:
        str=''
        classno = -1
        dirname = fullname.split("./解词\\")[1].split('\\')[0]
        for classname in classname_dict.keys():
            if classname in fullname:
                classno = classname_dict[classname]
                print(classno)
                break
        if temp_class!=dirname:
            class_cipindict=get_class_cipinworddict(dirname)
            temp_class=dirname
            print(dirname)
        str = repr(classno)+' '
        ifs_curfile = open(fullname,'r',encoding='gb18030')
        # 统计每个词在每篇文章中出现的次数tf
        file_worddict={}
        for line in ifs_curfile.readlines():
            words=line.rstrip().split()
            for w in words:
                if w not in file_worddict.keys():
                    file_worddict[w]=1
                else:
                    file_worddict[w]+=1
        #遍历词频，计算每个词的tf、df值，最后得到权重weight，创建特征向量文件
        for wordno in range(0,len(array_worddict)):
            tf=0
            ctf=0
            nctf=1
            w=array_worddict[wordno]
            if w in file_worddict.keys():
                #tf值
                tf=file_worddict[w]
                #print(w)
                try:
                    ctf=class_cipindict[w]
                    #print(ctf)
                    nctf=cipin_dict[w]-ctf
                except:
                    continue
                if nctf==0:
                    nctf=1
                #print(nctf)
            #idf的值
            df=worddict[w]
            #权重weight
            weight=1.0*tf*math.log((N/df),2)
            str+=repr(wordno+1)+':'+repr(weight)+' '
        #创建特征向量文件
        ofs.write(str.rstrip()+'\n')
    ofs.close()
if __name__=='__main__':
    create_feature_file()
