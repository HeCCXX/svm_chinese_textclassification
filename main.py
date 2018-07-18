#-*- coding= gbk -*-
import sys

from PyQt5 import QtWidgets
from UI import Svm_ui
app=QtWidgets.QApplication(sys.argv)
form=Svm_ui()
form.show()
sys.exit(app.exec_())