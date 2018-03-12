from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QImage, QPainter, QPalette, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
        QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
import os, shutil

class ImageViewer(QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()

        self.files = []
        self.sfiles = []
        self.c = -1
        self.path = ""
        self.p = 0


        self.printer = QPrinter()
        self.scaleFactor = 0.0

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        
        self.lb1 = QLabel('学点编程吧，我爱你~！',self)
        self.statusBar().showMessage('Ready')
        
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")
        self.resize(500, 400)
        self.show()

    def openimg(self, url):

        if url:
            image = QImage(url)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % url)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            if self.files[self.c] not in self.sfiles:
                status = '将要删除'
            else:
                status = '保存'
            self.statusBar().showMessage(status)

            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()
    def opendir(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "H:\新建文件夹")
        self.opdir(directory)

    def opdir(self, directory):
        if directory:
            self.files = []
            self.sfiles = []
            self.p = 0
            self.path = directory
            for fname in os.listdir(directory):
                if fname != 'safeFiles':
                    self.files.append(fname)
                    self.sfiles.append(fname)
            if self.files:
                self.c = 0
                self.openimg(self.path + '\\' + self.files[self.c])
            if not os.path.exists(directory + '\\' + 'safeFiles'):
                os.mkdir(directory + '\\' + 'safeFiles')


    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_A:
            self.c -= 1
            if self.c < 0:
                self.c =0
                QMessageBox.information(self, "提示", "这是第一张...")
            else:
                self.openimg(self.path + '\\' + self.files[self.c])
        elif e.key() == Qt.Key_S:
            if self.files[self.c] in self.sfiles:
                self.sfiles.remove(self.files[self.c])
                if self.c  > self.p:
                    self.p = self.c + 1
            else:
                self.sfiles.append(self.files[self.c])
            self.openimg(self.path + '\\' + self.files[self.c])
        elif e.key() == Qt.Key_D:
            self.c += 1
            if self.c > (len(self.files) - 1):
                self.c -=1
                QMessageBox.information(self, "提示", "这是最后一张...")
            else:
                self.openimg(self.path + '\\' + self.files[self.c])

    def deleFile(self):
        reply = QMessageBox.question(self, '警告',
            "确定要删除？", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            print ('delete')

            for f in self.files[0:self.p]:
                if f not in self.sfiles:
                    os.remove(self.path + '\\' + f)
                    print (f, '  deleted')
                    #self.files.remove(f)
                else:
                    shutil.move(self.path + '\\' + f, self.path + '\\' + 'safeFiles\\' + f)
            #self.c = self.p - (len(self.files)-len(self.sfiles))
            #self.files = self.sfiles
            #print (self.c)
            #self.openimg(self.path + '\\' + self.files[self.c])
            self.opdir(self.path)
        else:
            print ('holly')




    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self):
        QMessageBox.about(self, "About Image Viewer",
                "<p>The <b>Image Viewer</b> example shows how to combine "
                "QLabel and QScrollArea to display an image. QLabel is "
                "typically used for displaying text, but it can also display "
                "an image. QScrollArea provides a scrolling view around "
                "another widget. If the child widget exceeds the size of the "
                "frame, QScrollArea automatically provides scroll bars.</p>"
                "<p>The example demonstrates how QLabel's ability to scale "
                "its contents (QLabel.scaledContents), and QScrollArea's "
                "ability to automatically resize its contents "
                "(QScrollArea.widgetResizable), can be used to implement "
                "zooming and scaling features.</p>"
                "<p>In addition the example shows how to use QPainter to "
                "print an image.</p>")

    def createActions(self):
        self.openAct = QAction("&Open Dir", self, shortcut="Ctrl+O",
                triggered=self.opendir)  
        self.deleAct = QAction("&Delete File", self, shortcut="Ctrl+D",
                triggered=self.deleFile)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++",
                enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-",
                enabled=False, triggered=self.zoomOut)

        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S",
                enabled=False, triggered=self.normalSize)

        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False,
                checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)

        self.aboutAct = QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.deleAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * scrollBar.pageStep()/2)))

    

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    imageViewer = ImageViewer()
    sys.exit(app.exec_())