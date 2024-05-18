import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextEdit, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QScrollArea
import huffman
import lzw

class FileBrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Compressor - Decompressor')
        self.setFixedSize(QSize(400,500))

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        sub_layout = QHBoxLayout()
        layout.addLayout(sub_layout)

        self.file_path_edit = QLineEdit(self)
        self.file_path_edit.setReadOnly(True)
        sub_layout.addWidget(self.file_path_edit)

        self.browse_button = QPushButton('Browse Files', self)
        self.browse_button.clicked.connect(self.open_file_dialog)
        sub_layout.addWidget(self.browse_button)

        self.contents = QTextEdit()
        layout.addWidget(self.contents)

        self.button1 = QPushButton("Compress Huffman", self)
        self.button1.clicked.connect(self.on_clicked)
        self.button1.setEnabled(False)
        layout.addWidget(self.button1)

        self.button2 = QPushButton("Decompress Huffman", self)
        self.button2.clicked.connect(self.on_clicked)
        self.button2.setEnabled(False)
        layout.addWidget(self.button2)

        self.button3 = QPushButton("Compress LZW", self)
        self.button3.clicked.connect(self.on_clicked)
        self.button3.setEnabled(False)
        layout.addWidget(self.button3)

        self.button4 = QPushButton("Decompress LZW", self)
        self.button4.clicked.connect(self.on_clicked)
        self.button4.setEnabled(False)
        layout.addWidget(self.button4)

        self.statusbar = self.statusBar()

    def open_file_dialog(self):
        self.button1.setEnabled(False)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.file_path_edit.setText(file_path)
            self.file_path = file_path
            self.button1.setEnabled(True)
            self.button3.setEnabled(True)
            with open(file_path, 'r') as f:
                text = f.read()
            self.contents.setText(text)

    def on_clicked(self):
        sender = self.sender()
        match sender:
            case self.button1:
                if self.file_path:
                    self.encoded_data, self.huffman_tree = huffman.compress(self.file_path)
                    self.button2.setEnabled(True)
                    self.statusbar.showMessage('File Saved', 1000)
            case self.button2:
                huffman.decompress(self.encoded_data, self.huffman_tree)
                self.statusbar.showMessage('File Saved', 1000)
            case self.button3:
                if self.file_path:
                    lzw.compress(self.file_path)
                    self.button4.setEnabled(True)
                    self.statusbar.showMessage('File Saved', 1000)
            case self.button4:
                lzw.decompress()
                self.statusbar.showMessage('File Saved', 1000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileBrowserApp()
    ex.show()
    sys.exit(app.exec_())

