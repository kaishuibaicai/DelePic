from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QFileDialog
import sys, os

class Example(QWidget):

	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):

		self.btn = QPushButton('Open Dir', self)
		self.btn.move(20, 20)
		self.btn.clicked.connect(self.opendir)

		self.setGeometry(300, 300, 290, 150)
		self.setWindowTitle('删图')
		self.show()

	def opendir(self):
		directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "H:\新建文件夹")
		files = []
		for fname in os.listDir(directory):
			files.append(fname)
			print (fname)
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())