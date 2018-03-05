#!/usr/bin/env python

#============================================================================#
# PyQt5 port of the designer/containerextension example from Qt v5.x         #
#----------------------------------------------------------------------------#
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import (QApplication, QComboBox, QLabel, QStackedWidget,
        QVBoxLayout, QWidget,QPushButton, QLineEdit, QApplication, QTextEdit)
import os,sys
import book

#============================================================================#
# Implementation of a MultiPageWidget using a QComboBox and a QStackedWidget #
#----------------------------------------------------------------------------#

class MyCustomWidget(QWidget):
    second_switched = pyqtSignal()
    def __init__(self, query, parent=None):
        super(MyCustomWidget, self).__init__(parent)
        self.query = query
        layout = QVBoxLayout(self)

        # Create a progress bar and a button and add them to the main layout
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0,1)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.label)

        button = QPushButton("Start", self)
        layout.addWidget(button)
        button.clicked.connect(self.onStart)

        self.myLongTask = TaskThread(self.query)
        self.myLongTask.taskFinished.connect(self.onFinished)


    def onStart(self):
        self.progressBar.setRange(0,0)
        self.label.setText("Đợi tí, đang xác thực...")
        self.myLongTask.start()


    def onFinished(self):
        # Stop the pulsation

        self.progressBar.setRange(0,1)
        self.switched.emit()
        self.myLongTask.resulted.emit(search_results)

class TaskThread(QThread):

    taskFinished = pyqtSignal()
    resulted = pyqtSignal(list)
    def __init__ (self,query):
        self.query = query
    @pyqtSlot()
    def run(self):
        self.auth()
        time.sleep(7)
        self.taskFinished.emit()
    def auth(self):
        DEBUG = True

        # Log initialization
        log_level = logging.DEBUG if DEBUG else logging.INFO
        log_format = '%(asctime)s - %(levelname)s - %(module)s : %(lineno)d - %(message)s'
        logging.basicConfig(level=log_level, format=log_format)
        logger = logging.getLogger(__name__)


        query = None
        repository = book.Inventory('.//subdoc-abstract/paragraph/text()','.//subdoc-bibliographic-information/document-id/')
        logger.info('Loading books...')

        repository.load_books()
        docs_number = repository.books_count()
        logger.info('Done loading books, %d docs in index', docs_number)

        while query is not '':
            self.search_results = repository.search_books(self.query)


class PyMultiPageWidget(QWidget):
    switched = pyqtSignal()

    currentIndexChanged = pyqtSignal(int)

    pageTitleChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(PyMultiPageWidget, self).__init__(parent)

        self.comboBox = QComboBox()
        # MAGIC
        # It is important that the combo box has an object name beginning
        # with '__qt__passive_', otherwise, it is inactive in the form editor
        # of the designer and you can't change the current page via the
        # combo box.
        # MAGIC
        self.comboBox.setObjectName('__qt__passive_comboBox')
        self.stackWidget = QStackedWidget()
        self.comboBox.activated.connect(self.setCurrentIndex)
        self.lb = QLabel("Chọn số trường")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lb)
        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.stackWidget)
        self.setLayout(self.layout)

    def sizeHint(self):
        return QSize(400, 350)

    def count(self):
        return self.stackWidget.count()

    def widget(self, index):
        return self.stackWidget.widget(index)

    @pyqtSlot(QWidget)
    def addPage(self, page):
        self.insertPage(self.count(), page)

    @pyqtSlot(int, QWidget)
    def insertPage(self, index, page):
        page.setParent(self.stackWidget)
        self.stackWidget.insertWidget(index, page)
        title = page.windowTitle()
        if title == "":
            title = "Title %d" % (self.comboBox.count() + 1)
            page.setWindowTitle(title)
        self.comboBox.insertItem(index, title)

    @pyqtSlot(int)
    def removePage(self, index):
        widget = self.stackWidget.widget(index)
        self.stackWidget.removeWidget(widget)
        self.comboBox.removeItem(index)

    def getPageTitle(self):
        cw = self.stackWidget.currentWidget()
        return cw.windowTitle() if cw is not None else ''

    @pyqtSlot(str)
    def setPageTitle(self, newTitle):
        cw = self.stackWidget.currentWidget()
        if cw is not None:
            self.comboBox.setItemText(self.getCurrentIndex(), newTitle)
            cw.setWindowTitle(newTitle)
            self.pageTitleChanged.emit(newTitle)

    def getCurrentIndex(self):
        return self.stackWidget.currentIndex()

    @pyqtSlot(int)
    def setCurrentIndex(self, index):
        if index != self.getCurrentIndex():
            self.stackWidget.setCurrentIndex(index)
            self.comboBox.setCurrentIndex(index)
            self.currentIndexChanged.emit(index)

    pageTitle = pyqtProperty(str, fget=getPageTitle, fset=setPageTitle, stored=False)
    currentIndex = pyqtProperty(int, fget=getCurrentIndex, fset=setCurrentIndex)

