from svm_ui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import txt_segfile
import segfile
import alldict
import txt_alldict
import os
import SVM
from svmutil import *
import svm
class Svm_ui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(Svm_ui, self).__init__(*args, **kwargs)
        self.setupUi(self)
        #连接加载训练集加载路径
        self.Btn_train.clicked.connect(self.load_train)
        # 连接加载测试集加载路径
        self.Btn_test.clicked.connect(self.load_test)
        # 连接预处理函数
        self.Btn_seg.clicked.connect(self.seg)
        self.Btn_go.clicked.connect(self.go_train)
        self.Btn_vec.clicked.connect(self.create_vector)
        self.Btn_classify.clicked.connect(self.run)
    def load_train(self):
        file_name=QtWidgets.QFileDialog.getExistingDirectory(self,'选择训练集文件夹','./')
        self.label_3.setText(file_name)
        pass
    def load_test(self):
        file_name = QtWidgets.QFileDialog.getExistingDirectory(self, '选择训练集文件夹', './')
        self.label_4.setText(file_name)
        pass
    def seg(self):
        file_name=self.label_3.text()
        txt_name=file_name.split('文本分类语料库')[0]
        for dir in os.listdir(file_name):
            print(dir)
            if not os.path.exists(txt_name+'/解词/' + dir):
                os.mkdir(txt_name+'/解词/' + dir)
        # 读取每个文件中txt的全路径
        fullname_list = segfile.readfullnames(file_name)
        # 读取每个文件中的字典路径
        fillname_list = segfile.readfillnames()
        # txt 进行分词，统计词频，将类的总字典和词频字典写入每个类中，保存为txt
        # 统计每个文章中的词在多少篇文章中出现，保存到***。txt
        segfile.segfile(fullname_list)
        # 将读取的字典和词频字典，统计总字典
        segfile.sumdic(fillname_list)
        # 统计总词频
        segfile.sumcipindic()

        tfile_name=self.label_4.text()
        ttxt_name = tfile_name.split('testdata')[0]
        for dir in os.listdir(tfile_name):
            print(dir)
            if not os.path.exists(ttxt_name+'/txt解词/' + dir):
                os.mkdir(ttxt_name+'/txt解词/' + dir)
        fullname_list = txt_segfile.readfullnames(tfile_name)
        fillname_list = txt_segfile.readfillnames()
        txt_segfile.segfile(fullname_list)
        txt_segfile.sumdic(fillname_list)
        txt_segfile.sumcipindic()
        self.label_5.setText("语料库预处理完毕。")

    def create_vector(self):
        alldict.create_feature_file()
        txt_alldict.create_feature_file()
        self.label_5.setText("创建特征向量文件完成。")

    def go_train(self):
        #输入训练参数
        parameter=self.param.toPlainText()
        #读取新数据
        y, x = svm_read_problem("./1_scale.txt")
        prob = svm_problem(y, x)
        #传递训练参数
        param = svm.svm_parameter(parameter)
        #训练、生成模型并保存
        model = svm_train(prob, param)
        svm_save_model("./mode.txt", model)
        self.label_5.setText("训练完成，创建分类器完成。")
    def run(self):
        #out=SVM.go()
        self.label_5.setText("")
        m=[]
        #读取模型文件
        model=svm_load_model("./mode.txt")
        #读取特征文件
        x, y = svm_read_problem('./2_scale.txt')
        #进行文本分类，预测
        p_label, p_acc, p_val = svm_predict(x, y, model)
        with open("./mode.txt",'r') as f:
            for line in f.readlines()[:8]:
                m.append(line.strip())
        #分类结果保存至result.txt
        with open("./result.txt", 'w',encoding="gbk") as f2:
            for i in p_label:
                f2.write(str(i) + "\n")
            for j in m:
                f2.write(j + "\n")
            f2.write("Accuracy(准确率) = " + str(p_acc[0]) + "%    (classification)")
        f2.close()
        #显示结果
        self.textEdit.setText(str(p_label)+"\n"+str(m[0])+"\n"+str(m[1])
                              +"\n"+str(m[2])+"\n"+str(m[3])+"\n"+str(m[4])
                              +"\n"+str(m[5])+"\n"+str(m[6])+"\n"+str(m[7])
                              +"\n\nAccuracy(准确率) = "+str(p_acc[0])+"%    (classification)")
        self.label_5.setText("分类完成！")