class List():
    def __init__(self):
        super(List,self).__init__()
        self.lst = ["title","description","abstract"]

'''
Cách làm cho nó ngắn hơn: 1 class có 1 nhóm các widget,
 sau đó các class khác tạo instance của class đó để clone ra những nhóm
 widget tương tự
'''

class TitleWidget(QWidget):
    def __init__(self):
        super(TitleWidget,self).__init__()
        self.layout = QVBoxLayout(self)
        self.queryText = QLineEdit(self)
        self.queryText

class FormWidget(QWidget):

    def __init__(self):
        super(FormWidget, self).__init__()

        self.lb = QLabel("Term 1",self)
        self.lb.move(10,110)
        self.button2 = QLineEdit(self)
        self.button2.move(60,110)
        self.lb2 = QLabel("in Field 1: ",self)
        self.lb2.move(210,110)
        self.opt = QComboBox(self)
        self.opt.addItems(List().lst)
        self.opt.move(290,110)


        self.setWindowTitle("1 trường")

class SecondaryFormWidget(QWidget):
    def __init__(self):
        super(SecondaryFormWidget,self).__init__()

        self.lb = QLabel("Term 1",self)
        self.lb.move(10,80)
        self.button2 = QLineEdit(self)
        self.button2.move(60,80)
        self.lb2 = QLabel("in Field 1: ",self)
        self.lb2.move(210,80)
        self.opt = QComboBox(self)
        self.opt.addItems(List().lst)
        self.opt.move(290,80)

        self.lb = QLabel("Term 2",self)
        self.lb.move(10,130)
        self.button2 = QLineEdit(self)
        self.button2.move(60,130)
        self.lb2 = QLabel("in Field 2: ",self)
        self.lb2.move(210,130)
        self.opt = QComboBox(self)
        self.opt.addItems(List().lst)
        self.opt.move(290,130)

        self.setWindowTitle("2 trường ")
#============================================================================#
# Main for testing the class                                                 #
#----------------------------------------------------------------------------#


class XmlDisplay(QWidget):
    def __init__(self,name,root_path,parent=None):
        super(XmlDisplay,self).__init__(parent)
        self.name = name
        self.root_path = root_path

    def find(self):
        for root, dirs, files in os.walk(self.root_path):
            if name in files:
                return os.path.join(root, self.name)
    def display(self,x_path):
                #disable entities_resolving
            parser = etree.XMLParser(resolve_entities=False)
            tree = etree.parse(self.find(),parser=parser)
            root = tree.getroot()
            for content in root.xpath(x_path):
                return content


class Description(XmlDisplay):
    def __init__(self,name,root_path):
        XmlDisplay.__init__(self,name,root_path)
        summary = self.display(".//subdoc-description/summary-of-invention/section/paragraph/text()")
        self.text = QTextEdit(self)
        self.text.setPlainText(summary)

class Abstract(XmlDisplay):
    def __init__(self,name,root_path):
        XmlDisplay.__init__(self,name,root_path)
        abstract = self.display(".//subdoc-abstract/paragraph/text()")
        self.text = QTextEdit(self)
        self.text.setPlainText(abstract)

class XmlWindow(XmlDisplay):
    def __init__(self,name,root_path):
        XmlDisplay.__init__(self,name,root_path)
        self.choice = PyMultiPageWidget(self)
        self.choice.addPage(Description(self.name,self.root_path))
        self.choice.addPage(Abstract(self.name,self.root_path))





class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow,self).__init__()
        self.form = PyMultiPageWidget(self)
        self.form.addPage(FormWidget())
        self.form.addPage(SecondaryFormWidget())
        self.progress = MyCustomWidget(self)

        self.central_widget = QStackedWidget(self)
        self.central_widget.addWidget(self.form)
        self.central_widget.addWidget(self.progress)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setCurrentWidget(self.form)
        self.form.switched.connect(self.onSwitched)
        #self.move(300, 150)
        self.setWindowTitle('Tìm kiếm')
    def onSwitched(self):
        self.central_widget.setCurrentWidget(self.progress)
        self.form.second_switched.connect(self.onSecondSwitched)
    def onSecondSwitched(self):
        self.central_widget.setCurrentWidget(XmlWindow(name=,root_path=))

    def onResulted(self, lst):


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = MyMainWindow()
    widget.show()
    sys.exit(app.exec_())

#============================================================================#
# EOF                                                                        #
#----------------------------------------------------------------------------#
